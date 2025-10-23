# Feynman Diagram Drawing Scripts for φ⁴ Theory

这个目录包含两个脚本用于绘制 φ⁴ 理论的真空费曼图。

## 文件说明

### 1. `draw_vacuum_diagram.wls` - Wolfram Language 脚本
使用 Mathematica/Wolfram Language 绘制费曼图。

**使用方法:**
```bash
# 如果已安装 Wolfram Engine 或 Mathematica
wolframscript draw_vacuum_diagram.wls

# 或者直接运行
./draw_vacuum_diagram.wls
```

**输出文件:**
- `phi4_order1_vacuum.pdf` - λ¹ 阶真空图（详细版）
- `phi4_order1_vacuum.png` - λ¹ 阶真空图（PNG 格式）
- `phi4_order1_simple.pdf` - λ¹ 阶真空图（简化版）
- `phi4_order1_simple.png` - λ¹ 阶真空图（简化版 PNG）

### 2. `draw_vacuum_diagram.py` - Python 脚本
使用 matplotlib 绘制费曼图，更容易运行。

**依赖:**
```bash
pip install matplotlib numpy
```

**使用方法:**
```bash
python3 draw_vacuum_diagram.py

# 或者直接运行
./draw_vacuum_diagram.py
```

**输出文件:**
- `phi4_order1_vacuum.pdf` - λ¹ 阶图-8 图
- `phi4_order1_vacuum.png` - λ¹ 阶图-8 图（PNG）
- `phi4_order2_vacuum.pdf` - λ² 阶所有三个图
- `phi4_order2_vacuum.png` - λ² 阶所有三个图（PNG）

## 绘制的费曼图

### Order λ¹（一阶）
- **Figure-Eight Diagram（图-8图）**: 对称因子 S = 8
  - 单个 φ⁴ 顶点
  - 两个自圈传播子

### Order λ²（二阶）
1. **Eyeglass/Spectacles Diagram（眼镜图）**: 对称因子 S = 16
   - 两个顶点通过两条传播子连接
   - 每个顶点有一个自圈

2. **Basketball Diagram（篮球图）**: 对称因子 S = 48
   - 两个顶点通过四条平行传播子连接

3. **Nested/Setting-Sun Diagram（嵌套图）**: 对称因子 S = 4
   - 两个顶点
   - 一条传播子上有气泡插入

## 推荐使用

如果您已安装：
- **Mathematica/Wolfram Engine**: 使用 `.wls` 脚本获得最专业的图形
- **Python + matplotlib**: 使用 `.py` 脚本，更容易安装和运行

## 在 LaTeX 中使用

生成的 PDF 文件可以直接插入到 LaTeX 文档中：

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.5\textwidth]{phi4_order1_vacuum.pdf}
\caption{Order $\lambda^1$ vacuum diagram for $\phi^4$ theory.}
\end{figure}
```

## 注意事项

- 对称因子的计算遵循标准的费曼图规则
- 图中的蓝色线条表示传播子
- 黑点表示相互作用顶点
