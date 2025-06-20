# traffic_ovm/config.py

import numpy as np

# Số lượng xe
N = 500

# Tham số mô hình OVM
v_f_max = 2.0  # Tốc độ tối đa ngoài slowdown
x_c = 2.0      # Turning point
sensitivity = a = 2.5

dt = 1 / 128
steps = 50000