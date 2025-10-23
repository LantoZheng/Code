# Measurable Physical Observables - PhD Research Plan

**目的**: 响应Kondo教授建议"Define measurable observables"，明确每个实验目标的定量物理量

---

## 1. 可测量物理量分类体系

### 1.1 能量尺度 (Energy Scales) - meV精度

| 物理量 | 符号 | 定义 | 典型值 | 测量方法 | 物理意义 |
|-------|------|------|--------|----------|----------|
| **瞬态能量移动** | $\Delta E(t)$ | Pump后能带位置时间演化 | 10-100 meV | 反射率光谱峰位移动 | 声子软化/电子温度 |
| **CDW能隙演化** | $\Delta_{\text{CDW}}(t)$ | CDW gap magnitude时间依赖 | $\Delta_0 \sim 30$ meV | Fano/Lorentzian拟合 | CDW序参量强度 |
| **带宽重整化** | $W(t)$ | 电子带宽的瞬态变化 | $\Delta W \sim 50-200$ meV | 光谱权重积分 | 关联强度变化 |
| **Van Hove点移动** | $\Delta E_{\text{VH}}(t)$ | Van Hove singularity能量移动 | 5-30 meV | DOS峰位追踪 | 拓扑能带响应 |

**实验精度要求**:
- 能量分辨率: ≤ 5 meV (光谱仪分辨率)
- 信噪比: SNR > 100:1 (需平均≥1000次shots)
- 温度稳定性: ±0.1 K

---

### 1.2 时间尺度 (Time Scales) - fs-ps精度

| 物理量 | 符号 | 定义 | 典型值 | 提取方法 | 物理过程 |
|-------|------|------|--------|----------|----------|
| **电子-电子热化** | $\tau_{e-e}$ | 电子系统内部热平衡时间 | 50-100 fs | 指数拟合上升沿 | 库仑散射 |
| **电子-声子耦合** | $\tau_{e-ph}$ | 能量传递到晶格的时间 | 0.5-2 ps | 指数拟合衰减 | e-ph相互作用 |
| **CDW恢复时间** | $\tau_{\text{CDW}}$ | CDW重新建立的时间 | 5-50 ps | S型曲线拟合 | 序参量动力学 |
| **相干时间** | $\tau_{\text{coh}}$ | 相干振荡的衰减时间 | 1-5 ps | FFT后拟合包络 | 退相干机制 |
| **声子周期** | $T_{\text{ph}}$ | A₁g模式振荡周期 | ~300 fs ($\sim 10$ THz) | FFT peak | 声子频率 |

**实验精度要求**:
- 时间分辨率: ≤ 50 fs (交叉相关宽度)
- 延迟线精度: ±5 fs (机械stage)
- 时间窗口: -500 fs 至 +100 ps

---

### 1.3 耦合强度 (Interaction Strengths) - 无量纲

| 物理量 | 符号 | 定义 | 典型值 | 提取方法 | 理论框架 |
|-------|------|------|--------|----------|----------|
| **电子-声子耦合** | $\lambda$ | 无量纲耦合常数 | 0.3-0.8 | $\lambda = \frac{\Delta_0}{k_B T_c}$ (BCS-like) | McMillan公式 |
| **准粒子权重** | $Z$ | 质量增强因子 | $m^*/m = 2-5$ | $Z = \frac{W_{\text{exp}}}{W_{\text{DFT}}}$ | Fermi液体理论 |
| **关联强度** | $U/W$ | Hubbard U vs 带宽比 | 0.5-2 | 对比DFT+DMFT | Mott物理 |
| **CDW阶参量** | $\langle \psi \rangle$ | 复序参量幅值 | $\|\psi\| = 0-1$ | 从$\Delta_{\text{CDW}}$归一化 | Landau-Ginzburg |

---

### 1.4 动量空间 (Momentum Space) - k分辨

| 物理量 | 符号 | 定义 | 典型值 | 测量方法 | 物理意义 |
|-------|------|------|--------|----------|----------|
| **带选择响应** | $A_i(\mathbf{k}, t)$ | 轨道i的谱函数时间演化 | 0-100 (a.u.) | 泵浦能量调谐 + trARPES | 轨道动力学 |
| **Fermi面动力学** | $k_F(t)$ | Fermi动量的时间变化 | 0.1-0.5 Å⁻¹ | Fermi edge追踪 | 电子结构响应 |
| **CDW嵌套矢量** | $Q_{\text{CDW}}$ | CDW嵌套的高对称点 | (1/3, 1/3)或类似 | 倒空间强度模式 | CDW稳定性 |

---

## 2. Objective-Specific Measurable Targets

### Objective 1: E-ph vs E-e Disentanglement (Year 1-2)

