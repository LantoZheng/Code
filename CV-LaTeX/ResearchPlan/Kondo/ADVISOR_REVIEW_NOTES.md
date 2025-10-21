# 导师审查标记说明文档

## 文档概览
已在 Research Plan 中添加三类彩色标记，便于导师快速识别需要审查和确认的关键事项。

---

## 标记类型

### 🔴 红色 - ADVISOR REVIEW（导师审查）
**格式**: `[ADVISOR REVIEW: ...]`  
**用途**: 需要导师做出重要决策或提供关键指导的事项

### 🔵 蓝色 - VERIFY（验证确认）
**格式**: `[VERIFY: ...]`  
**用途**: 需要验证的技术参数、数值或实验条件

### 🟠 橙色 - TODO（待办事项）
**格式**: `[TODO: ...]`  
**用途**: 学生需要完成的行动项目

---

## 已添加的审查标记列表

### 第一页：审查清单摘要框
在标题下方添加了一个醒目的框架，包含：
- 所有标记类型的说明
- 6 个关键问题汇总
- 快速导航指南

---

### Objective 1（研究目标 1）

**[VERIFY]** 能量值确认
```
Please confirm these energy values match the actual band structure 
of CsV₃Sb₅ or provide updated DFT calculations
```
**位置**: M-点跃迁能量 (1.2-1.4 eV) 和 K-点 Dirac 态 (0.9-1.1 eV)  
**原因**: 这些数值是实验设计的核心，需要基于准确的能带结构计算

---

### Objective 2（研究目标 2）

**[VERIFY]** Fano 参数值
```
Are these q-parameter values appropriate for kagome metals? 
Please provide reference values if available
```
**位置**: q = 2-5 的 Fano 不对称参数  
**原因**: 该范围是基于其他 CDW 系统估算，需确认是否适用于 kagome 金属

---

### Objective 3（研究目标 3）

**[VERIFY]** 测量灵敏度
```
Please confirm this sensitivity is achievable with current lab equipment
```
**位置**: ΔR_CD / ΔR ~ 10⁻³-10⁻²  
**原因**: 圆二色性测量需要高灵敏度，需确认实验室设备能否达到

---

### Methodology - Experimental Setup（方法学 - 实验装置）

#### 1. **[ADVISOR REVIEW]** OPA 系统可用性
```
Does the Kondo Lab have this OPA system available, or will it need 
to be purchased/shared with another lab?
```
**位置**: Ti:Sapphire + OPA 系统描述  
**重要性**: ⭐⭐⭐⭐⭐  
**原因**: 
- 这是整个研究的核心设备
- 涉及预算或实验室间合作安排
- 影响项目启动时间

#### 2. **[VERIFY]** 光学元件兼容性
```
Are achromatic quarter-wave plates available for the full 0.8-1.6 eV range?
```
**位置**: 圆偏振测量所需的四分之一波片  
**原因**: 宽光谱范围需要特殊光学元件，需确认可用性

---

### Methodology - Sample Preparation（方法学 - 样品制备）

#### 3. **[ADVISOR REVIEW]** 样品合作
```
Has contact been established with the Wilson group or other synthesis 
groups? Please confirm availability and timeline for sample delivery
```
**位置**: 样品来源描述  
**重要性**: ⭐⭐⭐⭐⭐  
**原因**: 
- 样品是实验的前提条件
- 需要提前数月建立合作关系
- 影响整个时间线的可行性

#### 4. **[VERIFY]** 低温设备
```
Is the cryostat with this temperature range and stability available in the lab?
```
**位置**: 10-300 K，稳定性 ±0.5 K 的低温恒温器  
**原因**: 需确认实验室现有设备规格

---

### Timeline（时间线）

#### 5. **[ADVISOR REVIEW]** 时间规划现实性
```
Please review if 6 months is realistic for this phase given the 
number of energy points and required averaging time
```
**位置**: Months 4-9（能量依赖测量阶段）  
**原因**: 需导师根据实际经验评估数据采集所需时间

#### 6. **[TODO]** 理论合作者
```
Identify potential theory collaborators early in the project
```
**位置**: Months 19-21（数据分析阶段）  
**原因**: 提前建立理论合作有助于数据解读

#### 7. **[ADVISOR REVIEW]** 毕业要求对齐
```
Please confirm if these target journals and timelines align with 
your expectations for graduation requirements
```
**位置**: Months 22-24（投稿和答辩阶段）  
**重要性**: ⭐⭐⭐⭐  
**原因**: 确保研究计划符合博士毕业标准

---

### Risk Assessment（风险评估）

#### 8. **[ADVISOR REVIEW]** Prof. Ozeki 合作
```
Please advise if collaboration with Prof. Ozeki is feasible and if 
formal arrangements need to be made
```
**位置**: Risk 4 - OPA 稳定性问题  
**原因**: 涉及跨实验室合作，需导师协调

