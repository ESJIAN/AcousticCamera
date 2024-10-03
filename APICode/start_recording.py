# Notice:导入主模块中的变量
# 在主模块中定义变量，在子模块中修改全局变量


import sys
sys.path.append("D:\\Users\\JDG223\\Documents\\VSCODE\\Python\\AcousticCamera")

# 使用绝对导入的方式导入变量
from MainCode.acoustic_Location_updated_2d import stream,is_recording

def start_recording():
    global stream, is_recording
    if not is_recording:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
        is_recording = True
        update_plot()
        

