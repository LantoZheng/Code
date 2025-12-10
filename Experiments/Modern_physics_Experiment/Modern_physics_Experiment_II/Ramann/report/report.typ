/*
Conversion Report:

Original LaTeX Packages Found:
- ctex: Used for typesetting Chinese documents. Automatically handled by Typst's excellent CJK support.
- amsmath: Used for mathematical environments and symbols. Replaced by Typst's native mathematical syntax.
- graphicx: Used for including images. Replaced by Typst's native `image()` function.
- geometry: To adjust page margins and paper size. Replaced by Typst's native `set page()` functions.
- hyperref: For clickable links in the table of contents. Typst generates clickable links in the table of contents automatically.
- booktabs: For professional looking tables. Replaced by Typst's native table features which offer good control.
- float: For the [H] float placement specifier. Typst handles figure placement well, often making strict placement like [H] unnecessary. Figure placement is typically managed by Typst's layout engine.
- caption: For better caption handling. Typst's native figure and caption features are used.
- biblatex: For bibliography management. Replaced by the Typst Universe `@preview/bibliography` package. A bibliography file (like .bib) is required. The original hardcoded bibitems are noted as needing conversion or replacement by proper bibliography management with the package.

Typst Package Replacement Scheme:
- ctex: No specific Typst package needed. Typst natively supports Chinese characters and typesetting.
- amsmath: Replaced by Typst's native mathematical syntax.
- graphicx: Replaced by Typst's native `image()` function.
- geometry: Replaced by Typst's native `set page()` function.
- hyperref: Typst's automatic link generation for table of contents is utilized.
- booktabs: Replaced by Typst's native table syntax.
- float: Typst's native figure placement with optional placement hints if needed.
- caption: Typst's native figure caption handling.
- biblatex: Replaced by the `@preview/bibliography` Typst package.

Potential Issues and Considerations:
- The original `\geometry{a4paper, margin=1in}` is converted to `set page(paper: "a4", margin: 1in)`.
- Float placement with `[H]` from `float` is not directly translated. Typst's layout engine handles figure placement. If strict placement is critical, manual layout adjustments might be required, but Typst's default behavior is often sufficient.
- The `thebibliography` environment with hardcoded `\bibitem` entries is converted to the `bibliography` Typst package. _You will need to create a bibliography file (e.g., `references.bib`) and update the `#show: bibliography` call if your bibliography is in a different format or file._ The current conversion assumes the provided bibitem can be roughly translated into a simple entry in a .bib file if needed, but a proper bibliography requires a source file.
- Image files ('图片 1.jpg', '图片 2.png', etc.) and the data file ('data.jpg') must be located in the same directory as the Typst file or a specified path for the document to compile correctly.
- Table formatting might slightly differ from `booktabs`'s default appearance, but standard solid lines are used which are common in Typst.
- `\clearpage` and `\newpage` are translated to `#pagebreak()`.

*/



#set document(title: "激光拉曼光谱", author: "郑晓旸 20211030007\n指导老师： 何聪丽", date: datetime(2025, 5, 21))

#set page(paper: "a4", margin: 1in)
#set text(lang: "zh") // Set language for Chinese typesetting

// Custom caption formatting similar to original
#show figure.caption: {
  block(spacing: 0.65em)[ #counter(figure).display(): #body ]
}

#set par(justify: true)

#set math(indent: 1em)

#title(
  // Title block for styling
  block(height: 1.5em)[#box(text(1.5em, weight: "bold")[激光拉曼光谱])]
)

#author(
  box(text("郑晓旸 20211030007")),
  box(text("指导老师: 何聪丽"))
)

#date(datetime(2025, 5, 21).display("[year]年[month]月[day]日"))

#pagebreak() // Equivalent to \maketitle followed by \newpage

#outline()

#pagebreak() // Equivalent to \newpage


