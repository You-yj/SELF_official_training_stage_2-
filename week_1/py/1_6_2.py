from fealpy.backend import backend_manager as bm
import numpy as np

def simulate_diffusion(L, D, N, T, alpha_target, bc_type, init_func):
    """
    一维扩散前向欧拉仿真
    bc_type: 'reflect' 反射零通量(鬼点) / 'periodic' 周期边界
    init_func(N, L) -> u0 生成初始场
    返回:u_final, mass_initial, mass_final, all_steps_u
    """
    # 1. dx
    if bc_type == "reflect":
        dx = L / (N - 1)
    elif bc_type == "periodic":
        dx = L / N
    else:
        raise ValueError("bc_type must be reflect or periodic")
    
    #  2. 由alpha反求dt，n=ceil(T/dt)，强制n*dt=T精确满足
    dt = alpha_target * (dx ** 2) / D
    n = int(np.ceil(T / dt))
    dt_exact = T / n
    alpha_actual = D * dt_exact / (dx ** 2) if dx > 0 else 0.0

    # 初始场
    u = init_func(N, L)
    mass0 = np.sum(u) * dx
    all_u = [u.copy()]

    for _ in range(n):
        u_next = np.zeros_like(u)
        if bc_type == "reflect":
            # 鬼点策略实现零通量 du/dx=0
            ghost_left = u[1] #u_{-1}=u_1
            ghost_right = u[-2] #u_N=U_{N-2}
            u_full = np.concatenate([[ghost_left], u, [ghost_right]]) 
            u_next = u + alpha_actual * (u_full[2:] - 2 * u_full[1:-1] + u_full[:-2])
        elif bc_type == "periodic":
            # 周期环绕差分
            left = np.roll(u, 1)
            right = np.roll(u, -1)
            u_next = u + alpha_actual * (right - 2 * u + left)
        all_u.append(u_next.copy())
        u = u_next
    mass_final = np.sum(u) * dx
    return u, mass0, mass_final, all_u

# -------------------------- 初始条件构造函数 --------------------------
def init_const(N, L):
    """案例1 恒定场u=3"""
    return 3.0 * np.ones(N, dtype=np.float64)

def init_cosine_k(N, L, k):
    """案例2 周期余弦 u_j=cos(2πkj/N)"""
    j = np.arange(N)
    return np.cos(2 * np.pi * k * j / N)

def init_palindrome_tri(N, L):
    """案例3 回文对称三角形凸起, N奇数"""
    x = np.linspace(0, L, N)
    mid = N // 2
    u = np.zeros(N)
    for i in range(mid + 1):
        val = x[i] if x[i] <= L/2 else L - x[i]
        u[i] = val
        u[N - 1 - i] = val
    return u

def init_case4(N, L):
    """案例4 初始 [1.0,0.0,0.0] N=3"""
    return np.array([1.0, 0.0, 0.0], dtype=np.float64)

# ---------------------------- 容差策略 ----------------------------
EPS_ABS = 1e-10    #比较浮点数量(质量和对称性) 绝对容差
EPS_REL = 1e-9     #比较浮点数量(质量和对称性) 相对容差
EPS_REL_AMP = 1e-8 #比较振幅比  相对容差
def is_close(a, b, rtol=EPS_REL, atol=EPS_ABS):
    """标量浮点相等判断"""
    return abs(a - b) <= atol + rtol * max(abs(a), abs(b))

# -------------------------- 不变量校验工具 --------------------------
def check_mass_conserved(m0, m1):
    """质量守恒布尔"""
    return is_close(m0, m1)

