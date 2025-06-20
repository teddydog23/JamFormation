# traffic_ovm/model.py

import numpy as np

# ===== Hàm vận tốc tối ưu =====

# Vùng thường (có hệ số a)
def optimal_velocity_normal(delta_x, v_max, x_c, a):
    return 0.5 * v_max * (np.tanh(a * (delta_x - x_c)) + np.tanh(a * x_c))

# Vùng slowdown (ngầm định a = 1)
def optimal_velocity_slowdown(delta_x, v_max, x_c):
    return 0.5 * v_max * (np.tanh(delta_x - x_c) + np.tanh(x_c))

# ===== Hàm kiểm tra giới hạn tốc độ hiện tại =====

def get_speed_limit(pos, sections, v_f_max):
    """
    Trả về (v_max, is_slowdown) tương ứng với vị trí hiện tại
    """
    for zone in sections['slowdowns']:
        if zone['start'] <= pos <= zone['end']:
            return zone['v_max'], True
    return v_f_max, False

# ===== Hàm gia tốc chính =====

def acceleration(x, v, idx, sections, a, v_f_max, x_c):
    N = len(x)
    L = sections['L']
    
    # Tính delta_x với điều kiện tuần hoàn
    delta_x = x[(idx + 1) % N] - x[idx]
    if delta_x < 0:
        delta_x += L

    pos = x[idx] % L
    v_max, is_slowdown = get_speed_limit(pos, sections, v_f_max)

    if is_slowdown:
        V_opt = optimal_velocity_slowdown(delta_x, v_max, x_c)
    else:
        V_opt = optimal_velocity_normal(delta_x, v_max, x_c, a)

    return a * (V_opt - v[idx])
