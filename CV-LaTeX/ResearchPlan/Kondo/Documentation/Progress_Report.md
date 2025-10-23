# PhD转换计划修改进度报告

**日期**: 2025年10月23日
**状态**: Phase 1核心修改完成 (~60%)，Phase 2待实施

---

## ✅ 已完成的关键修改

### 1. 引文准确性核实 ✅

**完成度**: 100%

**验证结果**:

- ✅ PRL 134, 096401 (2024) - "Chirality in the Kagome Metal CsV₃Sb₅" - **正确**
- ✅ PRB 107, 174303 (2023) - "All-optical manipulation of charge density waves" - **正确**
- ⚠️ **已修正**: arXiv:2503.07442 → **PRB 112, 125127 (2025)** "Coherent Phonon Pairs..."
- ✅ Progress in Surface Science (2025) - HHG-based trARPES review - **正确**
- ✅ PRR 7, 013025 (2025) - ML for Weyl points (Hofmann group) - **正确**

**修改位置**:

- `Research_Insights_2024-2025.md` Line 50

---

### 2. Kondo Lab研究方向调研 ✅

**完成度**: 100%

**核心发现**:

| 研究方向                      | 契合度         | 证据                                   | 对计划的影响           |
| ----------------------------- | -------------- | -------------------------------------- | ---------------------- |
| **铜氧化物超导体**      | 🟢🟢🟢🟢🟢 5/5 | "Main topic...cuprates"                | **Year 4重点！** |
| **拓扑材料ARPES**       | 🟢🟢🟢🟢🟢 5/5 | PRL 132, 136402 (2024) Dirac semimetal | 基础专长               |
| **Time-resolved ARPES** | 🟢🟢🟢🟢 4/5   | 他人引用，状态不确定                   | 高新技术               |
| **Kagome metals**       | 🟢🟢🟢 3/5     | "Entangled Kondo-Kagome lattices"      | 新兴方向               |

**⚠️ 关键战略调整**:

```diff
原计划假设:
- trARPES是"确定的Lab能力"
- Dual-modality (reflectivity + trARPES)是"主线"

修改后策略:
+ Pump-probe reflectivity是"主线技术" (100%确定)
+ trARPES是"potential future direction" (保守)
+ 铜氧化物是"Year 4战略重点" (5/5契合!)
```

**文档创建**:

- ✅ `Kondo_Feedback_Analysis.md` (8章节,详细分析)

---

### 3. Abstract彻底重写 ✅

**完成度**: 100%

#### **Before** (技术导向):

```
"This doctoral research outlines... by developing band-selective 
pump-probe spectroscopy as a novel quantitative tool..."
```

#### **After** (物理问题导向):

```
"Core Physics Questions: How do electron-phonon coupling and 
electron-electron correlations compete to drive CDW formation? 
How does correlation-topology interplay manifest in non-equilibrium?"

"Measurable Observables:
- Energy scales: ΔE(t), ΔCDW(t) (meV precision)
- Time scales: τe-e, τe-ph (fs resolution)  
- Interaction strengths: λ, Z
- Momentum dependence: Ai(k,t)"
```

**关键改进**:

- ✅ 开头即明确**核心物理问题**（not技术描述）
- ✅ 列出**12+可测量物理量**（含精度和单位）
- ✅ **trARPES保守化**: "Should Lab's trARPES capabilities become available..." (不再是确定计划)
- ✅ **5-year physics-driven timeline**: Foundation→Mechanism→Topology→Universality→Engineering
- ✅ 直接响应Kondo建议: "disentangle e-ph vs e-e" + "measurable observables"

**修改位置**:

- `PhD_Conversion_Plan.md` Lines 120-170

---

### 4. 可测量物理量体系建立 ✅

**完成度**: 100%

创建了完整的 `Measurable_Observables.md`文档，包含:

#### **四大物理量类别**:

**A. 能量尺度** (meV精度)

- $\Delta E(t)$ - 瞬态能量移动
- $\Delta_{\text{CDW}}(t)$ - CDW gap演化
- $W(t)$ - 带宽重整化
- $\Delta E_{\text{VH}}(t)$ - Van Hove点移动

**B. 时间尺度** (fs-ps精度)