def check_palindrome(u):
    """是否回文对称 u[i] ≈ u[N-1-i]"""
    N = len(u)
    for i in range((N + 1) // 2):
        if not is_close(u[i], u[N - 1 - i]):
            return False
    return True

def calc_amplitude_ratio(u0, un, k, N, n_steps, alpha):
    """周期余弦模态理论振幅比 gk^n, 对比实测振幅比"""
    gk = 1 - 4 * alpha * (np.sin(np.pi * k / N)) ** 2
    theory = gk ** n_steps
    # 提取余弦模态振幅（最大值绝对值）
    amp0 = np.max(np.abs(u0))
    ampn = np.max(np.abs(un))
    measured = ampn / amp0
    return measured, theory

def all_finite(arr):
    """无NaN、无无穷"""
    return np.all(np.isfinite(arr))

def in_initial_range(u, u0):
    """所有值在[min(u0), max(u0)]之间"""
    umin0 = np.min(u0)
    umax0 = np.max(u0)
    return np.all((u >= umin0 - EPS_ABS) & (u <= umax0 + EPS_ABS))

# ============================== 案例1 ==============================
L1, D1, N1, T1, alpha1 = 1.0, 0.1, 64, 0.1, 0.45
u_ref, m0_ref, m_ref, _ = simulate_diffusion(L1, D1, N1, T1, alpha1, "reflect", init_const)
u_per, m0_per, m_per, _ = simulate_diffusion(L1, D1, N1, T1, alpha1, "periodic", init_const)
case1_1 = check_mass_conserved(m0_ref, m_ref)
case1_2 = check_mass_conserved(m0_per, m_per)
case1_3 = np.allclose(u_ref, u_per, rtol=EPS_REL, atol=EPS_ABS)

# ============================== 案例2 ==============================
L2, D2, N2, T2, alpha2, k2 = 1.0, 0.2, 128, 0.05, 0.10, 1
# 周期边界
u2_per, m0_2p, m2p, all2p = simulate_diffusion(L2, D2, N2, T2, alpha2, "periodic", lambda N,L: init_cosine_k(N,L,k2))
n_steps2 = len(all2p) - 1
meas, theo = calc_amplitude_ratio(all2p[0], u2_per, k2, N2, n_steps2, alpha2)
case2_1 = check_mass_conserved(m0_2p, m2p)
case2_2 = is_close(meas, theo, rtol=EPS_REL_AMP)
# 反射边界同参数
u2_ref, m0_2r, m2r, _ = simulate_diffusion(L2, D2, N2, T2, alpha2, "reflect", lambda N,L: init_cosine_k(N,L,k2))
case2_3 = check_mass_conserved(m0_2r, m2r)

# ============================== 案例3 ==============================
L3, D3, N3, T3, alpha3 = 1.0, 0.1, 129, 0.05, 0.45
# 反射
u3_ref, m0_3r, m3r, all3r = simulate_diffusion(L3, D3, N3, T3, alpha3, "reflect", init_palindrome_tri)
case3_1 = check_mass_conserved(m0_3r, m3r)
case3_2 = check_palindrome(u3_ref)
# 周期
u3_per, m0_3p, m3p, all3p = simulate_diffusion(L3, D3, N3, T3, alpha3, "periodic", init_palindrome_tri)
case3_3 = check_palindrome(u3_per)

# ============================== 案例4 ==============================
L4, D4, N4, alpha4 = 1.0, 0.1, 3, 0.5
dx4 = L4 / N4
dt4 = (dx4 ** 2) / (2 * D4)
T4 = 5 * dt4
u4, m0_4, m4, all4 = simulate_diffusion(L4, D4, N4, T4, alpha4, "periodic", init_case4)
all_u4 = np.concatenate(all4)
case4_1 = check_mass_conserved(m0_4, m4)
case4_2 = all_finite(all_u4)
case4_3 = in_initial_range(u4, all4[0])

# 按题目指定顺序汇总结果
results = [
    case1_1, case1_2, case1_3,
    case2_1, case2_2, case2_3,
    case3_1, case3_2, case3_3,
    case4_1, case4_2, case4_3
]
# 输出要求单行 [bool,bool,...]
str_res = [str(b) for b in results]
print("[" + ",".join(str_res) + "]")

