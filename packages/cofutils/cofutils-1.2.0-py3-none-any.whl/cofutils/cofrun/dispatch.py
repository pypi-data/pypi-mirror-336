import json
import os
import argparse
import subprocess
import datetime
import time
import torch
import re
import copy
import shutil
from tabulate import tabulate
from collections import defaultdict
from ..cofwriter import cofcsv
from .common import DEVICE_NAME_MAP, notion, logging
GLOBAL_ARGS = None

def get_log_name_from_config(global_config_file, current_config_file, key_suffix):
    if key_suffix == '':
        return ''
    if key_suffix in ['all', 'diff']:
        with open(global_config_file) as fp:
            config_list = json.load(fp)
        full_keys = {}
        for config in config_list:
            for key in config:
                if key not in full_keys:
                    full_keys[key] = []
                if isinstance(config[key], list):
                    for _key in config[key]:
                        if _key not in full_keys[key]:
                            full_keys[key].append(_key)
                else:
                    if config[key] not in full_keys[key]:
                        full_keys[key].append(config[key])
        diff_keys = [key for key in full_keys if len(full_keys[key]) > 1]
    else:
        diff_keys = key_suffix.split(',')
    
    name = ''
    with open(current_config_file) as fp:
        config_list = json.load(fp)
    for key in diff_keys:
        for config in config_list:
            if key in config:
                name += f'.{key}={config[key]}'
    return name
        
            
def auto_exec():
    if GLOBAL_ARGS.test:
        logging(f"{GLOBAL_ARGS.config_file} test done")
        return
    if not os.path.exists(GLOBAL_ARGS.tmp_dir):
        os.mkdir(GLOBAL_ARGS.tmp_dir)
    if GLOBAL_ARGS.output_dir is not None:
        # check if output directory exists or not
        if not os.path.exists(GLOBAL_ARGS.output_dir):
            os.mkdir(GLOBAL_ARGS.output_dir)
        now = datetime.datetime.now()
        gpu_name = torch.cuda.get_device_properties(torch.device("cuda")).name
        def extract_gpu_info(name):
            if name in DEVICE_NAME_MAP.keys():
                return DEVICE_NAME_MAP[name]
            else:
                return 'GPU'
        formatted_time = now.strftime("%m%d%H%M%S")
        # mkdir
        task_name = extract_gpu_info(gpu_name) + formatted_time + get_log_name_from_config(GLOBAL_ARGS.file, GLOBAL_ARGS.config_file, GLOBAL_ARGS.key_suffix)
        log_dir = os.path.join(GLOBAL_ARGS.output_dir, task_name)
        os.mkdir(log_dir)
        # write config file
        with open(GLOBAL_ARGS.config_file) as fp:
            config_list = json.load(fp)
        
        # save config json file
        with open(f'{log_dir}/config.json', "w") as fp:
            json.dump(config_list,fp=fp, indent=4, separators=(',', ': '))
        # save template bash script
        shutil.copy(GLOBAL_ARGS.template_file, f'{log_dir}/run.sh')
        # launch task
        logging("launch task: ", task_name)
        with open(f'{log_dir}/log', 'w') as fp:
            try: 
                result = subprocess.run(['bash', 'cof_workspace/launch-all.sh'], stdout=fp, stderr=subprocess.STDOUT, text=True)
                logging(f"task {task_name} return code: {result.returncode}")
            except KeyboardInterrupt:
                logging(f"task {task_name} killed by users")
        GLOBAL_ARGS.log_file_list.append(f'{log_dir}/log')

        for filename in os.listdir(GLOBAL_ARGS.tmp_dir):
            # Construct full file path
            file_path = os.path.join(GLOBAL_ARGS.tmp_dir, filename)
            if os.path.isfile(file_path):
                shutil.move(file_path, log_dir)
        
        logging(f"saving to {log_dir} ...")
    else:
        subprocess.run(['bash','cof_workspace/launch-all.sh'])