- $\tau_{e-e} \sim 50-100$ fs - 电子热化
- $\tau_{e-ph} \sim 0.5-2$ ps - e-ph耦合
- $\tau_{\text{CDW}} \sim 5-50$ ps - CDW恢复
- $\tau_{\text{coh}} \sim 1-5$ ps - 相干衰减

**C. 耦合强度** (无量纲)

- $\lambda \sim 0.3-0.8$ - e-ph coupling
- $Z = m^*/m \sim 2-5$ - 准粒子权重
- $U/W$ - 关联强度
- $\langle \psi \rangle$ - CDW序参量

**D. 动量空间** ($\mathbf{k}$-resolved)

- $A_i(\mathbf{k}, t)$ - Band-selective dynamics
- $\mathbf{k}_F(t)$ - 费米面演化
- $\mathbf{Q}_{\text{CDW}}(t)$ - 嵌套矢量

#### **每个Objective的定量目标**:

**Objective 1** (Year 1-2): Mechanism Identification

- **判据**: 若$\tau_{e-ph} \ll \tau_{\text{CDW}}$ → e-ph主导
- **提取**: $\lambda \sim 0.5 \pm 0.2$
- **验证**: Fluence dependence (线性→e-ph, 非线性→e-e)

**Objective 2** (Year 2-3): Correlation-Topology

- **Map**: $A_i(\mathbf{k}, t)$ via pump-energy scan
- **提取**: $Z(\mathbf{k})$ momentum dependence
- **Test**: Van Hove点 vs 普通区域对比

**Objective 3** (Year 3-4): Universality - **Cuprates重点**

- **Pseudogap**: $\Delta_{\text{PG}}(t)$ vs temperature
- **d-wave**: $A_i(\phi, t)$ azimuthal dependence
- **Scaling**: $\tau_{\text{relax}}$ vs $T_c$ relations

**Objective 4** (Year 4-5): Photo-induced phases

- **Order parameters**: $\langle \psi_{\text{CDW/SC/M}} \rangle(t)$
- **Floquet**: Pump-pump-probe sidebands
- **Lifetime**: $\tau_{\text{photo-phase}} > 10$ ps (stability criterion)

**文档价值**:

- 清晰响应Kondo: "Define measurable observables"
- 提供定量success metrics
- 区分Master-level (定性) vs PhD-level (定量±precision)

---

### 5. 战略分析文档创建 ✅

**完成度**: 100%

创建了 `Kondo_Feedback_Analysis.md`，包含:

**8个主要章节**:

1. Kondo反馈核心要点解读
2. Kondo Lab研究方向确认
3. 修改策略: 从技术到物理
4. 具体修改行动清单
5. 引文修正记录
6. 关键消息点（给委员会）
7. 执行优先级
8. 成功标准

**关键洞见**:

**Kondo建议一**: "Clarify long-term physical objective"

```
问题诊断:
❌ Current: "track Fermi surface evolution" = 技术描述
✅ Needed: "disentangle e-ph vs e-e" = 物理问题

解决方案:
- 每个Objective都是physical question (not技术任务)
- 5-year递进逻辑: Method→Mechanism→Topology→Universality→Engineering
```

**Kondo建议二**: "Define measurable observables"

```
问题诊断:
❌ Current: "measure dynamics" (模糊)
✅ Needed: "具体物理量 + 数值精度 + 物理意义"

解决方案:
- 12+定量物理量，每个含: 符号、典型值、测量方法、物理框架
- 表格化呈现 (委员会友好)
```

**trARPES保守化策略**:

```diff
- 原版: "leveraging Lab's trARPES development" (确定性)
+ 修改: "Should Lab's trARPES capabilities become available,
         my reflectivity data will provide ideal targets...
         However, core research is complete using reflectivity alone"
```

---

## 🚧 进行中的工作

### 6. trARPES描述保守化 🔄

**完成度**: 60% (Abstract完成, Objectives/Timeline待修改)

**Abstract** ✅:

```latex
"Should the laboratory's ongoing time-resolved ARPES development 
mature during my doctoral term, my reflectivity data will provide 
ideal targets for momentum-resolved validation—creating a powerful 
dual-modality framework. However, the core research program is 
designed to be complete and impactful using reflectivity alone."
```

**待修改**:

- Objectives章节: 去除对trARPES的依赖描述
- Timeline: 将trARPES从"Year 3-4主线"改为"optional future extension"
- Expected Outcomes: 明确即使没有trARPES，研究仍完整

