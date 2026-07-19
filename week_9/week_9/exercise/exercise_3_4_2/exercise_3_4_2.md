**问题**: 考虑函数 $f(x) = \begin{cases}\dfrac{\sin x}{x}, x \neq 0, \\ 1, x = 0.\end{cases}$，弧度为单位。本题旨在研究当 $x$ 很小时，使用标准浮点运算计算 $f(x)$ 所产生的有效数字损失问题，并设计一种数值稳定的替代方法，以精确捕捉微小的减量 $d(x) = 1 - f(x)$。

从以下基本依据出发：
- 关于 $x = 0$ 的正弦函数的泰勒级数： $\sin x = x - \dfrac{x^{3}}{3!} + \dfrac{x^{5}}{5!} - \cdots$ 
- 由 $f(x)$ 导出的级数及其相关的减量 $d(x)$：$f(x) = 1 - \dfrac{x^{2}}{3!} + \dfrac{x^{4}}{5!} - \cdots,\ d(x) = 1 - f(x) = \dfrac{x^{2}}{3!} - \dfrac{x^{4}}{5!} + \dfrac{x^{6}}{7!} - \cdots$  
- 标准浮点模型：对于基本运算 $\circ \in \{+,-,\times,\div\}$，$\mathbf{fl}(a \circ b) = (a \circ b)(1 + \delta)$，其中 $|\delta| \le u$，$u$ 是工作精度的单位舍入误差。

---

**任务 1**：

论证：为何当 $x$ 很小时，直接计算 $\mathbf{fl}(\sin x)/\mathbf{fl}(x)$ 对于 $f(x)$ 具有较小的相对误差，但在形成 $1 - \mathbf{fl}(\sin x)/\mathbf{fl}(x)$ 时，会由于相减抵消而完全丢失关于减量 $d(x)$ 的信息。推导出一个用 $u$ 表示的阈值尺度，在该尺度下，朴素计算法无法可靠地解析 $d(x)$（以 $u$ 的渐近形式表示该阈值）。

**证明**：

假设 $x$ 是精确浮点数，即 $x$ 本身是机器可精确表示的浮点数，即 $\mathbf {fl}(x)=x$，此时不存在舍入误差；

令 $\hat f(x)$ 为 $f(x)$ 的计算值； $\hat d(x)$ 为 $1-f(x)$ 的计算值。

- 计算 $f(x)$ 时的误差：
  $$
  \begin{aligned}
  \hat f(x) =& \mathbf{fl}\left( \dfrac{\mathbf{fl}(\sin x)}{\mathbf{fl}(x)} \right) =  \mathbf{fl}\left( \dfrac{\mathbf{fl}(\sin x)}{x} \right) = \dfrac{\sin x}{x}(1+\delta_1)(1+\delta_2) \\
  =& \dfrac{\sin x}{x} (1+\delta_1 + \delta_2 + \delta_1 \delta_2 ) \approx \dfrac{\sin x}{x} (1+\delta_1 + \delta_2) = f(x)(1+\delta_1 + \delta_2)
  \end{aligned}
  $$
  其中 $\approx$ 是展开乘积并舍弃二阶小量的结果； $|\delta_1|, |\delta_2| \le u$，故计算 $f(x)$ 的总相对误差为
  $$
  \left| \dfrac{\hat f(x) - f(x)}{f(x)} \right| \approx |\delta_1 + \delta_2| \le |\delta_1| + |\delta_2| \le 2u
  $$

  这个相对误差很小，量级与单位舍入误差 $u$ 相当，因此，直接计算 $f(x)$ 在其整个定义域内都是数值稳定的。

