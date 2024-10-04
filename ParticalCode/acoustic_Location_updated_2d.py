### 平面麦克风矩阵波束成形阵列 ###
import sys                                                                      # 导入系统模块
sys.path.append("D:\\Users\\JDG223\\Documents\\VSCODE\\Python\\AcousticCamera") # 将绝对项目路径导入path中



import tkinter as tk
from tkinter import ttk                                             # 导入tkinter的GUI组件库用于图形化展示
import pyaudio                                                      # 导入pyaudio库用于音频输入输出的计算
import numpy as np # type: ignore                                   # 导入numpy数组计算库用于矩阵计算
import matplotlib.pyplot as plt                                     # 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # 导入matplotlib嵌入到tkinter的GUI中
from scipy.fftpack import fft                                       # 导入scipy的fft库用于傅里叶变换计算
import time                                                         # 导入时间模块进行时间度统一




from APICode.calculate_delay_and_sum import *                       # 导入API包函数
from APICode.start_recording import *
from APICode.stop_recording import *
from APICode.update_plot import *



# 导入APICode包中的calculate_delay_and_sum函数


# 路径的最小单位为文件夹而非文件本身


### 麦克风阵列参数初始化 ###



# 麦克风坐标设定(坐标单位：米)
mic_positions = np.array([
    [0,0],              # 麦克风1坐标
    [0,0.6],            # 麦克风2坐标
    [0.40,0.45],        # 麦克风3坐标
    [-0.1,0.60],        # 麦克风4坐标
    [-0.55,-0.30],      # 麦克风5坐标
    [-0.55,-0.30],      # 麦克风6坐标
    [-0.10,-0.60],      # 麦克风7坐标
    [0.40,-0.45],       # 麦克风8坐标 
])



# 麦克风录音参数设定
FORMAT = pyaudio.paInt16    # 设置采样精度为16bit
CHANNELS =8                 # 设置采样通道为8通 
RATE = 44100                # 设置采样率为44.1khz
CHUNK = int(RATE * 0.2)     # 0.2秒
DEVICE_INDEX =1             # 设备编号



### 开始录音 ###


# 初始化pyaudio对象
# 作用：创建PyAudio对象，把对象属性赋值给对象p，这样就可以通过p来访问和操作这个对象的方法和属性了

p = pyaudio.PyAudio()
stream = None           # 音频流对象
is_recording = False    # 是否录音













### GUI界面参数初始化 ###


# 主窗口对象初始化
root = tk.Tk()                                               # 创建一个窗口对象
root.title("Acoustic Localization")                          # 设置窗口标题，名字为Acoustic Localization

# 框架对象初始化
frame = ttk.Frame(root, padding="10")                        # 创建一个框架对象(传参解读）
                                                             # root： 是主窗口对象，ttk.Frame 将作为 root 的一个子组件
                                                             # padding：设置框架内边距
                                                             
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # 配置框架对象 
                                                             # row=0：   指定框架所在的行号为 0。
                                                             # column=0：指定框架所在的列号为 0。
                                                             # sticky=(tk.W, tk.E, tk.N, tk.S)：

                                                             # sticky 参数指定了框架如何扩展以填充其所在网格单元格
                                                             # tk.W (West)：向左扩展
                                                             # tk.E (East)：向右扩展
                                                             # tk.N (North)：向上扩展
                                                             # tk.S (South)：向下扩展
                                                             # 综合起来，sticky=(tk.W, tk.E, tk.N, tk.S) 表示框架将在其所在的网格单元格内尽可能地扩展，填满整个单元格
                                                             
                                                             
# 将按钮放置在最上方
start_button = ttk.Button(frame, text="Start Recording", command=start_recording)
start_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
stop_button = ttk.Button(frame, text="Stop Recording", command=stop_recording)
stop_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)


# 图形显示区域
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

root.mainloop()
