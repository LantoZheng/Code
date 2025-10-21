# Research Plan - Kondo Lab

**学生**: Xiaoyang Zheng  
**题目**: Band-Selective Ultrafast Dynamics and Non-Thermal Control in the Topological Kagome Metal CsV₃Sb₅  
**实验室**: Kondo Laboratory  
**最后更新**: 2025年10月20日

---

## 📚 文档目录

### 主文档
- **ResearchPlan.pdf** (8 页) - 完整的研究计划，包含导师审查标记
- **ResearchPlan.tex** - LaTeX 源文件
- **ResearchPlan.bib** - 参考文献数据库（11 篇引用）

### 辅助文档（按阅读顺序）

1. **SUMMARY_ADVISOR_MARKS.md** ⭐ 从这里开始
   - 完成工作总结
   - 所有标记的快速概览
   - 使用指南和工作流程

2. **ADVISOR_CHECKLIST.md** 📋 会议必备
   - 可打印的单页检查清单
   - 复选框格式，便于记录决策
   - 会议记录空间

3. **ADVISOR_REVIEW_NOTES.md** 📖 详细参考
   - 所有 12 个标记的完整说明
   - 按优先级排序的关键事项
   - 技术实现细节

4. **MODIFICATIONS.md** 📝 修改历史
   - 详细的内容修改对比
   - 修改前后的文档统计
   - 未来改进建议

---

## 🎨 标记系统说明

### 三种彩色标记

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

---

## 🎯 关键事项（按优先级）

### ⭐⭐⭐⭐⭐ 最高优先级
1. **OPA 系统**：是否需要购买或共享？
2. **样品合作**：是否已与合成组建立联系？
3. **能带结构**：能量值是否需要 DFT 计算验证？

### ⭐⭐⭐⭐ 高优先级
4. 低温设备规格确认
5. Prof. Ozeki 合作可行性
6. 毕业时间线和期刊目标对齐
7. 研究方向与实验室优先级匹配

### ⭐⭐⭐ 中等优先级
8. 测量灵敏度验证
9. Fano 参数参考值
10. 光学元件光谱范围
11. 实验阶段时间评估

### 待办事项
12. 识别理论合作者

---

## 📖 快速开始指南

### 给导师

#### 第一次审阅（15-20 分钟）
1. 打开 **ResearchPlan.pdf**
2. 阅读第 1 页的"审查摘要框"（红框）
3. 浏览标记部分（彩色文本）
4. 记录初步想法

#### 详细审阅（准备会议）
1. 阅读 **ADVISOR_REVIEW_NOTES.md** 了解每个标记的背景
2. 使用 **ADVISOR_CHECKLIST.md** 记录决策
3. 准备会议议程

#### 会议中
- 使用 ADVISOR_CHECKLIST 逐项讨论
- 在复选框中记录决策
- 明确学生的下一步行动

---

### 给学生

#### 会前准备
- [ ] 打印 **ADVISOR_CHECKLIST.md**
- [ ] 准备每个 VERIFY 项的支持材料
- [ ] 列出可能的样品合作组
- [ ] 调研实验室设备清单
- [ ] 准备 DFT 能带结构图（或查找文献）

#### 会议中
- [ ] 记录所有导师决策
- [ ] 标注需要跟进的事项
- [ ] 明确 deadline

#### 会后跟进
- [ ] 根据反馈更新 ResearchPlan.tex
- [ ] 完成所有 TODO 事项
- [ ] 联系样品合成组（如批准）
- [ ] 准备最终版（移除标记）

---

## 🔧 编译说明

### 完整编译流程
```bash
cd /Users/zhengxiaoyang/Code/CV-LaTeX/ResearchPlan/Kondo
xelatex ResearchPlan.tex
biber ResearchPlan
xelatex ResearchPlan.tex
xelatex ResearchPlan.tex
```

### 要求
- XeLaTeX（用于 fontspec 和 Times New Roman）
- Biber（参考文献管理）
- 字体：Times New Roman（系统字体）

### 编译后输出
- **ResearchPlan.pdf**（8 页）
  - 第 1 页：标题 + 审查摘要框 + 摘要
  - 第 2-3 页：背景和研究目标
  - 第 4-5 页：方法学和时间线
  - 第 6-7 页：风险评估和广泛影响
  - 第 8 页：参考文献

