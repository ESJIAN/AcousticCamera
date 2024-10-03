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