---

## ⏳ 待完成的关键任务

### 7. 铜氧化物战略重点强化 📋

**优先级**: 🔴 High (利用Kondo Lab 5/5契合度!)

**需要添加**:

#### **Objective 3重写** (Year 3-4):

```latex
\textbf{Objective 3 (Year 3-4): Extending to Cuprate Superconductors}

\textit{Physics Question:} How do pseudogap and superconducting gap 
respond differently to ultrafast perturbations? Can we distinguish 
d-wave pairing symmetry in time domain?

\textit{Leveraging Kondo Lab Expertise:} Prof. Kondo's world-leading 
ARPES studies of cuprates provide unique advantage for this objective. 
My ultrafast measurements will address the same fundamental questions 
(e-ph vs e-e, pairing mechanism) in the time domain.

\textit{Measurable Observables:}
- Pseudogap dynamics: $\Delta_{\text{PG}}(T,t)$ for $T_c < T < T^*$
- d-wave anisotropy: $A_i(\phi, t)$, expect $\cos(2\phi)$ signature
- Relaxation channel identification: Does $\Delta_{\text{PG}}$ relax 
  through phonons or electronic correlations?

\textit{Sample Accessibility:} Kondo Lab's extensive cuprate sample 
library (LSCO, Bi2212, YBCO family) provides ideal testing ground.

\textit{Expected Outcomes:}
- First time-resolved study connecting equilibrium pseudogap structure 
  to non-equilibrium dynamics
- 1-2 papers in PRB/PRX (high-impact in cuprate community!)
- Direct comparison with Kondo Lab's equilibrium ARPES → unified picture

\textit{Risk:} 🟢 Low (Lab core expertise, samples available, proven techniques)
```

**战略理由**:

- **5/5契合度**: 最大化与Kondo Lab专长的overlap
- **样品优势**: Lab有extensive cuprate collection
- **互补性**: Equilibrium ARPES (Kondo专长) + Ultrafast (您贡献)
- **影响力**: Cuprate社区庞大，引用potential高
- **发表**: PRB/PRX级别（高质量但realistic）

---

### 8. Publication Strategy细化 📋

**优先级**: 🟡 Medium

**需要修改**: 从"数字目标"到"物理故事"

#### **Before**:

```
"Paper 1: Band-selective coupling (PRB)"
"Paper 2: Temperature dependence (PRB)"
...
```

#### **After** (Physics-driven narrative):

```
**Paper 1 (Year 2, PRB)**: "Disentangling electron-phonon vs 
electron-electron interactions in kagome CDW via band-selective 
ultrafast spectroscopy"

Physics Story:
- Core Question: e-ph or e-e driving CDW?
- Key Result: $\tau_{e-ph} = 1.2 \pm 0.3$ ps, $\lambda = 0.55 \pm 0.15$
- Conclusion: e-ph dominant but e-e contributes at high fluence
- Impact: Resolves controversy, cited as reference

**Paper 2 (Year 3, PRL/Nat.Comm.)**: "Correlation-enhanced ultrafast 
response near Van Hove singularity in CsV₃Sb₅"

Physics Story:
- Core Question: Does topology affect many-body dynamics?
- Key Result: $Z(\mathbf{k}_{\text{VH}}) = 2.8$ vs $Z(\Gamma) = 1.5$
- Conclusion: Van Hove→enhanced correlation→slower relaxation
- Impact: First momentum-resolved non-equilibrium many-body study

**Paper 3 (Year 4, PRB/PRX)**: "Pseudogap ultrafast dynamics in 
electron-doped cuprates: Distinguishing pairing vs fluctuation scenarios"

Physics Story:
- Core Question: Is pseudogap a pairing precursor or separate phenomenon?
- Key Result: $\tau_{\text{PG}}(T)$ shows d-wave anisotropy below $T^*$
- Conclusion: Supports pairing fluctuation picture
- Impact: Leverages Kondo Lab expertise, high cuprate community interest
- 🟢 Lowest Risk (Lab specialty!)

[... Paper 4-5 similar format]
```

**每篇论文包含**:

- Physics Question (not技术目标)
- Key Measurable Observables (定量结果)
- Expected Conclusion (可证伪)
- Impact Assessment (引用预期, 社区相关性)
- Risk Level (🟢🟡🔴)