= 实验 {#sec:experiment}

本实验采用半导体激光器泵浦的 $Nd^{3+}$:$YVO_{4}$ 晶体并倍频后到的 532nm 激光作为激发光源, 研究液体样品 $CCl_{4}$ 分子的拉曼光谱。

== 光子计数器阈值设定 {#sec:threshold}

启动计算机后, 先打开激光光谱仪的开关, 再运行拉曼光谱仪的测量程序, 等待光栅初始化完成后, 在阈值窗口测量无光时的暗计数与脉冲幅度的分布曲线。选择合适的阈值, 将其输入到主程序左侧界面的阈值窗口。

== 初步测量拉曼光谱 {#sec:initial_scan}

=== 参数设置 {#sec:params}

工作方式: 波长; 间隔: 0.1nm; 工作范围: 起始波长: 510nm, 终止波长: 560nm; 最大值: 100000, 最小值: 0; 负高压: 8; 域值: 14; 积分时间: 800ms。确认光栅狭缝处于合适宽度。

=== 粗扫 {#sec:rough_scan_procedure}

粗调光路之后, 令单色仪从 510nm 开始单程扫描, 得到初步测量的拉曼光谱。

== 细调光路 {#sec:fine_tuning}

在峰位处定点扫描, 同时调整光路, 使得接收到的散射光强增大, 在电脑图像上表现为光强曲线随时间上升。

再在 532nm 的瑞利散射峰附近和 555nm 的双峰附近反复扫描, 改变狭缝的大小, 直至瑞利散射峰顶端尖锐、双峰尽量高且能分开。

== 精细测量拉曼光谱 {#sec:fine_scan_procedure}

光路优化完成后, 再次从 510nm 至 560nm 扫描, 即可得到精细测量的拉曼光谱。利用自动寻峰功能, 可以快速峰值和峰位信息。

== 退偏度的计算 {#sec:depolarization}

为了定量描述散射光相对入射光偏振态的改变, 我们引入退偏度的概念。定义入射光的传播方向和散射光的观测方向构成的平面为散射平面, 引入符号 $I_\perp(\theta)$ 描述散射光强度, i 和 s 分别表示入射光和散射光的偏振方向相对于散射平面的取向。垂直于散射平面标记为 $\perp$, 平行于散射平面标记为 $\parallel$, 自然光标记为 n。退偏度定义为偏振方向垂直和平行于入射光偏振方向的散射光强之比。

在光路中加上偏振片, 旋转检偏器, 扫描检偏器相互垂直时的两种拉曼散射谱线。计算退偏度, 并记录在 #link(<tab:peak_values2>)[表 2] 中。

== 单光子计数器的进一步研究 {#sec:pmt_further_study}

点击“检索”, 使单色仪光栅处于拉曼光谱的某一峰值附近。在激光开启的情况下, 再次打开阈值窗口, 测量此时的脉冲计数与脉冲幅度的分布曲线, 并与之前的结果作比较。

= 结果与分析讨论 {#sec:results}

== 阈值设定 {#sec:results_threshold}

无光时暗计数与脉冲幅度分布曲线如 #link(<fig:pmt_dark_count>)[图 1] 所示, 此时激光并未开启, 图像中的峰源自光电倍增管的热噪声。选取阈值为 14 以滤去后续测量中热噪声的影响。

#figure(
  image("图片 1.jpg", width: 80%),
  caption: "无光时 PMT 输出的脉冲分布曲线",
) <fig:pmt_dark_count>

== 拉曼光谱的初步测量 {#sec:results_initial_scan}

=== 粗调光路 {#sec:results_rough_adjustment}
1. 先不加偏振片, 打开激光电源, 细调样品架和样品池的位置, 使激光束处于柱形样品池的轴线上。从各水平方向观察, 确认样品处在最佳照射状态。
2. 反复调节成像透镜组的前后位置, 使激光束腰在单色仪狭缝处成像最细最清晰。
3. 调节凹面镜的前后左右和俯仰角, 使被反射的散射光沿激光束腰和在狭缝上的像的中心连线汇聚到样品池中心, 以增加进入单色仪的拉曼散射光强。

=== 光谱粗扫 {#sec:results_spectrogram_scan}

参数设定完成后, 在 510nm-560nm 范围内进行扫描, 得到拉曼光谱的初步测量图像, 如 #link(<fig:rough_scan>)[图 2] 所示。可以看到此时中心的瑞利散射峰非常宽, 说明光路和狭缝还需要进一步调整。

#figure(
  image("图片 2.png", width: 80%),
  caption: "拉曼光谱的初步测量结果",
) <fig:rough_scan>

== 光路的优化 {#sec:optical_path_optimization}

利用“定点”功能测量固定波长的光强随时间的变化, 并在此期间微调光路, 使接收到的散射光增多, 光强变化趋势见 #link(<fig:optimization>)[图 3]。

#figure(
  image("图片 3.png", width: 80%),
  caption: "优化光路使接受到的散射光不断增强",
) <fig:optimization>

接着在 532nm 的中心瑞利散射峰和 555nm 的双峰附近小范围扫描, 调节狭缝的宽度, 使瑞利散射峰顶端尖锐、双峰尽量高且能分开。细锐的瑞利峰和分开的双峰如 #link(<fig:narrow_peaks>)[图 4 和 5] 所示, 此时确定合适的狭缝大小为 0.2mm。

#figure(
  block(
    image("图片 4.png", width: 45%) + h(1em) + image("图片 5.png", width: 45%)
  ),
  caption: [图 4: 细锐的瑞利散射峰 \quad 图 5: 555nm 附近分开的双峰],
) <fig:narrow_peaks>


== 拉曼光谱的精细测量 {#sec:results_fine_scan}

光路优化完成后, 再次从 510nm-560nm 扫描, 得到精细测量的拉曼光谱, 见下图 #link(<fig:fine_scan>)[图 6]。对比 #link(<fig:fine_scan>)[图 6] 和之前粗扫得到的 #link(<fig:rough_scan>)[图 2], 可以看到中心的瑞利散射峰明显变细, 两侧的拉曼散射峰也更为明显。#link(<fig:fine_scan_zoom>)[图 7] 是 #link(<fig:fine_scan>)[图 6] 的局部放大并自动寻峰后的结果, 从中可以更清晰地看到拉曼散射峰。图中明显的峰共有 9 个, 位于中心的瑞利散射线在强度上远高于周围的拉曼散射线。拉曼线的峰位在瑞利线两侧呈对称分布, 强度极弱, 低频一侧 (右侧) 的谱线为 Stokes 线, 高频一侧 (左侧) 的为反 Stokes 线。在 556nm 附近可观察到分开的双峰。峰位和峰高记录在 #link(<tab:peak_values1>)[表 1] 中。

#figure(
  image("图片 6.png", width: 80%),
  caption: "拉曼光谱的精细测量",
) <fig:fine_scan>

#figure(
  image("图片 7.png", width: 80%),
  caption: "拉曼光谱的精细测量(放大并寻峰)",
) <fig:fine_scan_zoom>


#table(
  caption: "峰值和峰位",
  columns: (none, repeat(9, auto)),
  align: center,
  [峰编号], [1], [2], [3], [4], [5], [6], [7], [8], [9],
  hline(),
  [峰位 (nm)], [520.5], [524.6], [527.2], [533.3], [539.4], [542.4], [546.5], [555.7], [556.5],
  hline(),
  [峰值], [26902.8], [30846.4], [41292.3], [-], [71144.9], [72825.7], [94770.7], [19166.1], [18894.0],
) <tab:peak_values1>


== 退偏度的测量 {#sec:results_depolarization}


#figure(
  image("图片 8.png", width: 60%),
  caption: "实验光路示意图",
) <fig:setup>

#figure(
  image("图片 9.png", width: 80%),
  caption: "偏振片分别处于垂直角度时的光谱",
) <fig:polarization_spectra>

#figure(
  image("图片 10.png", width: 80%),
  caption: "偏振片分别处于垂直角度时的光谱 (局部放大)",
) <fig:polarization_spectra_zoom>

退偏度越小, 说明产生散射光的分子振动模式对称性越高。#link(<tab:peak_values2>)[表 2] 中 7 号峰 (546.5nm) 的退偏度最小, 为 0.13, 说明此波长的拉曼散射光对应的 $CCl_{4}$ 分子振动为演示程序中的“模式一”, 4 个 Cl 原子沿它们与中心 C 的连线振动。

#table(
  caption: "峰位和峰高记录以及退偏度的计算",
  columns: (none, repeat(9, auto)),
  align: center,
  [峰编号], [1], [2], [3], [4], [5], [6], [7], [8], [9],
  hline(),
  [峰位 (nm)], [520.5], [524.6], [527.2], [533.3], [539.4], [542.3], [546.7], [555.8], [556.6],
  hline(),
  [$0^\degree$ 时峰高], [1364.0], [2848.6], [3382.5], [586581.1], [5598.1], [5943.5], [2104.1], [1911.5], [1837.5],
  hline(),
  [$90^\degree$ 时峰高], [4228.0], [3608.6], [4811.7], [1387046.8], [7704.4], [7646.0], [15857.0], [2322.4], [2195.5],
  hline(),
  [退偏度], [0.32], [0.79], [0.70], [0.42], [0.73], [0.78], [0.13], [0.82], [0.84],
) <tab:peak_values2>


== 单光子计数器的进一步研究 {#sec:results_pmt_further_study}

令单色仪光栅位于 555.8nm 附近, 再次利用阈值窗口测量此时的脉冲计数与脉冲幅度的分布曲线, 所得图像如 #link(<fig:pmt_light_count>)[11] 所示。对比之前无光条件下的结果, 可以发现曲线的形态出现了较大的差异, 峰宽变宽, 此时的阈值也增大到了 69。

#figure(
  image("图片 11.jpg", width: 80%),
  caption: "有光条件下的脉冲计数与脉冲幅度的分布曲线",
) <fig:pmt_light_count>

= 总结与建议 {#sec:conclusion}

== 总结 {#sec:summary}

本次实验中, 我们用半导体激光器泵浦的 $Nd^{3+}$:$YVO_{4}$ 晶体并倍频后得到的 532nm 激光作为激发光源, 研究了液体样品 $CCl_{4}$ 分子的拉曼光谱。实验中观察到了瑞利散射峰和拉曼光谱, 不断优化光路以得到理想的结果。之后加上了偏振片, 研究了散射光的偏振特性, 并计算了每个峰的退偏度。最后在有光条件下再次打开阈值窗口, 对单光子计数器进行了进一步的研究。


#show: bibliography("references.bib") // Using the bibliography package
// You'll need to create a references.bib file or
// replace this with your actual bibliography source.
// For the single entry provided:
/*
@article{ref:physics_lab,
  author = {北京师范大学物理实验教学中心},
  title = {近代物理实验讲义},
  year = {2016},
  note = {北京: 北京师范大学物理学系}
}
*/
#pagebreak()

= 附录 {#sec:appendix}

#figure(
  image("data.jpg", width: 90%),
  caption: "原始数据",
) <fig:appendix_setup>
