import datetime
import os

DEVICE_NAME_MAP={
    'NVIDIA GeForce GTX 1080 Ti': '1080Ti',
    'NVIDIA A40': '40A',
    'NVIDIA GeForce RTX 3090': '3090RTX'
}

def notion():
    print("Cofrun is ready to execute multiple tasks in batch mode. \
There're maybe some useful suggestions: \n\
    1. install and launch tmux. the following are some necessary related instructions: \n\
        * create a new tmux window: tmux new -s cof\n\
        * detach from the current session: Ctrl+b d\n\
        * attach to an existing session: tmux attach -t cof\n\
    2. the process would hang up if distributed task crashes. we strongly recommand you to: \n\
        * add \"export TORCH_NCCL_ASYNC_ERROR_HANDLING=1, pkill python\" to your template script\n\
        * if process hangs up, you can input \"pkill python\" command or Ctrl+C to skip the current task\n")
    
def logging(msg, *args):
    for each_arg in args:
        msg += str(each_arg)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[cofrun {formatted_time}] {msg}")
    if not os.path.exists("cof_workspace/"):
        os.mkdir("cof_workspace/")
    with open("cof_workspace/history.cof", "a+") as file:
        file.write(f"[cofrun {formatted_time}] {msg}\n")