---

## 📊 文档统计

### Research Plan
- **总页数**: 8 页（含参考文献）
- **字数**: ~3,500 词
- **章节**: 6 个主要章节
- **参考文献**: 11 篇
- **标记数**: 12 个

### 修改历史
- **初始版本**: ~4-5 页，缺乏实验细节
- **第一次修改**: 扩展至 7 页，添加详细方法学和风险评估
- **第二次修改**: 8 页，添加导师审查标记和首页摘要

---

## 🎓 研究计划亮点

### 创新点
1. **Band-selective 视角**：超越传统 band-averaged 方法
2. **动量分辨耦合图谱**：首次针对 kagome 金属
3. **圆偏振探测**：寻找 chiral CDW 的动力学证据

### 技术特色
- 泵浦能量可调（0.8-1.6 eV）
- 时间分辨率 ~50 fs
- 温度范围 10-300 K
- 圆二色性测量灵敏度 10⁻³-10⁻²

### 预期成果
- 首个 kagome 金属的 excitation spectrum
- 动量选择性电子-声子耦合机制
- 潜在的 chiral order 动力学证据
- 高影响力期刊论文（PRL/Nature Comm.）

---

## 🔄 工作流程

### 当前阶段：导师审查
```
┌─────────────────┐
│  完成标记添加   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 安排导师会议    │ ← 你在这里
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  会议讨论决策   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  更新研究计划   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 生成最终版本    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 开始实验准备    │
└─────────────────┘
```

---

## 📞 常见问题

### Q: 如何移除标记生成最终版？
**A**: 两种方法：
1. 在 LaTeX 序言中添加：
   ```latex
   \renewcommand{\advisornote}[1]{}
   \renewcommand{\verify}[1]{}
   \renewcommand{\todo}[1]{}
   ```
2. 手动删除所有标记调用和首页摘要框

### Q: 可以修改标记颜色吗？
**A**: 可以，在 LaTeX 序言中修改 `\color{red}` 为其他颜色，如 `\color{purple}`

### Q: 如何添加新标记？
**A**: 使用已定义的命令：
```latex
\advisornote{你的审查问题}
\verify{需要验证的参数}
\todo{待办事项}
```

### Q: 检查清单可以数字化吗？
**A**: 可以转换为 Google Form 或使用 Markdown 编辑器的复选框功能

---

## 📂 文件组织建议

### 当前结构
```
Kondo/
├── ResearchPlan.tex           # 主文档
├── ResearchPlan.pdf           # PDF 输出
├── ResearchPlan.bib           # 参考文献
├── ADVISOR_CHECKLIST.md       # 检查清单
├── ADVISOR_REVIEW_NOTES.md    # 详细说明
├── MODIFICATIONS.md           # 修改历史
├── SUMMARY_ADVISOR_MARKS.md   # 总结
└── README.md                  # 本文件
```

### 建议添加（未来）
```
Kondo/
├── figures/                   # 图片文件夹
│   └── band_structure.pdf    # 能带结构图
├── data/                      # 数据文件夹
│   └── energy_estimates.csv  # 能量估算
├── meeting_notes/             # 会议记录
│   └── 2025-10-20.md
└── versions/                  # 历史版本
    └── ResearchPlan_v1.0.pdf
```

---

## 🎯 下一步行动

### 立即行动
- [ ] 阅读 **SUMMARY_ADVISOR_MARKS.md**
- [ ] 安排导师会议
- [ ] 打印 **ADVISOR_CHECKLIST.md**

### 会前准备（建议 2-3 天）
- [ ] 准备能带结构图
- [ ] 列出样品合作组清单
- [ ] 调研实验室设备
- [ ] 收集相关文献

### 会后跟进
- [ ] 更新研究计划
- [ ] 完成待办事项
- [ ] 准备最终版

---

## 📧 联系方式

如有技术问题，请参考：
- LaTeX 编译问题：检查 `ResearchPlan.log`
- 内容问题：查阅 `ADVISOR_REVIEW_NOTES.md`
- 流程问题：参考本 README

---

**版本**: 2.0（含导师审查标记）  
**状态**: ✅ 准备就绪，等待导师审查  
**创建日期**: 2025年10月20日  
**预计会议日期**: _待定_
