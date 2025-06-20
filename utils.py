# traffic_ovm/utils.py

import numpy as np
from model import optimal_velocity_normal

# Tính current: J = (1/N) * sum(v)
def compute_current(v):
    return np.mean(v)

# Tính density: rho = N / L
def compute_density(N, L):
    return N / L

# Tính headway: delta_xi = xi+1 - xi (có chu kỳ)
def compute_headways(x, L):
    x_sorted = np.sort(x)
    dx = np.diff(np.concatenate((x_sorted, [x_sorted[0] + L])))
    return dx, x_sorted

# Phát hiện vùng jam: đoạn liên tục có v_i < threshold (ví dụ 1.0)
def compute_jam_length(x, v, threshold, L):
    x_sorted_idx = np.argsort(x)
    x_sorted = x[x_sorted_idx]
    v_sorted = v[x_sorted_idx]

    in_jam = v_sorted < threshold
    jam_regions = []
    jam_len = 0.0

    start = None
    for i in range(len(in_jam)):
        if in_jam[i]:
            if start is None:
                start = i
        else:
            if start is not None:
                end = i
                length = x_sorted[end - 1] - x_sorted[start]
                jam_regions.append(length)
                jam_len += length
                start = None

    # Nếu jam kéo dài đến cuối mảng
    if start is not None:
        length = (x_sorted[-1] + (L - x_sorted[-1] + x_sorted[0])) % L
        jam_regions.append(length)
        jam_len += length

    return jam_len, jam_regions

# Hàm lý thuyết: J = V(delta_x) / delta_x
def get_theoretical_current_fn(v_max, x_c, a):
    def J(dx):
        v = optimal_velocity_normal(dx, v_max, x_c, a)
        return v / dx
    return J