- 计算 $1-f(x)$ 时的误差：
  $$
  \begin{aligned}
  \hat d(x) =& \operatorname{fl}\big(1-\hat f(x)\big)= \big(1-\hat f(x)\big)(1+\delta_3) \approx  \big(1-f(x)\big)(1+\delta_1 + \delta_2))(1+\delta_3) \\
  =& \big(1-f(x) + f(x)(\delta_1 + \delta_2)\big)(1+\delta_3) = \big(d(x) + f(x)(\delta_1 + \delta_2)\big)(1+\delta_3) \\
  =& d(x) + f(x)(\delta_1 + \delta_2) + d(x)\delta_3 + f(x)(\delta_1 + \delta_2)\delta_3 \\
  \approx & d(x) + f(x)(\delta_1 + \delta_2) + d(x)\delta_3
  \end{aligned}
  $$
  其中 $\approx$ 是展开乘积并舍弃二阶小量的结果； $|\delta_3| \le u$，故计算 $d(x)$ 的总相对误差为

  $$
  \left| \dfrac{\hat d(x) - d(x)}{d(x)} \right| \approx \left| \dfrac{f(x)(\delta_1 + \delta_2) + d(x)\delta_3}{d(x)} \right| = \left| \dfrac{f(x)}{d(x)}(\delta_1 + \delta_2) + \delta_3 \right|
  $$

  当 $x$ 非常非常小时, $f(x) \approx 1$, $\ d(x) \approx x^2 / 6$，误差由第一项主导，故

  $$
  \left| \dfrac{\hat d(x) - d(x)}{d(x)} \right| \approx \left| \dfrac{f(x)}{d(x)} (\delta_1 + \delta_2) \right| \approx \dfrac{6}{x^2} | \delta_1 + \delta_2 | \lesssim \dfrac{12u}{x^2}
  $$

  当这个相对误差达到 $1$ 的量级或更大时，朴素计算变得不可靠。令 $12u / x^2 \approx 1$ 得到阈值 $|x| \approx \sqrt{12u}$ 

  > 对于双精度运算，$u = 2^{-53} \approx 1.11 \times 10^{-16}$，阈值 $|x| \approx 3.65 \times 10^{-8}$。对于小于等于此尺度的 $|x|$ 值，$d(x)$ 的朴素计算会丢失其他部分或全部有效数字。该阈值的渐进量级为 $O(\sqrt u)$ 

---

**任务 2**：

设计方法：（一种稳定的、基于级数的求值方法） 

- 对于 $|x|$ 小于一个基于 $u$ 的阈值 $\tau$ 的情况，通过其交错级数计算 $d(x)$ ，然后仅在最后一步使用数值稳定的求和策略形成 $f(x) = 1 - d(x)$ ；

  **核心思路**：规避 $\hat d(x)$ 的灾难性抵消：先直接级数算微小量 $d(x)$，最后一步再 $f=1−d$，仅一次安全减法，无精度丢失。

  已知麦克劳林级数 $d(x) = \frac{x^{2}}{3!} - \frac{x^{4}}{5!} + \frac{x^{6}}{7!} - \cdots = \sum_{k=1}^{\infty} (-1)^{k-1} \frac{x^{2k}}{(2k+1)!}$，交错级数，项快速衰减，截断至满足浮点精度即可。

- 对于 $|x| \ge \tau$ 的情况，使用直接求值 $f(x) = \sin(x)/x$ ；

- 通过返回 $f(0) = 1$ 来处理 $x = 0$ 处的可去奇点。

  对于 $x=0$：将函数作为特殊情况处理，根据定义返回 $f(0)=1$ 和 $d(0)=0$。

稳定性说明：

- 小 x 时不先算 $sinx/x$ 再减 $1$，而是直接展开 $d(x)$ 的多项式，从根源消除相近大数相减；
- 级数每一项都是同阶小量加减，无大幅数值差，累加仅引入 $O(u)$ 累积误差；
- 最后一步 $1−d$ 仅一次减法，且 $d≪1$，不会出现前 $10 +$ 位数字完全重合的灾难性抵消；
- 分段阈值 $τ=\sqrt u$ 是理论最优分界，兼顾精度与计算开销。

