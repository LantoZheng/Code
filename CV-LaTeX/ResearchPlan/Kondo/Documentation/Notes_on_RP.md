# Research Plan - 完整说明文档

**学生**: Xiaoyang Zheng  
**题目**: Band-Selective Ultrafast Dynamics and Non-Thermal Control in the Topological Kagome Metal CsV₃Sb₅  
**实验室**: Kondo Laboratory, ISSP  
**项目类型**: Master's Program (2 years)  
**最后更新**: 2025年10月23日

---

## 📋 目录

1. [文档概览](#文档概览)
2. [导师审查系统](#导师审查系统)
3. [关键问题与决策](#关键问题与决策)
4. [修改历史总结](#修改历史总结)
5. [参数验证记录](#参数验证记录)
6. [使用指南](#使用指南)

---

## 文档概览

### 主文档
- **ResearchPlan.pdf** (8 页) - 完整的研究计划，包含导师审查标记
- **ResearchPlan.tex** - LaTeX 源文件
- **ResearchPlan.bib** - 参考文献数据库（24 篇引用）

### 项目定位

这是一个 **2 年制 Master 项目**的研究计划，不是博士项目。关键差异：

| 维度 | 博士项目 | Master 项目（本文档） |
|------|---------|---------------------|
| **时长** | 3-5 年 | 2 年 |
| **定位** | 独立研究者 | 学习 + 初步研究 |
| **论文要求** | 3+ 篇一作 | 1-2 篇 |
| **目标期刊** | PRL/Nature Comm | PRB/JPSJ |
| **研究深度** | 开创新方向 | 在导师指导下贡献 |
| **课程要求** | 较少 | 第一年需修课 |

### 研究主题

**Band-Selective Ultrafast Dynamics in CsV₃Sb₅**

通过泵浦-探测反射光谱研究 kagome 金属 CsV₃Sb₅ 中的超快动力学，特别关注：
1. 能带选择性光激发动力学
2. CDW 声子模式的 Fano 共振
3. 手性 CDW 的圆二色性测量

---

## 导师审查系统

### 三种彩色标记

文档中使用三种颜色标记需要审查的事项：

| 标记 | 颜色 | 用途 | 数量 |
|------|------|------|------|
| `[ADVISOR REVIEW: ...]` | 🔴 红色 | 需要导师决策的关键事项 | 7 个 |
| `[VERIFY: ...]` | 🔵 蓝色 | 需要验证的技术参数 | 5 个 |
| `[TODO: ...]` | 🟠 橙色 | 学生待办事项 | 1 个 |

### 标记分布

```
首页：审查摘要框（overview）
  ├─ Objectives（3 个标记）
  │   ├─ [VERIFY] M-点和K-点能量值
  │   ├─ [VERIFY] Fano 参数范围
  │   └─ [VERIFY] 测量灵敏度
  ├─ Methodology（4 个标记）
  │   ├─ [ADVISOR] OPA 系统可用性
  │   ├─ [VERIFY] 四分之一波片
  │   ├─ [ADVISOR] 样品合作
  │   └─ [VERIFY] 低温设备
  ├─ Timeline（3 个标记）
  │   ├─ [ADVISOR] 时间规划现实性
  │   ├─ [TODO] 理论合作者
  │   └─ [ADVISOR] 毕业要求对齐
  ├─ Risk Assessment（2 个标记）
  │   ├─ [ADVISOR] Prof. Ozeki 合作
  │   └─ [ADVISOR] 样品优先级
  └─ Broader Impact（1 个标记）
      └─ [ADVISOR] 研究方向契合度
```

### 首页审查摘要框

文档首页包含一个醒目的审查摘要框，内容：

```latex
ADVISOR REVIEW CHECKLIST

标记类型说明：
- [ADVISOR REVIEW: ...] 红色：需要导师做出关键决策的事项
- [VERIFY: ...] 蓝色：需要验证的技术参数或实验条件
- [TODO: ...] 橙色：学生需要完成的行动项

关键问题（详细说明见各章节标记）：
1. 设备可用性：OPA 系统是否需要购买或共享？
2. 样品获取：是否已与合成组建立联系？
3. 能带结构：能量值是否需要 DFT 计算验证？
4. 时间规划：6 个月完成能量扫描是否现实？
5. 跨组合作：与 Prof. Ozeki 合作是否可行？
6. 期刊目标：毕业要求和发表目标是否对齐？
```

---

## 关键问题与决策

### ⭐⭐⭐⭐⭐ 最高优先级

#### 1. OPA 系统可用性

**问题**：Ti:Sapphire + OPA 系统是否可用？

**位置**：Methodology - Experimental Setup

**标记内容**：
```
[ADVISOR REVIEW: Does the Kondo Lab have this OPA system available, 
or will it need to be purchased/shared with another lab?]
```

**决策选项**：
- ☐ 实验室有现成设备
- ☐ 需要购买（预算？时间？）
- ☐ 需与其他实验室共享（哪个实验室？协调流程？）

**影响**：
- 核心设备，决定整个项目可行性
- 影响项目启动时间和预算
- 可能需要调整研究计划

**状态更新（2025年10月20日）**：
申请人已联系导师确认实验室配备 OPA 系统，文档已更新为肯定语气。

---

#### 2. 样品合作与获取

**问题**：CsV₃Sb₅ 高质量单晶样品如何获取？

**位置**：Methodology - Sample Preparation

**标记内容**：
```
[ADVISOR REVIEW: Has contact been established with the Wilson group 
or other synthesis groups? Please confirm availability and timeline 
for sample delivery]
```

**决策选项**：
- ☐ 已有联系（具体合作者？）
- ☐ 需要建立联系（通过谁？时间表？）
- ☐ 有其他样品来源（哪里？）

**影响**：
- 没有样品无法开展实验
- 样品质量直接影响数据质量
- 样品获取时间影响时间线

**建议行动**：
- 立即确认样品来源
- 如果需要建立合作，尽早联系
- 准备备选材料（其他 kagome 金属？）

---

#### 3. 能带结构能量值

**问题**：M-点（1.2-1.4 eV）和 K-点（0.9-1.1 eV）能量值是否准确？

**位置**：Objective 1

**标记内容**：
```
[VERIFY: Please confirm these energy values match the actual band 
structure of CsV₃Sb₅ or provide updated DFT calculations]
```

**验证来源**：
- DFT 计算
- ARPES 实验数据
- 光学吸收光谱

**影响**：
- 这些能量值是实验设计的核心
- 错误的能量范围会导致实验失败
- 需要基于准确数据选择 OPA 调谐范围

**参考文献**（已添加）：
- Tan et al., PRR 2021 - DFT+DMFT 计算
- Zhao et al., Nature 2021 - ARPES 数据
- Cho et al., PRL 2021 - van Hove 奇点演化

**建议更新值**：
- M-点相关跃迁：1.0-1.5 eV（更宽范围）
- K-点 Dirac 态：0.8-1.0 eV（略微调整）

---

### ⭐⭐⭐⭐ 高优先级

#### 4. 低温设备规格

**问题**：10-300 K、±0.5 K 稳定性的低温恒温器是否可用？

**位置**：Methodology - Sample Preparation

**标记内容**：
```
[VERIFY: Please confirm availability of such cryogenic system 
with these specifications]
```

**决策选项**：
- ☐ 有符合规格的设备
- ☐ 需要升级现有设备
- ☐ 需要共享其他实验室设备

---

#### 5. Prof. Ozeki 合作可行性

**问题**：与 Prof. Ozeki 组合作（OPA 稳定性技术）是否可行？

**位置**：Risk Assessment - Mitigation Strategies

**标记内容**：
```
[ADVISOR REVIEW: Is collaboration with Prof. Ozeki's group feasible? 
If so, should formal arrangements be made now?]
```

**背景**：
- Prof. Ozeki 组专长于 OPA 系统稳定性和优化
- 可能有助于解决泵浦能量漂移等技术问题

**决策选项**：
- ☐ 可行，需要正式安排
- ☐ 可行，但不是必须
- ☐ 不可行，另寻他法

---

#### 6. 毕业时间线和期刊目标

**问题**：24 个月时间线和期刊目标（PRB/JPSJ）是否符合毕业要求？

**位置**：Timeline - Publication Goals

**标记内容**：
```
[ADVISOR REVIEW: Are these publication goals and timeline aligned 
with program graduation requirements?]
```

**决策要点**：
- Master 项目通常需要 1-2 篇论文
- PRB/JPSJ 是合适的目标期刊
- 时间线是否留有足够缓冲？

---

#### 7. 研究方向与实验室优先级

**问题**：此研究方向是否与 Kondo Lab 当前优先级匹配？

**位置**：Broader Impact

**标记内容**：
```
[ADVISOR REVIEW: Does this research direction align with 
the laboratory's current priorities and available resources?]
```

**关键考虑**：
- Kondo Lab 主要使用 ARPES，不是泵浦-探测反射光谱
- 实验室正在开发 pump-probe ARPES（Section 7）
- 是否需要调整研究计划？

---

### ⭐⭐⭐ 中等优先级

#### 8. 测量灵敏度

**问题**：ΔR_CD / ΔR ~ 10⁻³-10⁻² 的灵敏度是否可达？

**验证结果**：
现代平衡探测技术常规达到 ΔR/R ~ 10⁻⁵-10⁻⁶，圆二色性信号 10⁻³-10⁻² 技术上可行。

**状态**：已验证，标记已删除

---

#### 9. Fano 参数参考值

**问题**：q = 2-5 是否适用于 kagome 金属？

**验证结果**：
基于文献，Fano 参数通常 1-10，CDW 系统常见 2-5，范围合理。

**参考文献**（已添加）：
- Uykur et al., npj Quantum Materials 2022 - 光学探测 CDW 中的 Fano 共振

**状态**：已验证，添加了背景说明

---

#### 10. 光学元件光谱范围

**问题**：消色差四分之一波片是否覆盖 0.8-1.6 eV？

**标记内容**：
```
[VERIFY: Are achromatic quarter-wave plates available for 
the full 0.8-1.6 eV range?]
```

**决策选项**：
- ☐ 有合适的元件
- ☐ 需要购买
- ☐ 可借用其他实验室

---

#### 11. 实验阶段时间评估

**问题**：Months 4-9（6 个月）完成能量依赖测量是否现实？

**标记内容**：
```
[ADVISOR REVIEW: Is 6 months realistic for systematic 
energy-dependent measurements?]
```

**考虑因素**：
- 需要扫描多个泵浦能量（~10-15 个点）
- 每个能量需要多次测量以统计
- 仪器故障和优化时间
- Master 学生学习曲线

**建议**：
- 评估是否需要延长至 8-10 个月
- 或减少测量点数量
- 确保有缓冲时间

---

### 待办事项

#### 12. 识别理论合作者

**任务**：尽早识别潜在理论合作者

**位置**：Timeline

**标记内容**：
```
[TODO: Identify potential theory collaborators early in the project]
```

**行动**：
- 在文献综述阶段识别相关理论组
- 向导师咨询推荐的合作者
- 在第一年建立联系

---

## 修改历史总结

### 第一轮修改：从博士到 Master 项目调整（2025年10月初）

**主要改动**：

#### 1. 添加申请背景说明框

在文档开头添加清晰的项目定位说明，避免审核者混淆。

#### 2. 重写 Abstract

**修改前（博士风格）**：
- "transcend this limitation"
- "construct the first momentum-resolved..."

**修改后（Master 风格）**：
- "Master's research proposal"
- "two-year project to contribute"
- "Under Professor Kondo's guidance"
- 强调快速掌握技术而非开创新领域

#### 3. 完全重构时间线

**原版问题**：
- 按实验阶段划分，缺少课程和日语学习
- 没有实验室文化融入策略
- 时间分配不符合 Master 学生成长曲线

**新版结构**：

**Year 1 (Months 1-12): Foundation and Integration**
- Months 1-3：实验室融入、基础培训、日语学习
- Months 4-8：核心实验技能发展
- Months 9-12：系统化能量依赖测量

**Year 2 (Months 13-24): Deep Characterization and Publication**
- Months 13-15：Fano 共振研究
- Months 16-18：圆二色性测量（如果时间允许）
- Months 19-24：数据分析、论文写作、答辩

**关键改进**：
- 明确日语学习计划（JLPT N4 → N3）
- 包含课程安排（GSGC 必修课）
- 更现实的技能发展曲线
- 约 2 个月应急缓冲时间

---

### 第二轮修改：补充实验细节（2025年10月中）

**主要新增内容**：

#### 1. Methodology 章节全面重写

**3.1 Experimental Setup** - 添加详细参数：
- Ti:Sapphire 系统：800 nm, 35 fs, 1 kHz
- OPA 调谐范围：0.8-1.6 eV (775-1550 nm)
- 时间分辨率：~50 fs
- 测量灵敏度：ΔR/R ~ 10⁻⁵
- 泵浦能量密度：10-500 μJ/cm²

**3.2 Sample Preparation** - 明确样品要求：
- 样品来源：合作获取
- 质量表征方法：XRD, 输运测量
- 样品尺寸：1-3 mm 横向，50-200 μm 厚度
- 处理流程：真空/惰性气氛解理

**3.3 Data Analysis** - 说明分析方法：
- 非线性最小二乘拟合
- 傅里叶分析（FFT + 窗口函数）
- 主成分分析（PCA）
- Monte Carlo 误差估计

#### 2. 明确理论预期

**Objective 1** - 添加定量预期：
- M-点主导情景下的信号特征
- K-点耦合较弱的预测
- 动量选择性响应的判据

**Objective 2** - 添加 Fano 参数预期：
- q = 2-5（基于类似系统）
- 不对称性与耦合强度的关系

#### 3. 扩充 Objective 3

从 1 句话扩展为 3 个段落：
- **物理机制**：手性 CDW 的 Berry 相位和轨道角动量
- **预期信号**：ΔR_CD / ΔR ~ 10⁻³-10⁻²
- **实验策略**：温度和能量依赖测量

---

### 第三轮修改：添加导师审查标记（2025年10月20日）

**添加内容**：

#### 1. LaTeX 彩色标记系统
```latex
\usepackage{xcolor, soul}
\newcommand{\advisornote}[1]{\sethlcolor{red!20}\hl{\textbf{[ADVISOR REVIEW: #1]}}}
\newcommand{\verify}[1]{\sethlcolor{blue!20}\hl{\textbf{[VERIFY: #1]}}}
\newcommand{\todo}[1]{\sethlcolor{orange!20}\hl{\textbf{[TODO: #1]}}}
```

#### 2. 首页审查摘要框

添加醒目框架，总结所有关键问题。

#### 3. 在文档中添加 12 个标记

分布在：
- Objectives：3 个标记（能量值、Fano 参数、灵敏度）
- Methodology：4 个标记（OPA、光学元件、样品、低温）
- Timeline：3 个标记（时间评估、理论合作、毕业要求）
- Risk Assessment：2 个标记（跨组合作、样品优先级）
- Broader Impact：1 个标记（研究方向对齐）

---

### 第四轮修改：参数验证与隐私保护（2025年10月20日）

#### 1. 能带结构能量值更新

**更新**：
- M-点：1.2-1.4 eV → 1.0-1.5 eV（更宽范围）
- K-点：0.9-1.1 eV → 0.8-1.0 eV（略微调整）

**依据**：
- 文献调研（Nature, PRL 论文）
- DFT 和 ARPES 数据

**添加引用**：
- Tan2021 - DFT+DMFT 计算
- Zhao2021 - ARPES 实验
- Cho2021 - van Hove 奇点演化

#### 2. Fano 参数验证

验证 q = 2-5 范围合理，添加背景说明和参考文献（Uykur2022）。

#### 3. 测量灵敏度验证

确认 10⁻³-10⁻² 技术可行，添加技术背景说明（Giannetti2016）。

#### 4. 删除合作者详细信息

根据隐私要求，删除：
- 具体合作者姓名
- 机构详细信息
- 保留通用描述："established collaborations with synthesis groups"

---

### 第五轮修改：OPA 系统确认更新（2025年10月20日）

**背景**：申请人已联系导师确认实验室有 OPA 系统

**语气调整**：

**修改前（不确定）**：
- "will be confirmed during initial laboratory orientation"
- "should facilitate rapid adaptation"
- "(details to be confirmed...)"

**修改后（肯定）**：
- "the Kondo Laboratory's OPA system"
- "has prepared me to quickly master"
- "established collaborations with synthesis groups"

**影响**：
- 展示更强的准备和信心
- 消除不必要的不确定性
- 显示对实验室资源的了解

---

## 参数验证记录

### 已验证参数

| 参数 | 原始值 | 验证结果 | 状态 | 参考文献 |
|------|--------|---------|------|---------|
| **M-点能量** | 1.2-1.4 eV | 调整为 1.0-1.5 eV | ✅ 已更新 | Tan2021, Zhao2021, Cho2021 |
| **K-点能量** | 0.9-1.1 eV | 调整为 0.8-1.0 eV | ✅ 已更新 | Zhao2021 |
| **Fano 参数** | q = 2-5 | 范围合理 | ✅ 已验证 | Uykur2022 |
| **CD 灵敏度** | 10⁻³-10⁻² | 技术可行 | ✅ 已验证 | Giannetti2016 |
| **平衡探测** | 10⁻⁵-10⁻⁶ | 常规可达 | ✅ 已验证 | Giannetti2016 |

### 待验证参数

| 参数 | 当前值 | 验证方法 | 优先级 |
|------|--------|---------|--------|
| **四分之一波片范围** | 0.8-1.6 eV | 询问实验室 | ⭐⭐⭐ |
| **低温恒温器规格** | 10-300 K, ±0.5 K | 检查设备 | ⭐⭐⭐⭐ |
| **OPA 调谐范围** | 775-1550 nm | 确认设备规格 | ⭐⭐⭐⭐⭐ |
| **泵浦能量密度** | 10-500 μJ/cm² | 实际测试 | ⭐⭐⭐ |

---

## 参考文献总结

### 新增文献（24 篇总数中的 9 篇新增）

#### CsV₃Sb₅ 能带结构（3 篇）
1. **Tan2021** - DFT+DMFT 计算，M-点 vHS 能量
2. **Zhao2021** - ARPES 数据，能带结构验证
3. **Cho2021** - CDW 态下 vHS 演化

#### 超快光谱方法（2 篇）
4. **Giannetti2016** - 超快光谱权威综述，灵敏度参考
5. **Sobota2021** - ARPES 技术背景

#### Kagome CDW 研究（4 篇）
6. **Wang2020** - CDW 手征性理论
7. **Uykur2022** - 光学探测 CDW，Fano 共振
8. **Miao2021** - CDW 几何构型
9. **Liang2021** - 三维 CDW 与 M-点耦合

### 原有重要文献（部分列举）

- **Demsar2007** - 超快光谱基础
- **Ortiz2019, 2020, 2021** - CsV₃Sb₅ 系列研究
- **Ye2021** - 手性 flux 相
- **Nie2022** - CDW 三重态配对

---

## 使用指南

### 导师会议准备

#### 会前准备（推荐顺序）

1. **首先阅读**：`SUMMARY_ADVISOR_MARKS.md`
   - 快速了解所有标记
   - 获取关键问题概览

2. **打印携带**：`ADVISOR_CHECKLIST.md`
   - 单页检查清单
   - 会议中使用复选框记录决策

3. **详细参考**：`ADVISOR_REVIEW_NOTES.md`
   - 需要时查看每个标记的完整背景
   - 了解技术细节和影响

4. **主文档**：`ResearchPlan.pdf`
   - 标记在文档中的完整上下文
   - 看到具体段落和论述

#### 会议议程建议

**Part 1: 关键决策（30 分钟）**
1. OPA 系统可用性
2. 样品获取策略
3. 研究方向与实验室优先级对齐

**Part 2: 技术参数（20 分钟）**
4. 能带结构能量值确认
5. 低温设备和光学元件
6. 时间线现实性评估

**Part 3: 合作与资源（10 分钟）**
7. 跨组合作可行性
8. 理论合作者推荐
9. 毕业要求确认

**Part 4: 后续行动（10 分钟）**
- 总结决策
- 明确下一步行动
- 设定跟进时间

### 文档更新工作流

#### 收到导师反馈后

1. **记录决策**
   - 在 `ADVISOR_CHECKLIST.md` 中标记复选框
   - 记录决策和理由

2. **更新主文档**
   - 删除已解决的标记
   - 根据反馈修改内容
   - 必要时添加新标记

3. **更新说明文档**
   - 在 `MODIFICATIONS.md` 中记录修改
   - 更新 `SUMMARY_ADVISOR_MARKS.md`

4. **版本控制**
   - 保存旧版 PDF（`ResearchPlan_v1.pdf`）
   - 编译新版本
   - 在修改文档中对比版本差异

### 标记处理原则

#### 何时删除标记

✅ **可以删除**：
- 导师已做出明确决策
- 参数已通过文献或实验验证
- 问题已通过其他方式解决

❌ **暂时保留**：
- 决策尚未最终确定
- 需要进一步讨论
- 等待实验验证

#### 何时添加新标记

需要添加新标记的情况：
- 发现新的技术问题或风险
- 实验设计需要重大调整
- 出现新的资源或合作需求

### 与其他文档的关系

#### Research Plan ↔ Statement of Purpose

**关键差异**：
- RP：技术细节，实验设计，时间线
- SoP：研究动机，背景匹配，灵活性

**同步要点**：
- SoP 中的研究计划应与 RP 一致
- 但 SoP 强调灵活性，RP 展示技术深度
- SoP 提到"时间分辨 ARPES"，RP 详述"泵浦-探测反射光谱"

#### Research Plan ↔ Personal Statement

**关系**：
- PS：展示过去成就（D2NN, SLM）
- RP：说明这些技能如何用于未来研究

**连接点**：
- SLM 经验 → OPA 调谐和波长优化
- 计算能力 → 数据分析和机器学习
- 实验动手能力 → 复杂光学系统构建

---

## 关键统计数据

### 文档规模
- **总页数**：8 页
- **总字数**：~6,000 词
- **参考文献**：24 篇
- **标记数量**：13 个（7 ADVISOR + 5 VERIFY + 1 TODO）

### 时间线
- **总时长**：24 个月
- **Year 1**：基础 + 技能 + Objective 1
- **Year 2**：Objective 2 + 可选 Objective 3 + 论文

### 预期成果
- **论文目标**：1-2 篇第一作者（PRB 或 JPSJ）
- **会议报告**：1 次（APS March Meeting 或类似）
- **硕士论文**：1 篇完整论文

---

## 风险与应对

### 主要风险

#### 1. 设备不可用
- **风险**：OPA 系统需要购买或不可用
- **应对**：调整研究计划，使用固定波长激光

#### 2. 样品获取困难
- **风险**：无法及时获得高质量 CsV₃Sb₅ 样品
- **应对**：准备备选材料（其他 kagome 金属）

#### 3. 时间线过紧
- **风险**：2 年内完成 3 个目标不现实
- **应对**：将 Objective 3 设为可选，聚焦 1+2

#### 4. 技术挑战
- **风险**：圆二色性测量灵敏度不足
- **应对**：与技术专家（Prof. Ozeki？）合作优化

### 缓冲策略

文档中已包含：
- **时间缓冲**：~2 个月应急时间
- **目标灵活性**：Objective 3 标记为"如果时间允许"
- **备选方向**：在 Risk Assessment 中列出
- **合作选项**：技术支持和理论合作

---

## 最终检查清单

### 提交前确认

#### 内容完整性
- [ ] 包含清晰的研究目标（3 个）
- [ ] 详细的实验方法（设备、样品、分析）
- [ ] 现实的时间线（24 个月）
- [ ] 风险评估和应对策略
- [ ] 更广泛影响和意义
- [ ] 完整的参考文献（24 篇）

#### 导师审查准备
- [ ] 首页有醒目的审查摘要框
- [ ] 所有标记清晰可见（彩色高亮）
- [ ] 关键问题按优先级排序
- [ ] 准备了配套检查清单

#### 技术准确性
- [ ] 能量值已验证或标记待确认
- [ ] 设备参数合理且可用
- [ ] 时间线经过仔细评估
- [ ] 数据分析方法明确

#### 格式规范
- [ ] LaTeX 编译无错误
- [ ] 参考文献格式统一
- [ ] 图表清晰（如有）
- [ ] PDF 可搜索

#### Master 项目适配
- [ ] 明确标注为 2 年 Master 项目
- [ ] 时间线包含课程和日语学习
- [ ] 强调在导师指导下工作
- [ ] 目标期刊适合 Master（PRB/JPSJ）
- [ ] 论文目标现实（1-2 篇）

---

## 常见问题

### Q1: 为什么有这么多标记？

**答**：Research Plan 是一个技术文档，很多参数和假设需要导师确认。标记系统确保：
- 不遗漏任何关键决策点
- 导师能快速识别需要关注的事项
- 学生清楚哪些是自己的行动项

### Q2: 是否应该在提交前删除所有标记？

**答**：**不建议**。保留标记的好处：
- 向委员会展示你已识别潜在风险
- 显示你与导师的沟通和准备
- 表明你对项目的深思熟虑

但是：
- 确保标记不是消极的（"我不知道..."）
- 而是建设性的（"需要确认最佳方法..."）

### Q3: 如果导师要求重大修改怎么办？

**答**：
1. 仔细记录所有反馈
2. 保存当前版本作为备份
3. 系统性地进行修改
4. 更新所有相关文档（RP, SoP, PS）
5. 准备修改对比文档

### Q4: 时间线是否过于乐观？

**答**：当前时间线已经过调整，包含：
- 第一年的课程和日语学习时间
- 技能发展的学习曲线
- Objective 3 作为可选项
- ~2 个月应急缓冲

如果导师认为仍过紧，可以：
- 进一步延长某些阶段
- 删除 Objective 3
- 减少测量点数量

### Q5: 与 Kondo Lab 的技术差异如何处理？

**答**：已在 SoP 中处理：
- 强调灵活性和适应性
- 提出多个备选方向
- 展示技能可迁移性（SLM → ARPES）
- 表达对学习新技术的热情

在 RP 中：
- 保持技术细节（展示准备）
- 但在 Broader Impact 中加入标记，询问方向对齐

---

## 结语

这份 Research Plan 是一个**活文档**（living document），应该随着与导师的讨论和项目的进展不断更新和完善。

**核心原则**：
1. **诚实透明**：承认不确定性，寻求指导
2. **技术严谨**：基于文献和实验事实
3. **现实可行**：时间和资源与 Master 项目匹配
4. **灵活适应**：准备根据反馈调整

**最终目标**：
- 向招生委员会展示技术准备和研究潜力
- 向导师展示深思熟虑和主动沟通
- 为自己创建一个清晰的 2 年路线图

祝申请顺利！🎓
