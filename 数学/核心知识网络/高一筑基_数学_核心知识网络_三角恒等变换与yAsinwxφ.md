# 三角恒等变换与 $y = A\sin(\omega x + \varphi)$

| 字段 | 内容 |
|------|------|
| **来源** | 53科学备考《高中知识清单》数学知识图谱 / 人教A版必修第一册第五章 |
| **时间标签** | #高一筑基 |
| **难度** | ★★★★☆ |
| **状态** | ⚠️待强化 |
| **试卷来源** | #新高考Ⅰ卷·广东 |
| **广东考情** | 考查频率：高频；难度：中档~中高档；三角恒等变换是三角大题第一问的标配，辅助角公式是化简的核心工具 |

---


![三角函数变换](../../图形库/数学/三角函数变换.png)

## 核心内容

### 一、两角和与差的三角函数公式
- $\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta$（$S_{(\alpha+\beta)}$）
- $\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta$（$S_{(\alpha-\beta)}$）
- $\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta$（$C_{(\alpha+\beta)}$）
- $\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta$（$C_{(\alpha-\beta)}$）
- $\tan(\alpha + \beta) = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta}$（$T_{(\alpha+\beta)}$）
- $\tan(\alpha - \beta) = \frac{\tan\alpha - \tan\beta}{1 + \tan\alpha\tan\beta}$（$T_{(\alpha-\beta)}$）

### 二、二倍角公式
- $\sin 2\alpha = 2\sin\alpha\cos\alpha = \frac{2\tan\alpha}{1 + \tan^2\alpha}$
- $\cos 2\alpha = \cos^2\alpha - \sin^2\alpha = 2\cos^2\alpha - 1 = 1 - 2\sin^2\alpha$
- $\tan 2\alpha = \frac{2\tan\alpha}{1 - \tan^2\alpha}$

### 三、降幂公式（升角公式）
- $\sin^2\alpha = \frac{1 - \cos 2\alpha}{2}$
- $\cos^2\alpha = \frac{1 + \cos 2\alpha}{2}$

### 四、辅助角公式
$$a\sin x + b\cos x = \sqrt{a^2 + b^2}\sin(x + \varphi)$$
其中 $\tan\varphi = \frac{b}{a}$（注意 $a, b$ 符号决定 $\varphi$ 所在象限）

**常见形式**：
- $\sin x \pm \cos x = \sqrt{2}\sin(x \pm \frac{\pi}{4})$
- $\sqrt{3}\sin x \pm \cos x = 2\sin(x \pm \frac{\pi}{6})$
- $\sin x \pm \sqrt{3}\cos x = 2\sin(x \pm \frac{\pi}{3})$

### 五、三角恒等变换策略
1. **角的关系**：拆角、凑角、倍角、半角
2. **名的关系**：弦化切、切化弦（齐次式）
3. **式的关系**：降幂、升幂、辅助角公式统一
4. **"1"的代换**：$1 = \sin^2\alpha + \cos^2\alpha = \tan\frac{\pi}{4}$

---

## 题型识别标志

> **看到什么条件 → 立刻想到什么方法**

| 题干关键条件 | 识别为 | 首选方法 |
|-------------|--------|----------|
| "已知 $\sin(\alpha-\beta)$、$\cos\alpha\sin\beta$，求 $\cos(2\alpha+2\beta)$" | 和差角+倍角 | 先求 $\sin(\alpha+\beta)$，再用 $\cos2x=1-2\sin^2x$ |
| "化简三角式求值" | 恒等变换 | 和差、倍角、降幂、辅助角依次使用 |
| "出现 $\sin A\cos B\pm\cos A\sin B$" | 和差公式 | 逆用 $\sin(A\pm B)$ |
| "已知两角和与差的正弦/余弦" | 配角 | 用 $\alpha=(\alpha-\beta)+\beta$ 等关系配角 |
| "化简到 $A\sin(\omega x+\varphi)$" | 辅助角 | $\sqrt{a^2+b^2}\sin(x+\varphi)$ |
| "求周期/单调区间/最值" | 图象性质 | 先化简成标准型，再整体代入 |

## 解题路径（三角恒等变换求值四步法）

