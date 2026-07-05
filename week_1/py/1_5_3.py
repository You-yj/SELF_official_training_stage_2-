import numpy as np

EPS = 1e-9

def make_lab(C, k, alpha):
    # 构造状态矩阵A
    A = np.array([
        [-k / C, 1 / C],
        [-alpha, 0.0]
    ])
    # 求特征值
    eigvals = np.linalg.eigvals(A)
    re_parts = np.real(eigvals)
    
    has_pos = any(r > EPS for r in re_parts)
    has_zero = any(abs(r) <= EPS for r in re_parts)
    all_neg = all(r < -EPS for r in re_parts)
    
    if has_pos:
        return -1
    elif all_neg:
        return 1
    else:
        return 0

# 测试参数集 (C,k,α,T0,Tset)，后两个不影响A，忽略
cases = [
    (10, 2, 1, 293, 295),    # A
    (5, 0, 1, 293, 295),     # B
    (10, 2, 0, 295, 295),    # C
    (10, 2, -0.5, 293, 295), # D
    (1, 0.1, 10, 300, 295)   # E
]

labels = []
for C, k, alpha, T0, Tset in cases:
    lab = make_lab(C, k, alpha)
    labels.append(lab)

print(labels)
