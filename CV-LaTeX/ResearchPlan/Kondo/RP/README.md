# 🔬 Research Plan (RP)

本文件夹包含 Research Plan 的所有文件。

---

## 📄 文件列表

| 文件名 | 类型 | 说明 |
|--------|------|------|
| **ResearchPlan.pdf** | PDF | 完整研究计划（8 页） |
| ResearchPlan.tex | LaTeX | 源文件 |
| ResearchPlan.bib | BibTeX | 参考文献数据库（24 篇） |

---

## 🎯 研究主题

**Band-Selective Ultrafast Dynamics and Non-Thermal Control in the Topological Kagome Metal CsV₃Sb₅**

通过泵浦-探测反射光谱研究 kagome 金属 CsV₃Sb₅ 中的超快动力学。

---

## 📊 文档特点

### 项目定位
- **类型**：2 年制 Master 项目（非博士）
- **实验室**：Kondo Laboratory, ISSP
- **意向导师**：Professor Takeshi Kondo

### 研究目标
1. **Objective 1**：能带选择性光激发动力学
2. **Objective 2**：CDW 声子模式的 Fano 共振
3. **Objective 3**：手性 CDW 的圆二色性测量（可选）

### 时间线
- **Year 1** (Months 1-12)：基础 + 技能 + Objective 1
- **Year 2** (Months 13-24)：Objective 2 + 可选 Objective 3 + 论文

### 预期成果
- 1-2 篇第一作者论文（PRB 或 JPSJ）
- 完整硕士论文

---

## 🎨 导师审查标记系统

文档中使用三种彩色标记：

| 标记 | 颜色 | 用途 | 数量 |
|------|------|------|------|
| `[ADVISOR REVIEW: ...]` | 🔴 红色 | 需要导师决策的关键事项 | 7 个 |
| `[VERIFY: ...]` | 🔵 蓝色 | 需要验证的技术参数 | 5 个 |
| `[TODO: ...]` | 🟠 橙色 | 学生待办事项 | 1 个 |

### 关键问题（按优先级）

#### ⭐⭐⭐⭐⭐ 最高优先级
1. **OPA 系统可用性** - 是否需要购买或共享？
2. **样品获取** - 是否已与合成组建立联系？
3. **能带结构** - 能量值是否需要 DFT 验证？

#### ⭐⭐⭐⭐ 高优先级
4. 低温设备规格确认
5. Prof. Ozeki 合作可行性
6. 毕业时间线和期刊目标对齐
7. 研究方向与实验室优先级匹配

---

## 📚 详细说明文档

想了解更多关于 Research Plan 的信息，请查看：

**[Documentation/Notes_on_RP.md](../Documentation/Notes_on_RP.md)**

包含：
- 导师审查系统详解
- 所有 13 个标记的完整说明
- 关键问题与决策点
- 修改历史总结（5 轮修改）
- 参数验证记录
- 使用指南（导师会议准备、文档更新工作流）

---

## 🔧 编译说明

使用 LaTeX + BibTeX 编译：

```bash
# 完整编译流程
pdflatex ResearchPlan.tex
bibtex ResearchPlan
pdflatex ResearchPlan.tex
pdflatex ResearchPlan.tex  # 运行两次以解决交叉引用
```

---

## 📋 导师会议准备

### 会前准备（推荐顺序）

1. **快速了解**：查看 [Documentation/Notes_on_RP.md](../Documentation/Notes_on_RP.md) 的导师审查系统部分
2. **了解关键问题**：按优先级准备讨论（OPA、样品、能量值）
3. **查看标记**：在 PDF 中定位所有彩色标记
4. **准备材料**：打印 PDF 或准备电子版展示

### 会议议程建议

**Part 1: 关键决策（30 分钟）**
- OPA 系统可用性
- 样品获取策略
- 研究方向对齐

**Part 2: 技术参数（20 分钟）**
- 能带结构能量值
- 设备和元件确认
- 时间线评估

**Part 3: 合作与资源（10 分钟）**
- 跨组合作
- 理论合作者
- 毕业要求

---

## 📊 文档统计

- **总页数**：8 页
- **参考文献**：24 篇
- **标记数量**：13 个（7 ADVISOR + 5 VERIFY + 1 TODO）
- **时间线**：24 个月
- **研究目标**：3 个（第 3 个可选）

---

## ⚠️ 重要提醒

### 技术差异注意
- **Research Plan** 侧重泵浦-探测反射光谱
- **Kondo Lab** 主要使用 ARPES（正开发时间分辨）
- **策略**：已在 Statement of Purpose 中强调灵活性

### 标记不是问题
- 标记是**沟通工具**，展示深思熟虑
- 向导师展示已识别的关键决策点
- 不是"不知道"，而是"需要确认最佳方法"

---

## 🔄 修改历史

本 Research Plan 经过 5 轮修改优化：

1. **第一轮**：从博士到 Master 项目调整
2. **第二轮**：补充实验细节
3. **第三轮**：添加导师审查标记
4. **第四轮**：参数验证与隐私保护
5. **第五轮**：OPA 系统确认更新

详见：[Documentation/Notes_on_RP.md](../Documentation/Notes_on_RP.md) 的修改历史部分

---

**返回**: [主目录 README](../README.md)
