**问题梳理**：

原方程： $f(x) = x^3 - 3x + 1 = 0$，存在**三个单实根**，对任意单根 $x^*$ 满足 $f'(x^*)\neq0$，这是隐函数定理成立的核心前提。

扰动模型： $f_\varepsilon(x) = f(x) + \varepsilon g(x)$，其中 $\varepsilon$ 是一个小的实数参数，$g(x)$ 是一个光滑函数。

核心研究目标：函数微小扰动 $εg(x)$ 会让根偏移多少，量化敏感性（条件数），并区分牛顿法、二分法在扰动下的表现差异。

---

**任务 1**：讨论在单根处根映射 $f \mapsto x^\star$ 的适定性

适定性三要素：解存在、解唯一、解连续依赖输入（此处输入是函数 $f$）。

令 $F(x,\varepsilon)=f(x) + \varepsilon g(x)$，$\varepsilon_0=0$

1. 已知 $F(x^*,\varepsilon_0)=0$，且显然连续
2. $F_x(x,\varepsilon)=3x^2-3+\varepsilon g'(x)$ 连续且在 $(x^*,\varepsilon_0)$ 处均不为 0
3. $F_{\varepsilon}(x,\varepsilon)= g(x)$ 连续

故由隐函数定理可知：

1. 在 $(x^*,\varepsilon_0)$ 某邻域内，方程 $F(x,\varepsilon)=f(x) + \varepsilon g(x)$ 唯一确定了隐函数 $x=x(\varepsilon)$；
2. $x(\varepsilon)$ 在 $\varepsilon_0$ 某邻域内连续且可微

---

**任务 2**：根据函数的加性扰动凭经验估计根的绝对条件数

对恒等式 $f\big(x(\varepsilon)\big) + \varepsilon g\big(x(\varepsilon)\big) = 0$ 关于 $\varepsilon$ 求导：

$$
\begin{align}
\frac{d}{d\varepsilon} \Big[ f\big(x(\varepsilon)\big) + \varepsilon g\big(x(\varepsilon)\big) \Big] &= 0 \\
f'\big(x(\varepsilon)\big) \frac{dx}{d\varepsilon} + g\big(x(\varepsilon)\big) + \varepsilon g'\big(x(\varepsilon)\big) \frac{dx}{d\varepsilon} &= 0
\end{align}
$$
在 $\varepsilon = 0$ 处求值，并注意到 $x(0) = x^\star$，方程简化为：$f'(x^\star) \frac{dx}{d\varepsilon}\bigg|_{\varepsilon=0} + g(x^\star) = 0$ 

解出这个代表根对扰动敏感性的导数，得到：$\frac{dx}{d\varepsilon}\bigg|_{\varepsilon=0} = - \frac{g(x^\star)}{f'(x^\star)}$ 

对于一个小的非零 $\varepsilon$，根的变化量 $\Delta x = x(\varepsilon) - x^\star$ 可以通过一阶泰勒展开来近似：$\Delta x \approx \varepsilon \frac{dx}{d\varepsilon}\bigg|_{\varepsilon=0} = -\varepsilon \frac{g(x^\star)}{f'(x^\star)}$ 

因此，这个预测位移的大小是：$\Delta x_{\text{pred}} = |\Delta x| \approx \left| \frac{\varepsilon g(x^\star)}{f'(x^\star)} \right|$ 

用 $x^\star$ 的数值近似值 $x_0$ 来代替它，该近似值由未扰动方程（$\varepsilon=0$）计算得出。最终得到公式：$\Delta x_{\text{pred}} = \left| \dfrac{\varepsilon\,g(x_0)}{f'(x_0)} \right|$。项 $\left| \frac{g(x_0)}{f'(x_0)} \right|$ 是根相对于扰动 $g(x)$ 的估计绝对条件数。

---

**任务 3**：必须实现这两种求根方法来计算数值近似值。

- 针对 $f_\varepsilon$ 的**牛顿法**，使用 $f_\varepsilon$ 的导数。

  这种迭代方法可以找到实值函数 $h(x)$ 根的越来越好的近似值。迭代由以下公式定义：
  $$
  x_{k+1} = x_k - \frac{h(x_k)}{h'(x_k)}
  $$
  如果初始猜测值 $x_0$ 足够接近一个单根，该方法会二次收敛。我们将把这个方法应用于扰动函数 $h(x) = f_\varepsilon(x) = x^3 - 3x + 1 + \varepsilon g(x)$，使用其导数 $h'(x) = f'_\varepsilon(x) = 3x^2 - 3 + \varepsilon g'(x)$。当绝对步长 $|x_{k+1} - x_k|$ 小于容差 $10^{-14}$ 时，终止。

- 针对 $f_\varepsilon$ 的**二分法**，，在表现出符号变化的指定区间上使用。

  对于一个连续函数 $h(x)$，如果在区间 $[a, b]$ 上 $h(a)$ 和 $h(b)$ 异号，该方法保证收敛。它通过迭代地将区间减半，同时保持根被包围在区间内。在每一步，计算中点 $c = (a+b)/2$。如果 $h(a)h(c)<0$，新区间变为 $[a, c]$，否则变为 $[c, b]$。当区间宽度 $b-a$ 小于容差 $10^{-14}$ 时，终止。

- **案例输出定义**：

  1.  $\varepsilon$ 非零：

     - 计算$\Delta x_{\text{obs}} = \lvert x_\varepsilon - x_0 \rvert$，为观测位移。

       - 其中 $x_\varepsilon$ 是由指定方法计算的 $f_\varepsilon$ 的根；
       -  $x_0$ 是由相同选择规则计算的对应基准根 $f$ 的根。

       > 相同规则是指：相同方法和括号区间，或由初始猜测值决定的相同吸引盆）

     - 计算 $\Delta x_{\text{pred}} = \left| \dfrac{\varepsilon\,g(x_0)}{f'(x_0)} \right|$，为预测的一阶位移大小。

       - 其中 $f'(x) = 3x^2 - 3$ 是在基准根 $x_0$ 处求值的未扰动函数的导数。

  2.  $\varepsilon$ 为零：计算返回的根相对于相应基准根的绝对差，并报告该方法所用的迭代次数。

---

代码见：[exercise_3_6_2.py](./exercise_3_6_2.py)

结果如下：

```
[3.7905275007688033e-07,3.7905268086775384e-07,3.7905275029892493e-07,3.790526808677525e-07,1.1847925309040954,5,4.440892098500626e-16,47,1.3164366663431792e-07,1.3164361454490094e-07,2.4740907633713505e-07,2.4740906632285367e-07,1.2906342661267445e-13,1.2901316783463214e-13]
```