---

### 9. Timeline物理里程碑重写 📋

**优先级**: 🟡 Medium

**需要修改**: 从"技术任务"到"物理理解递进"

#### **当前版本**:

```
Year 1: Lab integration, equipment training...
Year 2: Temperature scans, first paper...
Year 3: Extension to other materials...
```

#### **修改为物理问题递进**:

```
**Year 1 (Foundation): "Does the method work?"**
- Question: Can pump-energy tuning achieve band-selectivity?
- Milestone: First $A_i(E_{\text{pump}}, t)$ dataset
- Physics Outcome: Proof-of-principle
- Publication Prep: Methods paper drafting

**Year 2 (Mechanism): "What drives the CDW?"**
- Question: Disentangle e-ph vs e-e interactions
- Milestone: Extract $\tau_{e-e}, \tau_{e-ph}, \lambda$
- Physics Outcome: Quantitative phase diagram
- Publication: PRB paper submitted

**Year 3 (Topology): "Does topology matter?"**
- Question: Correlation-topology interplay
- Milestone: Map $Z(\mathbf{k})$, prove VH enhancement
- Physics Outcome: First $\mathbf{k}$-resolved many-body dynamics
- Publication: PRL/Nat.Comm. submitted

**Year 4 (Universality): "Is this universal?"**
- Question: Cross-material validation
- Milestone Focus: **Cuprates pseudogap** (Kondo Lab specialty!)
- Physics Outcome: Unified framework across materials
- Publications: 2 papers (cuprates⭐ + comparative study)

**Year 5 (Synthesis & Frontier): "Can we engineer?"**
- Question: Photo-induced hidden phases achievable?
- Milestone: Complete dissertation
- Physics Outcome: Comprehensive physical picture
- Publication: Capstone paper OR definitive review
```

**关键**: 每年一个**physics question**作为组织原则

---

### 10. Statement of Purpose修改 📋

**优先级**: 🔴 High (必须响应Kondo反馈!)

**需要修改的段落**:

#### **A. Research Objectives段落**:

```diff
- Before: "My goal is to track the evolution of Fermi surfaces and 
          band dispersions with time-resolved ARPES..."

+ After: "My doctoral research addresses a fundamental question in 
         many-body physics: **How do electron-phonon coupling and 
         electron-electron correlations compete in topological CDW 
         systems?** By measuring quantitative observables—transient 
         energy shifts $\Delta E(t)$ (meV precision), carrier 
         relaxation times $\tau_{e-e}$ and $\tau_{e-ph}$ (fs resolution), 
         and correlation-induced band renormalization $Z$—I will 
         establish a predictive framework extending Prof. Kondo's 
         equilibrium expertise into the time domain."
```

#### **B. Why Kondo Lab段落**:

```diff
- Before: "Prof. Kondo's laboratory possesses world-leading ARPES 
          capabilities..."

+ After: "Prof. Kondo's unparalleled expertise in equilibrium 
         angle-resolved photoemission of strongly correlated materials
         —particularly **cuprates** (pseudogap, d-wave pairing) and 
         topological systems—provides the ideal foundation to extend 
         into non-equilibrium physics. My ultrafast spectroscopy will 
         address the **same fundamental questions** (e-ph vs e-e, 
         correlation effects, pairing mechanisms) but in the time domain, 
         creating natural synergy. The laboratory's established sample 
         synthesis collaborations and extensive cuprate library uniquely 
         position this work for high impact."
```

#### **C. Timeline段落**:

```diff
- Before: "Years 1-2: Foundation Phase... Years 3-4: Research Phase..."

+ After: "My five-year program is structured around **progressive 
         physics understanding**:
       
         Years 1-2: *Establishing Methodology & Mechanism Identification*
         - Core Question: Disentangle e-ph vs e-e in kagome CDW
         - Deliverable: Quantitative phase diagram (PRB)
       
         Year 3: *Correlation-Topology Interplay*
         - Core Question: Does topology enhance many-body effects?
         - Deliverable: Breakthrough discovery (PRL/Nat.Comm.)
       
         Year 4: *Universal Framework via Cuprates*
         - Core Question: Are mechanisms universal?
         - Deliverable: Leverage Prof. Kondo's core expertise (PRB/PRX)
       
         Year 5: *Synthesis & Photo-induced Phases*
         - Deliverable: Comprehensive dissertation, capstone paper"
```