**Primary Observables**:
- [ ] $\tau_{e-e}$ in CsV₃Sb₅ @ T = 10-30 K (extract from reflectivity rise time)
- [ ] $\tau_{e-ph}$ from phonon decay timescale
- [ ] $\lambda$ = $\frac{\Delta_0}{k_B T_c}$ estimation from BCS-like analysis
- [ ] $\Delta E(t)$ band position shift (meV level)

**Success Criteria**:
- ✅ Quantitative disentanglement: $\tau_{e-e} \ll \tau_{e-ph}$ or vice versa conclusively shown
- ✅ Publication in Physical Review B with data tables
- ✅ Error bars < 10% on time constants

### Objective 2: Correlation-Topology Interplay (Year 3)

**Primary Observables**:
- [ ] $Z(k)$ momentum-dependent mass enhancement across Brillouin zone
- [ ] $A_i(\mathbf{k}, t)$ band-selective dynamics at Van Hove + Dirac points
- [ ] $\Delta E_{\text{VH}}(t)$ Van Hove singularity shift timescale
- [ ] Comparison: $Z$ at different k → topology dependence?

**Success Criteria**:
- ✅ First momentum-resolved ultrafast data in kagome system
- ✅ Clear evidence: topology enhances/suppresses correlation effects
- ✅ Publication in PRL or Nature Communications

### Objective 3: Cuprate Pseudogap (Year 4)

**Primary Observables**:
- [ ] $\Delta_{\text{PG}}(T, t)$ pseudogap dynamics vs temperature
- [ ] $\tau_{\text{PG}}$ pseudogap relaxation timescale (compare to superconducting gap)
- [ ] $\Delta(φ, t)$ d-wave anisotropy in non-equilibrium
- [ ] Polarization-resolved: validate d-wave symmetry

**Success Criteria**:
- ✅ First direct time-domain pseudogap measurement
- ✅ Resolves: PG precursor vs competing order question
- ✅ Publications in PRB + PRX with complementary cuprate datasets

### Objective 4: Photo-induced Phases (Year 5, High-Risk)

**Primary Observables**:
- [ ] Transient order parameter dynamics $\langle \psi_{\text{hidden}} \rangle(t)$
- [ ] Lifetime of photo-induced state
- [ ] Recovery mechanism vs equilibrium

**Success Criteria** (OR outcomes):
- ✅ Discovery: evidence for long-lived photo-induced phase, OR
- ✅ Null result: "No stable photo-induced phase observed" in high-quality dataset (publishable)

---

## 3. 与Research Plan的对应关系

每个Year的Physics Question对应的Measurable Observables:

```
Year 1-2: "What drives CDW?"
├─ E-ph vs E-e: τ_e-e, τ_e-ph, λ
└─ Publication: Quantitative phase diagram (PRB)

Year 3: "Does topology matter?"
├─ Correlation-topology: Z(k), A_i(k,t), ΔE_VH(t)
└─ Publication: Breakthrough discovery (PRL/Nat.Comm.)

Year 4: "Is method universal?"
├─ Cuprates: Δ_PG(T,t), τ_PG, Δ(φ,t)
└─ Publications: 2× on pseudogap + d-wave (PRB/PRX)

Year 5: "Hidden phases?"
├─ Photo-induced: ⟨ψ_hidden⟩(t), lifetime
└─ Publication: Capstone paper or confirmatory null result
```

---

## 4. 实验可行性评估

### 高可能性 (Green) ✅
- $\tau_{e-e}$, $\tau_{e-ph}$: 标准泵浦探针，CsV₃Sb₅易得
- $\Delta E(t)$: 反射率光谱常规分析
- $\lambda$: BCS估计从已知$\Delta_0$和$T_c$

### 中等可能性 (Yellow) 🟡
- $Z(k)$ momentum-resolved: 需要trARPES，但Kondo Lab正开发中
- $\Delta_{\text{PG}}(T,t)$ in cuprates: 样品复杂，需多态备样

### 低可能性 (Red) 🔴  
- Photo-induced phases: 高能量、易损伤样品、信号微弱
- 但即使失败，良好null结果也有出版价值

---

## 5. 精度与误差管理

| 物理量 | 目标精度 | 误差来源 | 缓解策略 |
|-------|--------|---------|---------|
| $\tau_{e-e}$ | ±10% | 仪器交叉相关、拟合偏差 | 多泵浦能量平均、理论对比 |
| $\Delta E(t)$ | ±5 meV | 能量校准、漂移 | 实时校准光谱仪、温度稳定 |
| $\lambda$ | ±0.1 | 理论模型假设 | 与DFT+DMFT交叉验证 |
| $Z$ | ±0.5 | DFT计算不准、测量误差 | 多个k点平均、误差传播 |

---

**总结**: 12+个精确可测量物理量为PhD研究提供量化成功标准，回应Kondo教授"define measurable observables"的建议。