#### 9. **[ADVISOR REVIEW]** 样品合作优先级
```
Should we prioritize establishing these collaborations immediately, 
or are there existing connections we can leverage?
```
**位置**: Risk 5 - 样品可用性  
**重要性**: ⭐⭐⭐⭐⭐  
**原因**: 
- 需立即采取行动的事项
- 可能利用现有人脉网络
- 影响项目启动

---

### Broader Impact（广泛影响）

#### 10. **[ADVISOR REVIEW]** 研究方向契合度
```
Please confirm that this research direction aligns with the lab's 
current priorities and available resources
```
**位置**: 与 Kondo Lab 研究方向的对齐声明  
**重要性**: ⭐⭐⭐⭐  
**原因**: 确保项目与实验室长期规划一致

---

## 按重要性排序的关键事项

### 🔥 最高优先级（立即需要确认）
1. **OPA 系统可用性**（设备/预算）
2. **样品合作关系建立**（Wilson 组等）
3. **能带结构能量值**（DFT 计算）

### ⚡ 高优先级（第一次会议讨论）
4. **低温设备规格确认**
5. **Prof. Ozeki 合作可行性**
6. **毕业时间线和期刊目标**
7. **研究方向与实验室优先级对齐**

### ✓ 中等优先级（后续确认）
8. **测量灵敏度**（设备性能）
9. **Fano 参数参考值**
10. **四分之一波片光谱范围**
11. **时间规划现实性评估**

### 📝 学生行动项
12. **识别理论合作者**（TODO）

---

## 使用建议

### 给导师的建议：
1. **首次审阅**: 先阅读第一页的"审查清单摘要框"
2. **逐项确认**: 按照文档中的彩色标记逐一审查
3. **批注方式**: 
   - 可以直接在 PDF 上添加批注
   - 或在单独文档中按标记编号回复
   - 或在会议中口头讨论

### 给学生的建议：
1. **会议准备**: 打印此说明文档，准备每个问题的背景资料
2. **记录决策**: 会议后创建决策日志，记录每项的确认结果
3. **后续行动**: 根据导师反馈更新 Research Plan
4. **移除标记**: 确认后可删除相应的彩色标记，保持文档整洁

---

## 文档统计

- **总标记数**: 12 个
- **ADVISOR REVIEW**: 6 个（红色）
- **VERIFY**: 5 个（蓝色）
- **TODO**: 1 个（橙色）

- **涉及章节**: 
  - Objectives: 3 个标记
  - Methodology: 4 个标记
  - Timeline: 3 个标记
  - Risk Assessment: 2 个标记
  - Broader Impact: 1 个标记

---

## 后续步骤

### 第一次导师会议议程建议：
1. **开场**（5 分钟）：简述研究计划核心创新点
2. **设备与资源**（15 分钟）：讨论 OPA、低温设备、光学元件
3. **样品与合作**（15 分钟）：样品来源、合作关系建立
4. **技术参数**（10 分钟）：能量值、灵敏度、Fano 参数
5. **时间线**（10 分钟）：各阶段时间安排的现实性
6. **下一步行动**（5 分钟）：确定优先级和截止日期

### 会议后 TODO：
- [ ] 根据导师反馈更新所有标记项
- [ ] 创建设备清单和采购/共享计划（如需要）
- [ ] 起草样品合作邮件（如需要）
- [ ] 寻找或计算更准确的能带结构数据
- [ ] 更新时间线甘特图
- [ ] 准备最终版 Research Plan（无标记版）

---

## 文件位置

- **LaTeX 源文件**: `ResearchPlan.tex`
- **生成的 PDF**: `ResearchPlan.pdf`（8 页，含彩色标记）
- **修改说明**: `MODIFICATIONS.md`
- **本文档**: `ADVISOR_REVIEW_NOTES.md`

---

## 技术说明

### LaTeX 实现
文档使用了以下 LaTeX 包和命令来实现彩色标记：

```latex
\usepackage{xcolor}
\usepackage{soul}

\newcommand{\advisornote}[1]{{\color{red}\textbf{[ADVISOR REVIEW: #1]}}}
\newcommand{\verify}[1]{{\color{blue}\textbf{[VERIFY: #1]}}}
\newcommand{\todo}[1]{{\color{orange}\textbf{[TODO: #1]}}}
```

### 移除标记
如果需要生成无标记的"最终版"，可以重新定义这些命令为空：

```latex
\renewcommand{\advisornote}[1]{}
\renewcommand{\verify}[1]{}
\renewcommand{\todo}[1]{}
```

或者直接删除文档中所有 `\advisornote{...}`, `\verify{...}`, `\todo{...}` 调用。

---

**最后更新**: 2025年10月20日  
**版本**: 1.0（初始版本，包含 12 个审查标记）
