from fealpy.backend import backend_manager as bm

def check_energy_monotonic(N, nu, alpha, T_end, initial):
    # 1. 网格与时间参数
    dx = 1.0 / (N - 1)
    dt = alpha * (dx ** 2) / nu
    n_steps = int(bm.floor(T_end / dt))
    eps1 = 1e-12

    # 2. 构造网格点 x_i = i*dx, i=0,1,...,N-1
    x = [i * dx for i in range(N)]

    # 3. 空间网格点x_i=i*dx的初始条件定义
    u = [0.0] * N
    if initial == "sine":
        for i in range(N):
            u[i] = bm.pi * x[i]
            u[i] = bm.sin(u[i])
    elif initial == "highfreq":
        m = bm.floor(0.45 * (N - 1))
        m = max(m, 1)
        for i in range(N):
            u[i] = bm.sin(m * bm.pi * x[i])
    elif initial == "zero":
        u = [0.0] * N
    else:
        raise ValueError("unknown initial type")

    # 边界点设为零
    u[0] = 0.0
    u[-1] = 0.0

    def compute_E(state):
        """计算离散能量 En
           state为当前时间层的全场数值       
        """
        s = 0.0
        for i in range(1, N - 1):
            s += state[i] ** 2
        return dx * s

    E_prev = compute_E(u)

    for _ in range(n_steps):
        u_next = [0.0] * N
        # 更新内部点
        for i in range(1, N - 1):
            u_next[i] = u[i] + alpha * (u[i+1] - 2 * u[i] + u[i-1])
        # 边界保持0
        u_next[0] = 0.0
        u_next[N-1] = 0.0

        E_curr = compute_E(u_next)
        eps2 = eps1 * (1.0 + E_prev)
        # 判断是否违反单调：E_curr > E_prev + eps2
        if E_curr > E_prev + eps2:
            return False
        # 迭代更新
        u = u_next
        E_prev = E_curr
    # 全部时间步均满足单调
    return True

# 定义全部测试用例
test_cases = [
    (41, 0.1, 0.4, 0.1, "sine"),
    (41, 0.1, 0.5, 0.1, "sine"),
    (41, 0.1, 0.6, 0.1, "highfreq"),
    (5, 1.0, 0.5, 0.5, "sine"),
    (21, 0.5, 0.9, 0.1, "zero"),
]

# 批量运行
results = []
for case in test_cases:
    res = check_energy_monotonic(*case)
    results.append(str(res))

# 输出指定单行格式
print("[" + ",".join(results) + "]")