> 650分导向：给值求值的核心是"变角"——把所求角用已知角表示，避免硬算。

### 第一步：看所求
明确目标角与已知角的关系，确定配角路线（如 $\alpha+\beta=(\alpha-\beta)+2\beta$ 等）。

### 第二步：选公式
和差角、倍角、降幂、辅助角按需组合。

### 第三步：代已知
将已知数值代入，求出中间量（如 $\sin(\alpha+\beta)$）。

### 第四步：得结论
用二倍角等收口，注意符号与取值范围。

## 母题（2023 新课标Ⅰ卷·第8题，5分）

> 广东考生真题。由和差角求中间量、再用二倍角收口，是三角恒等变换的标准流程。

**题目**：已知 $\sin(\alpha-\beta)=\dfrac{1}{3}$，$\cos\alpha\sin\beta=\dfrac{1}{6}$，则 $\cos(2\alpha+2\beta)=$（ ）

A. $\dfrac{7}{9}$　B. $\dfrac{1}{9}$　C. $-\dfrac{1}{9}$　D. $-\dfrac{7}{9}$

**解**：
由 $\sin(\alpha-\beta)=\sin\alpha\cos\beta-\cos\alpha\sin\beta=\frac{1}{3}$，且 $\cos\alpha\sin\beta=\frac{1}{6}$，得
$$\sin\alpha\cos\beta=\frac{1}{3}+\frac{1}{6}=\frac{1}{2}$$

于是
$$\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta=\frac{1}{2}+\frac{1}{6}=\frac{2}{3}$$

故
$$\cos(2\alpha+2\beta)=1-2\sin^2(\alpha+\beta)=1-2\times\frac{4}{9}=\frac{1}{9}$$

**答**：选 B。

---

## 自测训练（3道·覆盖恒等变换核心公式）

> 先独立完成，再展开卡片末尾「参考答案」核对。每题标注所检验的知识点，方便对号查漏。

**第1题**（检验 二倍角公式 + 半角公式）

已知 $\cos\alpha = -\dfrac{3}{5}$，$\alpha \in \left(\dfrac{\pi}{2}, \pi\right)$，求 $\cos 2\alpha$ 和 $\sin\dfrac{\alpha}{2}$ 的值。

**第2题**（检验 和差角公式 + 配角法）

已知 $\alpha,\beta$ 均为锐角，$\cos\alpha = \dfrac{4}{5}$，$\cos(\alpha+\beta) = \dfrac{5}{13}$，求 $\cos\beta$ 的值。

**第3题**（检验 辅助角公式 + 标准型性质）

化简 $f(x) = \sin 2x - \sqrt{3}\cos 2x$ 为 $A\sin(\omega x+\varphi)$ 的形式，并求其最小正周期和值域。

---

## 关联卡片

- [三角函数的概念与诱导公式](高一筑基_数学_核心知识网络_三角函数的概念与诱导公式.md) — 恒等变换的基础工具
- [三角函数的图象与性质](高一筑基_数学_核心知识网络_三角函数的图象与性质.md) — 化简后分析图象性质

---


- [【卡片标题】三角函数与解三角形大题](../典型题型与方法/高二深化_数学_典型题型与方法_三角函数与解三角形大题.md)

- [三角的概念与诱导公式](高一筑基_数学_核心知识网络_三角的概念与诱导公式.md)
## 备注
- 易错点：辅助角公式中 $\tan\varphi = \frac{b}{a}$，注意 $\varphi$ 的象限由 $a, b$ 共同决定，不是仅由 $\frac{b}{a}$ 决定
- 三角大题化简的标准路径：诱导公式 $\rightarrow$ 和差/倍角展开 $\rightarrow$ 降幂 $\rightarrow$ 辅助角公式 $\rightarrow$ $y = A\sin(\omega x + \varphi)$ 形式
- 广东卷常考：给定三角函数式化简后求周期、单调区间、最值

---

## 参考答案

> 答案与题目分板块呈现，便于"先做后对"。每题给出规范解答 + 易错提醒，做完一题对一题。

<details>
<summary>▶ 第1题详解（二倍角公式 + 半角符号判定）</summary>