def auto_gen():
    GLOBAL_ARGS.target_file_name = os.getcwd().strip('/').replace('/', '-')
    host_file_name="cof_workspace/hostfile"
    launch_file_name="cof_workspace/launch-all.sh"
    script_file_name=f'cof_workspace/{GLOBAL_ARGS.target_file_name}.sh'
    cluster_ip_list=list()

    def autogen_from_template(config_table, template_file, ipx):
        def compile(line:str, table):
            line = line.strip('\n')
            key_list = line.split('%')
            re_table = table
            for key in key_list:
                if key:
                    re_table=re_table[key]
            if isinstance(re_table, bool):
                re_table=str(re_table).lower()
            return '_'.join(key_list)+f"={re_table}\n"
                
        with open(template_file, 'r') as file:
            lines = file.readlines()

        modified_lines = [compile(line, config_table) if line.startswith('%') else line for line in lines]
        modified_lines = [ '_'.join(line.strip('\n').split('&'))+f"={ipx}\n"if line.startswith('&') else line for line in modified_lines]
        return ''.join(modified_lines)

    with open(GLOBAL_ARGS.config_file) as f:
        config_list = json.load(f)
    config_table = {k:v for each in config_list for k,v in each.items()}
    logging("\n"+tabulate([[k,v] for k,v in config_table.items()], headers=["Configuration Key", "Value"], tablefmt="rounded_outline"))
    cluster_ip_list = [each for each in config_table["CLUSTER_IPS"].split(" ") if each]
    
    ##########################################
    # generate launch-all.sh!
    ##########################################
    NNODES = config_table['NNODES']
    
    current_dir = os.getcwd()
    nsys_start_cmd = f'pkill nsys; nsys start --stop-on-exit=false --stats=true -c cudaProfilerApi -f true -o {os.path.join(GLOBAL_ARGS.tmp_dir,"target")};'
    nsys_launch_cmd = 'nsys launch --wait=primary --trace=cuda,nvtx'
    launch_all_content = f'{nsys_start_cmd if GLOBAL_ARGS.nsys else ""} mpirun -np {NNODES} \\\n\
    --hostfile {current_dir}/cof_workspace/hostfile  \\\n\
    -bind-to none -map-by slot \\\n\
    --allow-run-as-root \\\n\
    -x LD_LIBRARY_PATH -x PATH \\\n\
    {nsys_launch_cmd if GLOBAL_ARGS.nsys else ""} bash /tmp/{GLOBAL_ARGS.target_file_name}.sh \n\
second_return_code=$?\n\
if [ $second_return_code -ne 0 ]; then \n\
    exit 1 \n\
fi \n\
exit 0'
    if not os.path.exists("cof_workspace/"):
        os.mkdir("cof_workspace/")
    with open(launch_file_name,"w") as fp:
        fp.write(launch_all_content)
    for host_idx,host_ip in enumerate(cluster_ip_list[:NNODES]):
        script_content = autogen_from_template(config_table, GLOBAL_ARGS.template_file, host_idx)
        with open(script_file_name,'w') as f:
            f.write(script_content)
        dispatch_cmd=f'scp {script_file_name} {host_ip}:/tmp/'
        return_code=os.system(dispatch_cmd+" > /dev/null 2>&1")
        return_code="successfully" if return_code==0 else "failed"
        logging(f"{dispatch_cmd} ..................... {return_code}")
    if return_code!="successfully":
        logging("failed to dispatch tasks")
        return -1
    else:
        logging("successfully dispatch tasks")
        
    ##########################################
    # generate hostfile!
    ##########################################

    with open(host_file_name,"w") as fp:
        for each_ip in cluster_ip_list[:NNODES]:
            fp.write(each_ip + " slots=1\n")
    return 0

def process_file():
    assert auto_gen()==0
    start = time.time()
    auto_exec()
    end = time.time()
    GLOBAL_ARGS.total_time+=end-start
    logging(f"{GLOBAL_ARGS.config_file} done execution time: {end-start:.2f}s")

