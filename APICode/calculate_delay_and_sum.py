import numpy as np

def calculate_delay_and_sum(data, mic_positions, RATE):
    theta_range = np.linspace(-50, 50, 101) * np.pi / 180
    phi_range = np.linspace(-50, 50, 101) * np.pi / 180
    intensity_map = np.zeros((len(theta_range), len(phi_range)))
    threshold = 1000

    # 预计算 sin(theta) 和 cos(theta) * sin(phi)
    sin_theta = np.sin(theta_range).reshape(-1, 1)  # (101, 1)
    cos_theta_sin_phi = (np.cos(theta_range).reshape(-1, 1) * np.sin(phi_range)).T  # (101, 101)

    # 计算延迟矩阵： (2, 101, 101) -> 每个 theta, phi 对应的延迟向量
    delays = np.array([sin_theta, cos_theta_sin_phi])  # (2, 101, 101)
    delays = np.einsum('ijk,jl->ikl', delays, mic_positions) / 343  # (mic数量, 101, 101)

    # 向量化信号移位
    delays_in_samples = (delays * RATE).astype(int)  # 延迟转为采样点
    shifted_signals = np.array([np.roll(data, shift, axis=0) for shift in delays_in_samples])  # (mic数量, 101, 101, 样本数)

    # 求和并计算强度
    summed_signals = np.sum(shifted_signals, axis=0)  # (101, 101, 样本数)
    intensity = np.max(np.abs(summed_signals), axis=-1)  # 计算强度 (101, 101)

    # 阈值判断
    intensity_map[intensity > threshold] = intensity[intensity > threshold]

    return intensity_map, theta_range, phi_range
