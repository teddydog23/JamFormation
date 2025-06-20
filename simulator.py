# traffic_ovm/simulator.py

import numpy as np
from model import acceleration

# Runge-Kutta bậc 4 cho hệ N phương trình
def rk4_step(x, v, dt, acc_fn, sections, a, v_f_max, x_c):
    N = len(x)
    L = sections['L']

    def acc_all(x_, v_):
        return np.array([acc_fn(x_, v_, i, sections, a, v_f_max, x_c) for i in range(N)])

    kx1 = dt * v
    kv1 = dt * acc_all(x, v)

    kx2 = dt * (v + 0.5 * kv1)
    kv2 = dt * acc_all((x + 0.5 * kx1) % L, v + 0.5 * kv1)

    kx3 = dt * (v + 0.5 * kv2)
    kv3 = dt * acc_all((x + 0.5 * kx2) % L, v + 0.5 * kv2)

    kx4 = dt * (v + kv3)
    kv4 = dt * acc_all((x + kx3) % L, v + kv3)

    x_next = (x + (kx1 + 2 * kx2 + 2 * kx3 + kx4) / 6) % L
    v_next = v + (kv1 + 2 * kv2 + 2 * kv3 + kv4) / 6

    return x_next, v_next

# Hàm mô phỏng chính
def simulate(N, steps, dt, acc_fn, x_init, v_init, sections, a, v_f_max, x_c, save_every=1000):
    x, v = x_init.copy(), v_init.copy()
    history = []

    print(f"[SIM] Bắt đầu mô phỏng trong {steps} bước...")
    print(f"[SIM] Số xe: {N} | Độ dài đường: {sections['L']} | save_every: {save_every}")

    for t in range(steps):
        x, v = rk4_step(x, v, dt, acc_fn, sections, a, v_f_max, x_c)

        if t % save_every == 0 or t == steps - 1:
            history.append((x.copy(), v.copy()))
            print(f"[SIM] Bước {t+1}/{steps} đã lưu trạng thái.")

        elif t % (steps // 10) == 0:
            print(f"[SIM] Đang chạy... {t+1}/{steps} ({(t+1)/steps:.0%})")

    print("[SIM] Mô phỏng hoàn tất.")
    return history