def process_batched_files():
    global GLOBAL_ARGS
    assert os.path.exists(GLOBAL_ARGS.input_dir), GLOBAL_ARGS.input_dir+" not exist"
    config_file_list = []
    for _, _, files in os.walk(GLOBAL_ARGS.input_dir):
        for file in files:
            config_file_list.append(os.path.join(GLOBAL_ARGS.input_dir, file))
    config_file_list.sort()
    if GLOBAL_ARGS.list:
        print("="*25)
        print("     Print Log List")
        print("="*25)

        print(f"log num: {len(config_file_list)}")
        print("id         name")
        for id, dir in enumerate(config_file_list):
            print(f"{id}    {dir}")

        print("-"*25)
        logging("list input files done")
        GLOBAL_ARGS.config_file_list=[]
    else:     
        def parse_str_range(str_range:str):
            str_range_list = str_range.split(',')
            print(str_range_list)
            int_range = []
            for each in str_range_list:
                integers = re.findall(r'\d+', each)
                if '-' in each:
                    start = int(integers[0])
                    end = int(integers[1])+1
                    int_range += list(range(start, end))
                else:
                    int_range.append(int(integers[0]))
            return int_range
        candidate_config_file_list = [config_file_list[each] for each in parse_str_range(GLOBAL_ARGS.range)] if GLOBAL_ARGS.range is not None else config_file_list
        GLOBAL_ARGS.config_file_list=candidate_config_file_list
        
        for idx, config_file in enumerate(candidate_config_file_list):
            logging(f"{idx+1}/{len(candidate_config_file_list)} executing: {config_file}")
            GLOBAL_ARGS.config_file = config_file
            process_file()
            logging(f"estimated remaining time: {GLOBAL_ARGS.total_time/(idx+1)*(len(candidate_config_file_list)-idx-1)}s")

def task_setup():
    global GLOBAL_ARGS
    GLOBAL_ARGS.log_file_list=[]
    logging(f"task setup ...")
    if GLOBAL_ARGS.input_dir is not None:
        process_batched_files()
    elif GLOBAL_ARGS.file and GLOBAL_ARGS.template_file:
        def check_inner_list(config_file):
            json_gen_dir = 'cof-gen/'
            with open(config_file) as f:
                config_list = json.load(f)

            def find_lists_and_generate_combinations(config_list, setting_lists):
                # setting_lists = []
                setting_num = 1
                waited_to_visit = [each for each in config_list]
                for config in waited_to_visit:
                    for key, value in config.items():
                        if isinstance(value, dict):
                            waited_to_visit.append(value)
                        elif isinstance(value, list):
                            if value:
                                if not setting_lists:
                                    setting_lists = [[v] for v in value]
                                else:
                                    setting_lists = [s + [v] for s in setting_lists for v in value]
                                setting_num *= len(value)
                                config[key] = []
                            else:
                                config[key] = setting_lists.pop(0)

                return setting_lists, setting_num
            setting_lists = []
            setting_lists, setting_num = find_lists_and_generate_combinations(config_list, setting_lists)
            if setting_lists:
                if os.path.exists(json_gen_dir):
                    shutil.rmtree(json_gen_dir)
                os.mkdir(json_gen_dir)

                for idx in range(setting_num):
                    config_copy = copy.deepcopy(config_list)
                    _, _ = find_lists_and_generate_combinations(config_copy, setting_lists[idx])
                    with open(f'{json_gen_dir}/config-{str(idx).zfill(len(str(setting_num)))}'+".json", "w") as fp:
                        json.dump(config_copy, fp=fp, indent=4, separators=(',', ': '))
            return bool(setting_lists)

        if check_inner_list(GLOBAL_ARGS.file):
            GLOBAL_ARGS.input_dir = 'cof-gen/'
            process_batched_files()
        else:
            GLOBAL_ARGS.config_file = GLOBAL_ARGS.file
            process_file()