---

## 📊 整体进度评估

### 完成度统计

| 任务类别                   | 完成度 | 状态      |
| -------------------------- | ------ | --------- |
| **引文核实**         | 100%   | ✅ 完成   |
| **Kondo Lab调研**    | 100%   | ✅ 完成   |
| **Abstract重写**     | 100%   | ✅ 完成   |
| **可测量物理量体系** | 100%   | ✅ 完成   |
| **战略分析文档**     | 100%   | ✅ 完成   |
| **trARPES保守化**    | 60%    | 🔄 进行中 |
| **铜氧化物强化**     | 0%     | ⏳ 待开始 |
| **Publication细化**  | 0%     | ⏳ 待开始 |
| **Timeline重写**     | 0%     | ⏳ 待开始 |
| **SoP修改**          | 0%     | ⏳ 待开始 |

**总体进度**: **~55-60%**

---

## 🎯 后续工作优先级

### 🔴 Critical (今天完成):

1. **铜氧化物战略重点** (Objective 3重写)

   - 时间: 2-3小时
   - 原因: 利用Kondo Lab 5/5契合度，最大化影响力
2. **trARPES完全保守化** (Objectives, Timeline, Outcomes)

   - 时间: 1-2小时
   - 原因: 避免over-promise不确定技术

### 🟡 High (明天完成):

3. **Timeline物理递进重写**

   - 时间: 3-4小时
   - 原因: 响应Kondo "define key physics questions over full term"
4. **Statement of Purpose修改**

   - 时间: 2-3小时
   - 原因: 直接提交给委员会的文档

### 🟢 Medium (后天完成):

5. **Publication Strategy细化**

   - 时间: 2小时
   - 原因: Physics narrative更convincing
6. **ResearchPlan.tex LaTeX修改**

   - 时间: 4-5小时
   - 原因: 实际提交的文档
7. **一致性验证** (RP ↔ SoP)

   - 时间: 1-2小时
   - 原因: 确保无矛盾

---

## ✅ 成功标准（修改后）

完成所有修改后，委员会应该看到:

### 物理深度 (not技术炫耀):

- ✅ **核心问题明确**: "Disentangle e-ph vs e-e" (不是"measure dynamics")
- ✅ **可测量量定量**: 12+物理量，含精度和单位
- ✅ **理论框架清晰**: Predictive, quantitative (not phenomenological)

### PhD级别野心:

- ✅ **5-year递进**: Foundation→Mechanism→Topology→Universality→Engineering
- ✅ **跨材料验证**: Kagome→**Cuprates**⭐→TMDs (universality)
- ✅ **风险平衡**: 4 low + 2 medium + 1 high risk (realistic moonshot)

### Kondo Lab对齐:

- ✅ **专长延续**: Equilibrium ARPES → Non-equilibrium
- ✅ **铜氧化物中心**: 5/5契合度，Year 4战略重点
- ✅ **技术现实**: Pump-probe主线 + trARPES潜在(不over-promise)

### 委员会视角:

- ✅ **独立性**: 明确的physics ownership (not just技术work)
- ✅ **可行性**: Realistic timeline, established techniques
- ✅ **影响力**: 3-5 PRB/PRL papers, 300-500 citations预期
- ✅ **培养价值**: 从学生→mentor→leader的清晰路径

---

## 📝 下一步立即行动

**建议工作顺序** (今天):

### Session 1 (上午, 3小时):

1. ✅ 完成铜氧化物Objective 3重写
2. ✅ 修改Objectives章节，完全去除trARPES依赖

### Session 2 (下午, 3小时):

3. ✅ Timeline重写（物理问题递进）
4. ✅ 开始SoP修改（Research Objectives, Why Kondo Lab段落）

### Session 3 (晚上, 2小时):

5. ✅ Publication Strategy细化（physics narrative）
6. ✅ 一致性检查（RP ↔ SoP关键数据）

**预计总时间**: 今天8小时可完成大部分核心修改
**剩余工作**: 明天LaTeX编译 + 最终验证 (~4-5小时)

---

**准备好开始吗？** 建议从**铜氧化物Objective 3重写**开始，因为这是最大的战略机会（5/5契合度！）
