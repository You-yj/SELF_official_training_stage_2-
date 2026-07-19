#import numpy as np
from fealpy.backend import backend_manager as bm

# 原函数 f(x) = x^3 - 3x + 1
def f(x):
    return x**3 - 3 * x + 1
# 原函数导数 f'(x)
def df(x):
    return 3 * x**2 - 3
# 扰动函数 f_ε(x) = f(x) + ε·g(x)
def f_eps(x, eps, g):
    return f(x) + eps * g(x)
# 扰动导数 f'_ε(x) = f'(x) + ε·g'(x)
def df_eps(x, eps, g, dg):
    return df(x) + eps * dg(x)


# 牛顿法求解
def newton(x0, eps, g, dg, tol=1e-14, max_iter=200):
    x = x0
    iter_cnt = 0
    for _ in range(max_iter):
        fx = f_eps(x, eps, g)
        dfx = df_eps(x, eps, g, dg)
        dx = -fx / dfx
        x = x + dx
        iter_cnt += 1
        if bm.abs(dx) < tol:
            break
    return x, iter_cnt


# 二分法求解
def bisection(a, b, eps, g, dg, tol=1e-14, max_iter=200):
    fa = f_eps(a, eps, g)
    fb = f_eps(b, eps, g)
    if fa * fb > 0:
        raise ValueError(f"区间[{a}, {b}]两端函数值同号，无保证根")
    iter_cnt = 0
    while (b - a) > tol and iter_cnt < max_iter:
        c = (a + b) / 2.0
        fc = f_eps(c, eps, g)
        if fa * fc <= 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        iter_cnt += 1
    root = (a + b) / 2.0
    return root, iter_cnt



# 扰动函数1：g(x)=x
def g1(x):
    return x
def dg1(x):
    return 1.0

# 扰动函数7：g(x)=sin(x)（弧度）
def g7(x):
    return bm.sin(x)
def dg7(x):
    return bm.cos(x)

# ========== 预计算所有 ε=0 基准根 ==========
root1_0, _ = bisection(1, 2, 0.0, g1, dg1)
root2_0, _ = newton(1.3, 0.0, g1, dg1)
root5_0, _ = bisection(0, 1, 0.0, g1, dg1)
root6_0, _ = bisection(-2, -1, 0.0, g1, dg1)
root7_0, _ = newton(0.3, 0.0, g7, dg7)

# ========== Case 1 ==========
eps1 = 1e-6
x1_eps, _ = bisection(1, 2, eps1, g1, dg1)
dx_obs1 = abs(x1_eps - root1_0)
dx_pred1 = abs(eps1 * g1(root1_0) / df(root1_0))

# ========== Case 2 ==========
eps2 = 1e-6
x2_eps, _ = newton(1.3, eps2, g1, dg1)
dx_obs2 = abs(x2_eps - root2_0)
dx_pred2 = abs(eps2 * g1(root2_0) / df(root2_0))

# ========== Case 3 ==========
x3_0, N3 = newton(0.2, 0.0, g1, dg1)
dx3 = abs(x3_0 - root2_0)

# ========== Case 4 ==========
x4_0, N4 = bisection(1.1, 2.0, 0.0, g1, dg1)
dx4 = abs(x4_0 - root1_0)

# ========== Case 5 ==========
eps5 = 1e-6
x5_eps, _ = bisection(0, 1, eps5, g1, dg1)
dx_obs5 = abs(x5_eps - root5_0)
dx_pred5 = abs(eps5 * g1(root5_0) / df(root5_0))

# ========== Case 6 ==========
eps6 = 1e-6
x6_eps, _ = bisection(-2, -1, eps6, g1, dg1)
dx_obs6 = abs(x6_eps - root6_0)
dx_pred6 = abs(eps6 * g1(root6_0) / df(root6_0))

# ========== Case 7 ==========
eps7 = 1e-12
x7_eps, _ = newton(0.3, eps7, g7, dg7)
dx_obs7 = abs(x7_eps - root7_0)
dx_pred7 = abs(eps7 * g7(root7_0) / df(root7_0))

# 题目要求输出顺序
output = [
    dx_obs1, dx_pred1,
    dx_obs2, dx_pred2,
    dx3, N3,
    dx4, N4,
    dx_obs5, dx_pred5,
    dx_obs6, dx_pred6,
    dx_obs7, dx_pred7
]

output_str = f"[{','.join(map(str, output))}]"
print(output_str)