def summary():
    global GLOBAL_ARGS
    if GLOBAL_ARGS.summary is None:
        return
    if not (hasattr(GLOBAL_ARGS, 'config_file_list') and hasattr(GLOBAL_ARGS, 'log_file_list')):
        sub_dir_list = sorted([each for each in os.listdir(GLOBAL_ARGS.summary) if os.path.isdir(os.path.join(GLOBAL_ARGS.summary,each))])
        GLOBAL_ARGS.config_file_list = [os.path.join(GLOBAL_ARGS.summary, sub_dir, 'config.json') for sub_dir in sub_dir_list]
        GLOBAL_ARGS.log_file_list = [os.path.join(GLOBAL_ARGS.summary, sub_dir, 'log') for sub_dir in sub_dir_list]
    logging(f"tasks summary: cofrun executes {len(GLOBAL_ARGS.config_file_list)} tasks and generate {len(GLOBAL_ARGS.log_file_list)} logs at all")
    if len(GLOBAL_ARGS.config_file_list)!=len(GLOBAL_ARGS.log_file_list) or len(GLOBAL_ARGS.log_file_list)==0:
        print("some tasks did not generate log files properly, skipping summary!")
        return
    
    def process_log_files(file_paths):
        throughput_value_list=[]
        for file in file_paths:
            with open(file, 'r') as fp:
                log_data = fp.read()
            pattern = r' iteration        \d+/       \d+ \| .*throughput per GPU \(TFLOP/s/GPU\): (\d+\.\d+|\d+) \|.*'
            matches = re.findall(pattern, log_data)
            # print(matches)
            throughput_value_list.append(0)
            if len(matches)>1:
                throughput_value_list[-1]=float(matches[-1])
        return throughput_value_list
    
    def process_json_files(file_paths):
        json_file_table = defaultdict(list)
        same_value = dict()
        diff_value = dict()
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                data = json.load(f)
                data = {k:v for each in data for k,v in each.items()}
            # key_list = data.keys()
            for k,v in data.items():
                json_file_table[k].append(v) 
        for k,v in json_file_table.items():
            if len(set(v))==1:
                same_value[k]=v[0]
            else:
                diff_value[k]=v
        return same_value, diff_value
    same_value, diff_value = process_json_files(GLOBAL_ARGS.config_file_list)
    diff_value['throughput per GPU (TFLOP/s/GPU)']=process_log_files(GLOBAL_ARGS.log_file_list)
    diff_value['configuration file']=[os.path.dirname(file) for file in GLOBAL_ARGS.log_file_list]
    
    logging("same parameter:\n"+tabulate([[k,v] for k,v in same_value.items()], headers=["Same Argument", "Value"], tablefmt="rounded_outline"))
    logging("different parameter and result:\n"+tabulate([[value[idx] for value in diff_value.values()] for idx in range(len(GLOBAL_ARGS.config_file_list))], headers=diff_value.keys(), tablefmt="rounded_outline"))
    
    csv_table = cofcsv('summary')
    for idx in range(len(GLOBAL_ARGS.config_file_list)):
        csv_table.write({k:v[idx] for k,v in diff_value.items()})
    cofcsv.save(root_dir=GLOBAL_ARGS.summary)
    
def main():
    global GLOBAL_ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f', type=str, default=None, help="configuration file path")
    parser.add_argument('--input_dir', '-i', type=str, default=None, help="run experiments in batch mode. all config files are placed in input directory")
    parser.add_argument('--template_file','-T', type=str, default=None, help='provide the path of template .sh file')
    parser.add_argument('--output_dir','-o', type=str, default=None,
                       help='write execution output to specific path')
    parser.add_argument('--test','-t', action='store_true',
                        help='use cofrun in test mode -> just generate bash script')
    parser.add_argument('--nsys','-n', action='store_true',
                        help='use nsys to profile your cuda programme')
    parser.add_argument('--list','-l', action='store_true',
                        help='list id of all input files, only available when input dir is provided')
    parser.add_argument('--range','-r', type=str, default=None,
                        help='support 3 formats: [int | int,int,int... | int-int], and int value must be > 0; for example, --range 0,1-3,6')
    parser.add_argument('--key_suffix','-k', type=str, default='diff',
                        help='name the log directory with the key suffix. `-k diff` means only using the different keys, otherwise keys should be separated with `,`; for example, `-k hidden_size,num_layers` and `-k hidden_size`, etc.')
    parser.add_argument('--tmp_dir', type=str, default='/tmp/coflog/',
                        help='specify the temporary directory path to store the intermediate files. cofrun will automatically copy all files in the temporary directory to the output directory which is specified by `-o. default value is /tmp/coflog/')
    parser.add_argument('--summary','-s', type=str, default=None,
                        help='provide your directory path which contains output files and cofrun would give the experiment summary in csv format')
    GLOBAL_ARGS = parser.parse_args()
    GLOBAL_ARGS.total_time=0
    notion()
    logging("-"*20+"cofrun begin"+"-"*20)

    args_str = "cofrun arguments\n"
    # alignment
    argument_table_data = list()
    for arg in vars(GLOBAL_ARGS):
        argument_table_data.append([arg, getattr(GLOBAL_ARGS, arg)])
    table = tabulate(argument_table_data, headers=["Cofrun Argument", "Value"], tablefmt="rounded_outline")
    logging(args_str+table)
    if GLOBAL_ARGS.summary is None:
        GLOBAL_ARGS.summary = GLOBAL_ARGS.output_dir
        task_setup()
    summary()
    logging("="*10 + "All submitted cofrun tasks done" + "="*10)

if __name__ == "__main__":
    main()