---

**任务 3**：实现一个完整的、可运行的程序，该程序要求如下： 
- 主要计算使用标准双精度浮点运算：

  全部浮点计算使用 fealpy 双精度 float64。

- 使用一个基于截断级数的高精度参考值，该级数通过任意精度算术计算，以近似得到具有多位正确数字的 $f(x)$ 和 $d(x)$ 的真实值：

  `decimal`提供高精度参考真值。

- 对于每个测试输入 $x$，计算三个误差度量：
	- 朴素 $f(x)$ 的相对误差：$\left|\dfrac{f_{\text{naive}} - f_{\text{ref}}}{f_{\text{ref}}}\right|$；
	- 朴素减量 $d_{\text{naive}} = 1 - f_{\text{naive}}$ 相对于 $d_{\text{ref}}$ 的相对误差： $\left|\dfrac{d_{\text{naive}} - d_{\text{ref}}}{d_{\text{ref}}}\right|$（如果 $d_{\text{ref}} = 0$，则定义此值为 $0$）；
	- 稳定级数减量 $d_{\text{stable}}$ 相对于 $d_{\text{ref}}$ 的相对误差：$\left|\dfrac{d_{\text{stable}} - d_{\text{ref}}}{d_{\text{ref}}}\right|$（如果 $d_{\text{ref}} = 0$，则定义此值为 $0$）。
	
- 使用弧度，不涉及物理单位。

- 测试集： 对输入 $x \in \{0,\;10^{-12},\;10^{-10},\;10^{-8},\;-10^{-7},\;10^{-7},\;10^{-4},\;10^{-1}\}$ 评估程序。

- 最终输出格式： 生成单行输出，其中包含一个以逗号分隔的列表的列表形式的结果，每个内部列表对应一个测试输入，并按上述顺序包含三个误差度量。例如：`[[e11,e12,e13],[e21,e22,e23],...]`，所有条目均为浮点数。角度单位为弧度，在计算或输出的任何地方都不得使用百分号。

实现步骤：
- 使用 Python 的 decimal 模块对 $f_{\text{ref}}$ 和 $d_{\text{ref}}$ 进行高精度参考计算。

  构造函数`reference_f_d`

- 朴素计算函数，$f_{\text{naive}}(x) = \sin(x)/x$ 和 $d_{\text{naive}}(x)$ = $1 - f_{\text{naive}}(x)$。

  构造函数`naive_f_d`

- 稳定计算函数，该函数实现上述混合算法以找到 $d_{\text{stable}}(x)$。

  构造函数`stable_d`

- 对于测试集中的每个输入 $x$，计算所要求的三个相对误差：$\epsilon_1 = \left|\dfrac{f_{\text{naive}} - f_{\text{ref}}}{f_{\text{ref}}}\right|,\ \epsilon_2 = \left|\dfrac{d_{\text{naive}} - d_{\text{ref}}}{d_{\text{ref}}}\right|,\ \epsilon_3 = \left|\dfrac{d_{\text{stable}} - d_{\text{ref}}}{d_{\text{ref}}}\right|$。

  构造主函数`solve`，

- 对于 $x=0$ 的情况，$d_{\text{ref}}=0$，误差度量 $\epsilon_2$ 和 $\epsilon_3$ 定义为 $0$。

---

代码见：[exercise_3_4_2.py](./exercise_3_4_2.py) 

结果如下：

```
[[0.0,0.0,0.0],[0.0,1.0,1.3775324423698682e-16],[0.0,1.0,1.128474576789396e-16],[0.0,1.0,0.0],[0.0,0.0007992778373590731,0.0007992778373590731],[0.0,0.0007992778373590731,0.0007992778373590731],[1.1102230264755284e-16,5.048554242104574e-08,5.048554242104574e-08],[8.331076721507793e-07,0.0004990319202374923,0.0004990319202374923]]
```





