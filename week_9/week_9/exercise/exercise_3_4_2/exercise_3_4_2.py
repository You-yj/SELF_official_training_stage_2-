#import numpy as np
from fealpy.backend import backend_manager as bm
from decimal import Decimal, getcontext

# bm.set_backend("numpy")
# bm.set_backend("pytorch")
# bm.set_default_device('cuda')

def reference_f_d(x_str: str) -> tuple[Decimal, Decimal]:
    if x_str == "0":
        d = Decimal(0)
        f = Decimal(1)
        return f, d
    x = Decimal(x_str)
    x_sq = x * x
    term = x_sq / Decimal(6)
    d_val = term
    while abs(term) > Decimal("1e-80"):
        k = len(str(d_val))
        term *= -x_sq / Decimal((2 * k) * (2 * k + 1))
        d_val += term
    f_val = Decimal(1) - d_val
    return f_val, d_val


def naive_f_d(x: float) -> tuple[float, float]:
    """朴素计算 f(x) = sin(x)/x , d(x) = 1 - f(x)"""
    if x == 0.0:
        return 1.0, 0.0
    f_naive = bm.sin(x) / x
    d_naive = 1 - f_naive
    return f_naive, d_naive


def stable_d(x: float, threshold: float) -> float:
    """稳定的、基于级数的d(x)求解方法"""
    if x == 0.0:
        return 0.0
    if abs(x) < threshold:
        x_sq = x * x
        term = x_sq / 6.0
        d_val = term
        # 最多迭代 15 次，或直到项不再改变
        for k_iter in range(2, 15):
            term *= -x_sq / ((2 * k_iter) * (2 * k_iter + 1))
            d_val_prev = d_val
            d_val += term
            if d_val == d_val_prev:
                break
        return d_val
    else:
        f_val = bm.sin(x) / x
        return 1.0 - f_val

# ---------- 主程序 ----------
def solve():
    getcontext().prec = 50

    test_cases_str = ['0', '1e-12', '1e-10', '1e-8', '-1e-7', '1e-7', '1e-4', '1e-1']
    test_cases_float = [float(x) for x in test_cases_str]
    threshold = 1e-7

    all_results = []
    for x_str, x_float in zip(test_cases_str, test_cases_float):
        # 1. 高精度参考值
        f_ref_dec, d_ref_dec= reference_f_d(x_str)
        d_ref = float(d_ref_dec)
        f_ref = float(f_ref_dec)

        # 2. 朴素计算
        f_naive_val, d_naive_val = naive_f_d(x_float)

        # 3. 稳定计算
        d_stable_val = stable_d(x_float, threshold)

        # 4. 计算相对误差
        if x_float == 0.0:
            err_f_naive = 0.0
            err_d_naive = 0.0
            err_d_stable = 0.0
        else:
            err_f_naive = abs((f_naive_val - f_ref) / f_ref) if f_ref != 0 else 0.0
            if d_ref == 0.0:
                # 理论上 x≠0 时 d_ref 不会为零，但保留逻辑
                err_d_naive = 0.0 if d_naive_val == 0.0 else float('inf')
                err_d_stable = 0.0 if d_stable_val == 0.0 else float('inf')
            else:
                err_d_naive = abs((d_naive_val - d_ref) / d_ref)
                err_d_stable = abs((d_stable_val - d_ref) / d_ref)

        all_results.append([err_f_naive, err_d_naive, err_d_stable])

    # 无空格的紧凑列表字符串
    formatted_results = [f"[{r[0]},{r[1]},{r[2]}]" for r in all_results]
    print(f"[{','.join(formatted_results)}]")

if __name__ == "__main__":
    solve()