**(1)** 由二倍角公式：
$$\cos 2\alpha = 2\cos^2\alpha - 1 = 2\cdot\dfrac{9}{25} - 1 = \dfrac{18}{25} - 1 = -\dfrac{7}{25}$$

**(2)** $\alpha \in \left(\dfrac{\pi}{2}, \pi\right)$，故 $\dfrac{\alpha}{2} \in \left(\dfrac{\pi}{4}, \dfrac{\pi}{2}\right)$（第一象限），$\sin\dfrac{\alpha}{2} > 0$。

$$\sin\dfrac{\alpha}{2} = \sqrt{\dfrac{1-\cos\alpha}{2}} = \sqrt{\dfrac{1-(-\frac{3}{5})}{2}} = \sqrt{\dfrac{\frac{8}{5}}{2}} = \sqrt{\dfrac{4}{5}} = \dfrac{2\sqrt{5}}{5}$$

**答**：$\cos 2\alpha = -\dfrac{7}{25}$，$\sin\dfrac{\alpha}{2} = \dfrac{2\sqrt{5}}{5}$。

> **易错提醒**：半角公式必须先判 $\dfrac{\alpha}{2}$ 所在象限以定符号——$\alpha$ 在第二象限时 $\dfrac{\alpha}{2}$ 在第一象限，$\sin\dfrac{\alpha}{2}$ 取正。

</details>

<details>
<summary>▶ 第2题详解（配角法 + 象限符号判定）</summary>

$\alpha$ 锐角，$\cos\alpha = \dfrac{4}{5}$，故 $\sin\alpha = \sqrt{1-\dfrac{16}{25}} = \dfrac{3}{5}$。

$\alpha,\beta$ 均锐角 $\Rightarrow 0 < \alpha+\beta < \pi$；又 $\cos(\alpha+\beta) = \dfrac{5}{13} > 0$，故 $\alpha+\beta \in \left(0, \dfrac{\pi}{2}\right)$，$\sin(\alpha+\beta) = \sqrt{1-\dfrac{25}{169}} = \dfrac{12}{13}$。

配角：$\beta = (\alpha+\beta) - \alpha$，
$$\begin{aligned}
\cos\beta &= \cos[(\alpha+\beta)-\alpha] \\
&= \cos(\alpha+\beta)\cos\alpha + \sin(\alpha+\beta)\sin\alpha \\
&= \dfrac{5}{13}\cdot\dfrac{4}{5} + \dfrac{12}{13}\cdot\dfrac{3}{5} \\
&= \dfrac{20}{65} + \dfrac{36}{65} = \dfrac{56}{65}
\end{aligned}$$

**答**：$\cos\beta = \dfrac{56}{65}$。

> **易错提醒**：必须先判定 $\alpha+\beta$ 落在第几象限（此处 $\cos(\alpha+\beta)>0$ 说明在第一象限），否则 $\sin(\alpha+\beta)$ 的符号会错。

</details>

<details>
<summary>▶ 第3题详解（辅助角公式 + 标准型性质）</summary>

提取系数 $1$ 和 $-\sqrt{3}$：
$$f(x) = \sin 2x - \sqrt{3}\cos 2x = 2\!\left(\dfrac{1}{2}\sin 2x - \dfrac{\sqrt{3}}{2}\cos 2x\right)$$

由辅助角公式（$\tan\varphi = \dfrac{-\sqrt{3}}{1} = -\sqrt{3}$，$a=1>0, b=-\sqrt{3}<0$，$\varphi$ 在第四象限）：
$$f(x) = 2\sin\!\left(2x - \dfrac{\pi}{3}\right)$$

- 最小正周期：$T = \dfrac{2\pi}{2} = \pi$
- 值域：$[-2, 2]$

**答**：$f(x) = 2\sin\!\left(2x - \dfrac{\pi}{3}\right)$，$T = \pi$，值域 $[-2, 2]$。

> **易错提醒**：辅助角公式中 $\varphi$ 的象限由 $a, b$ 共同决定。此处 $a=1>0, b=-\sqrt{3}<0$，$\varphi = -\dfrac{\pi}{3}$（不能直接写成 $+\dfrac{\pi}{3}$）。

</details>
