### 平面麦克风矩阵波束成形阵列 ###

import tkinter as tk
from tkinter import ttk                                             # 导入tkinter的GUI组件库用于图形化展示
import pyaudio                                                      # 导入pyaudio库用于音频输入输出的计算
import numpy as np # type: ignore                                   # 导入numpy数组计算库用于矩阵计算
import matplotlib.pyplot as plt                                     # 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # 导入matplotlib嵌入到tkinter的GUI中
from scipy.fftpack import fft                                       # 导入scipy的fft库用于傅里叶变换计算
import time                                                         # 导入时间模块进行时间度统一








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


# 录音参数设定
FORMAT = pyaudio.paInt16    # 设置采样精度为16bit
CHANNELS =8                 # 设置采样通道为8通 
RATE = 44100                # 设置采样率为44.1khz
CHUNK = int(RATE * 0.2)     # 0.2秒
DEVICE_INDEX =1             # 设备编号




### PyAudio对象初始化 ###


# 初始化pyaudio对象
# 作用：创建PyAudio对象，把对象属性赋值给对象p，这样就可以通过p来访问和操作这个对象的方法和属性了

p = pyaudio.PyAudio()
stream = None           # 音频流对象
is_recording = False    # 是否录音








# 实现延迟求和波束成形算法
def calculate_delay_and_sum(data): 
    theta_range = np.linspace(-50, 50, 101) * np.pi / 180          # 角度范围
    phi_range = np.linspace(-50, 50, 101) * np.pi / 180            # 
    intensity_map = np.zeros((len(theta_range), len(phi_range)))
    threshold = 1000                                               # 波形电压值门槛
    




    for i, theta in enumerate(theta_range):                        # 遍历角度范围 
        for j, phi in enumerate(phi_range):                        
            delays = np.array([np.sin(theta), np.cos(theta) * np.sin(phi)])
            delays = np.dot(mic_positions, delays) / 343  # 343m/s为声音速度
            shifted_signals = [np.roll(data[:, k], int(delay * RATE)) for k, delay in enumerate(delays)]
            summed_signal = np.sum(shifted_signals, axis=0)
            intensity = np.max(np.abs(summed_signal))
            if intensity > threshold:
                intensity_map[i, j] = intensity

    return intensity_map, theta_range, phi_range

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

def stop_recording():
    global stream, is_recording
    if is_recording:
        stream.stop_stream()
        stream.close()
        is_recording = False

def update_plot():
    if is_recording:
        data = stream.read(CHUNK)
        frames = np.frombuffer(data, dtype=np.int16).reshape(-1, CHANNELS)

        # 添加波形电压值门槛
        if np.max(np.abs(frames)) > 4000:
            intensity_map, theta_range, phi_range = calculate_delay_and_sum(frames)

            ax1.clear()
            ax1.plot(frames)
            ax1.set_title("Waveform")

            ax2.clear()
            theta_deg = theta_range * 180 / np.pi
            phi_deg = phi_range * 180 / np.pi
            im = ax2.imshow(intensity_map, extent=[phi_deg.min(), phi_deg.max(), theta_deg.min(), theta_deg.max()], aspect='auto', origin='lower')
            # fig.colorbar(im, ax=ax2)
            ax2.set_title("Sound Intensity Distribution")
            ax2.set_xlabel("Phi (degrees)")
            ax2.set_ylabel("Theta (degrees)")

            canvas.draw()

    root.after(100, update_plot)




### GUI界面初始化 ###

root = tk.Tk()                                               # 创建一个窗口对象
root.title("Acoustic Localization")                          # 设置窗口标题




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
