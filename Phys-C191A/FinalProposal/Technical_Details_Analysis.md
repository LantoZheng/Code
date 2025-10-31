# Technical Details Analysis for Quantum Money Inflation Project

**Date:** October 30, 2025  
**Authors:** Juncheng Ding, Tian Ariyaratrangsee, Xiaoyang Zheng  
**Course:** PHYS C191A - Quantum Computing

---

## Executive Summary

This document provides a comprehensive technical analysis of the quantum money inflation problem based on our Draft.md proposal and Professor Zhandry's "Quantum Lightning Never Strikes the Same State Twice" paper. We identify key theoretical concepts, mathematical models, implementation challenges, and open questions that need to be addressed in our final project.

---

## Part 1: Understanding the Inflation Problem

### 1.1 The Core Issue: No-Cloning ≠ No-Inflation

**Key Insight from Zhandry's Paper:**
- The **Quantum No-Cloning Theorem** prevents copying existing quantum states
- However, it does NOT prevent **unlimited generation of new valid quantum money states**
- This is the fundamental distinction between security (anti-counterfeiting) and economic stability (scarcity)

**Mathematical Framework:**
- Let `M` = minting algorithm (generates new valid quantum money states)
- Let `V` = verification algorithm (checks validity of quantum money)
- Let `Q(t)` = quantum computational power at time `t`
- Let `D` = computational difficulty of minting a new valid state

**Proposed Inflation Model:**
```
Minting Rate: R(t) ∝ Q(t) / D

If Q(t) grows exponentially (e.g., Q(t) = Q₀ · 2^(t/τ)), then:
R(t) = (Q₀ / D) · 2^(t/τ)

Total Money Supply: S(t) = ∫₀ᵗ R(τ) dτ ∝ 2^(t/τ) → ∞
```

**What We Need to Simulate (Part 1):**
1. **Classical analogy simulation:**
   - Model minting as a Poisson process with rate parameter λ(t) = Q(t)/D
   - Track cumulative money supply S(t)
   - Show S(t) → ∞ as Q grows exponentially

2. **Quantum circuit simulation (if time permits):**
   - Use Qiskit to implement simplified minting circuits
   - Measure success probability vs circuit depth/gates
   - Demonstrate how improved hardware (more qubits, lower error rates) increases minting rate

---

## Part 2: Existing Models and Their Limitations

### 2.1 Wiesner's Conjugate Coding (1983)

**Structure:**
- Bank generates |ψ⟩ = |b₁⟩ ⊗ |b₂⟩ ⊗ ... ⊗ |bₙ⟩
- Each |bᵢ⟩ ∈ {|0⟩, |1⟩, |+⟩, |-⟩} chosen randomly
- Bank keeps classical record of (i, basis, value)

**Verification:**
- Bank measures each qubit in the recorded basis
- If results match, note is valid

**Inflation Problem:**
- Minting complexity D = O(n) (just prepare n random qubits)
- No inherent scarcity mechanism
- **Unlimited issuance possible** with O(n) quantum operations

### 2.2 Zhandry's Quantum Lightning (2019)

**Key Innovation:** Public verification + collision-resistant serial numbers

**Construction (Degree-2 Polynomial Hash):**

Given security parameter λ, choose:
- n random upper-triangular matrices Aᵢ ∈ {0,1}^(m×m) for i=1,...,n
- Hash function: f_A(x) = (x^T · Aᵢ · x)ᵢ where operations are mod 2

**Bolt Generation:**
1. Generate superposition over collision sets:
   ```
   |ϕ₀⟩ = (1/2^(kn/2)) Σ_{Δ₁,...,Δₖ} |Δ₁,...,Δₖ⟩
   ```

2. Compute affine space S_Δ where all points collide under f_A

3. Create uniform superposition over S_Δ:
   ```
   |ϕ₁⟩ = Σ_Δ Σ_{x∈S_Δ} (1/(2^(kn/2)√|S_Δ|)) |Δ, x⟩
   ```

4. Measure f_A(x) to get serial number y:
   ```
   |⚡_y⟩ ∝ Σ_{Δ, x∈S_Δ : f_A(x)=y} (1/|S_Δ|) |x, x-Δ₁,...,x-Δₖ⟩
   ```

**Parameters for our analysis:**
- n = λ (security parameter)
- k = 2n
- m = kn = 2n² (input dimension)

**Verification Complexity:**
- Mini-verification: O(n²) gates per register
- Full verification: (k+1) × mini-verification = O(n³) gates

**Critical Question for Part 2.1:**
> **How does minting difficulty scale with quantum hardware improvements?**

**Hypothesis:**
If quantum hardware allows:
- Larger m (more input qubits)
- Deeper circuits (more gates)
- Lower error rates

Then the effective "cost" D of minting decreases, potentially leading to exponential inflation.

**Mathematical Analysis Needed:**
```
Let D_effective(Q) = D₀ / f(Q) where f(Q) captures hardware efficiency

If f(Q) ~ Q^α for some α > 0, then:
R(t) = Q(t) / D_effective(Q) = Q(t)^(1+α) / D₀

This grows even faster than exponential!
```

### 2.3 What We Must Prove/Simulate

**For Part 2.1 - Demonstrate Unlimited Inflation:**

1. **Theoretical Model:**
   - Define precise relationship between Q(t) and D_effective(Q)
   - Show mathematically that R(t) → ∞ under realistic hardware growth assumptions

2. **Simulation Evidence:**
   - Implement simplified bolt generation in Qiskit
   - Vary quantum resources (number of qubits, circuit depth)
   - Plot: Minting success rate vs. quantum resources
   - Extrapolate to show unbounded growth

**Key Metrics to Track:**
- Time to generate one valid bolt
- Number of circuit evaluations needed
- Gate count vs. success probability
- Parallel minting capability

---

## Part 3: Proposed Solution - Complexity-Based Issuance Control

### 3.1 Core Idea: Couple Minting Cost to Physical Resources

**Motivation from Zhandry's Paper:**
> "Typical assumptions in cryptography involve polynomial-time algorithms and inverse-polynomial success probabilities, rather than exponential."

**Our Proposal:** Introduce a **resource token** mechanism

**Modified Minting Protocol:**

1. **Resource Token Generation:**
   - Each minting attempt requires consuming a "resource token" RT
   - RT cost ∝ Hilbert space dimension of bolt being generated
   - RT generation has fixed physical cost (independent of Q)

2. **Mathematical Formalization:**
   ```
   Let d = 2^m be Hilbert space dimension for bolt
   Define: RT_cost(|ϕ⟩) = log₂(d) · E_unit
   
   Where E_unit is a fixed "energy quantum" independent of hardware
   ```

3. **Mint-with-Resource-Token Protocol:**
   ```python
   def mint_with_resource(A, RT_budget):
       required_RT = compute_hilbert_dimension(A)
       if RT_budget < required_RT:
           return INSUFFICIENT_RESOURCES
       
       # Generate bolt using Zhandry's protocol
       bolt = generate_bolt(A)
       
       # Consume resource tokens
       RT_budget -= required_RT
       
       return bolt, RT_budget
   ```

4. **Inflation Control:**
   - Total RT supply is bounded: RT_total = R_max
   - Minting rate now limited by RT consumption:
     ```
     R_bounded(t) ≤ R_max / RT_cost ≈ R_max / (m · n)
     ```
   - Even with exponential Q growth, R remains bounded!

### 3.2 Physical Realization Challenges

**Question:** Can we implement RT consumption in real quantum circuits?

**Possible Approaches:**

1. **Gate-Count-Based Penalty:**
   - Track cumulative gate count G across all minting attempts
   - Require G < G_max for acceptance
   - Problem: Doesn't capture true "resource" cost

2. **Decoherence-Aware Tokens:**
   - Exploit natural decoherence as a "cost" mechanism
   - Longer circuits → more decoherence → lower success probability
   - RT represents "coherence budget"
   
3. **Ancilla Qubit Consumption:**
   - Each minting consumes ancilla qubits permanently
   - Limited ancilla pool → limited minting
   - Most physically realistic but requires new circuit architecture

### 3.3 Mathematical Properties to Verify

**Theorem (to prove or conjecture):**
> If minting requires consuming RT ∝ log₂(dim(H)) where H is the state space, and total RT supply is bounded by R_max, then total money supply S(t) is bounded by:
> 
> S(∞) ≤ R_max / ⟨RT_cost⟩
> 
> where ⟨RT_cost⟩ is the average RT cost per valid bolt.

**What we need to show:**
1. RT mechanism doesn't break verification (polynomial-time verifiable)
2. RT mechanism doesn't enable new counterfeiting attacks
3. RT cost cannot be "cheated" by adversarial minting strategies

---

## Part 4: Implementation Strategy (Part 2.2-2.3)

### 4.1 Simplified Quantum Lightning in Qiskit

**Challenge:** Full Zhandry scheme requires m = 2n² qubits (e.g., n=10 → 200 qubits!)

**Our Approach:** Miniaturized version for proof-of-concept

**Mini-Lightning Parameters:**
- n = 3 (security parameter - toy value)
- k = 2 (collision set size)
- m = 12 (input dimension)

**Circuit Components:**

1. **Hash Function Implementation:**
   ```python
   def degree_2_hash_circuit(qc, x_reg, A_matrices, output_reg):
       """
       Compute f_A(x) = (x^T · A_i · x) for i=1,...,n
       in superposition
       """
       for i, A in enumerate(A_matrices):
           # Implement quadratic form
           for j in range(m):
               for k in range(j, m):
                   if A[j,k] == 1:
                       qc.ccx(x_reg[j], x_reg[k], output_reg[i])
   ```

2. **Collision Space Generation:**
   ```python
   def generate_collision_superposition(qc, delta_reg, x_reg, A_matrices):
       """
       Generate |ϕ₁⟩ state from Zhandry construction
       """
       # Create uniform superposition over Δ
       for q in delta_reg:
           qc.h(q)
       
       # Compute affine space S_Δ
       # (Simplified: use linear algebra solver classically)
       affine_space = compute_affine_space_classical(delta_reg, A_matrices)
       
       # Create uniform superposition over S_Δ
       # (This is the hard part - requires conditional state preparation)
   ```

3. **Verification Circuit:**
   ```python
   def mini_verify_bolt(qc, state_reg, A_matrices):
       """
       Project onto span of valid bolts and extract serial number
       """
       # Step 1: Uncompute to r-basis (Hadamard + phase estimation)
       for i in range(len(state_reg)):
           qc.h(state_reg[i])
       
       # Step 2: Measure to check if in valid subspace
       ancilla = QuantumRegister(1, 'ancilla')
       qc.measure(ancilla, classical_reg[0])
       
       # Step 3: If accepted, compute serial number
       serial_reg = QuantumRegister(n, 'serial')
       degree_2_hash_circuit(qc, state_reg, A_matrices, serial_reg)
       qc.measure(serial_reg, classical_serial)
   ```

### 4.2 Simulation Goals

**Experiment 1: Baseline Inflation (Part 1)**
- Measure minting rate R vs. circuit depth
- Vary: number of qubits (12 → 24 → 48)
- Plot: R(qubits) to show exponential growth
- Extrapolate: S(t) → ∞

**Experiment 2: Resource-Bounded Minting (Part 2.2)**
- Implement RT budget tracking
- Modify minting to check RT_cost before generation
- Plot: S(t) with and without RT mechanism
- Show: Bounded growth with RT

**Experiment 3: Verification Time Scaling (Part 2.3)**
- Measure verification gate count vs. n
- Confirm O(n³) scaling
- Check: Still polynomial even with RT mechanism

**Success Criteria:**
1. ✅ Clear demonstration that R → ∞ without intervention
2. ✅ RT mechanism successfully bounds S(t)
3. ✅ Verification remains polynomial-time
4. ✅ No new security vulnerabilities introduced

---

## Part 5: Critical Open Questions

### 5.1 Theoretical Questions

1. **Optimal RT Cost Function:**
   - Should RT_cost ∝ log(dim(H)) or dim(H) or something else?
   - What function ensures both scarcity AND usability?

2. **RT Generation Protocol:**
   - How are RTs initially distributed?
   - Can RTs be "recharged" over time? (Time-released cryptography?)
   - How to prevent RT market manipulation?

3. **Economic Stability:**
   - What happens when quantum hardware improves but RT supply is fixed?
   - Do we get deflation instead of inflation?
   - How to balance monetary policy?

4. **Security Implications:**
   - Does RT mechanism weaken no-cloning security?
   - New attack vectors via RT exhaustion?
   - Byzantine adversaries in RT distribution?

### 5.2 Implementation Questions

1. **Qiskit Limitations:**
   - Maximum practical circuit size (~30 qubits?)
   - Noise model accuracy for extrapolation?
   - Classical simulation vs. real quantum hardware

2. **Circuit Optimization:**
   - Can we reduce gate count for verification?
   - Parallel verification strategies?
   - Approximate verification trade-offs?

3. **Physical Realizability:**
   - Which RT mechanism is most implementable?
   - Current hardware capabilities?
   - Roadmap to practical deployment?

### 5.3 Evaluation Metrics (Part 3 Requirements)

**Success Criteria:**

| Metric | Target | Evaluation Method |
|--------|--------|-------------------|
| Inflation Rate Reduction | R_bounded / R_unbounded < 0.01 | Simulation comparison |
| Verification Time | O(n³) confirmed | Gate count analysis |
| Security Preservation | No new attacks found | Adversarial analysis |
| Scarcity Maintenance | P(collision) < 2^(-λ) | Statistical testing |
| Usability | Verification < 1s @ n=20 | Circuit execution time |

---

## Part 6: References and Mathematical Background

### 6.1 Key Concepts from Zhandry Paper

**No-Cloning Theorem:**
```
For any unitary U and states |ψ⟩, |φ⟩:
U(|ψ⟩ ⊗ |0⟩) = |ψ⟩ ⊗ |ψ⟩  for all |ψ⟩  ⟹  |ψ⟩ ∝ |φ⟩

I.e., universal cloning machine is impossible
```

**No-Conversion Theorem (Theorem in §4.2):**
```
For sequences of states S₁ = {|ψᵢ⟩}, S₂ = {|φᵢ⟩}
and any CPTP map M:

F²(M) ≤ d · λ₁(C_{S₁,S₂,D})

where d = dimension, C = Gram-like matrix, λ₁ = max eigenvalue
```

**Implication:** Even with quantum operations, converting |ψᵢ⟩ → |φᵢ⟩ with high fidelity is bounded.

### 6.2 Complexity Classes

**Assumption 1 (§5.1):** 2(k+1)-Non-Affine Multi-Collision Resistance (NAMCR)
- It's computationally hard to find 2(k+1) colliding inputs under f_A
- That are NOT affinely related
- For random degree-2 polynomial hash f_A

**Why this matters for inflation:**
If adversary can efficiently generate many collisions, they can:
1. Create many bolts with SAME serial number (counterfeiting)
2. OR create many bolts with DIFFERENT serial numbers (inflation!)

Our RT mechanism must prevent (2) without breaking (1)'s security.

### 6.3 Relevant Theorems to Cite

1. **Wiesner (1983):** Original quantum money with private verification
2. **Aaronson-Christiano (2012):** First public-key quantum money (later broken)
3. **Zhandry (2019):** Quantum Lightning from degree-2 hashes
4. **Unruh (2016):** Collapsing hash functions
5. **Aaronson (2016):** Complexity of quantum states lecture notes

---

## Part 7: Timeline with Technical Milestones

### Week 1 (Oct 30 - Nov 10): Baseline Simulation
- [ ] Implement degree-2 hash function classically (Python/NumPy)
- [ ] Build collision-finding algorithm (verify 2.1 analysis)
- [ ] Create inflation rate model: R(Q) function
- [ ] Plot S(t) for exponential Q(t) growth
- **Deliverable:** Plots showing unbounded inflation

### Week 2 (Nov 10 - Nov 17): Quantum Circuit Implementation
- [ ] Set up Qiskit environment (mini-lightning parameters)
- [ ] Implement hash circuit (n=3, m=12)
- [ ] Build bolt generation circuit (simplified)
- [ ] Measure gate count vs. qubit count
- **Deliverable:** Working Qiskit minting prototype

### Week 3 (Nov 17 - Nov 24): Resource Token Design
- [ ] Define RT_cost function mathematically
- [ ] Implement RT tracking in simulation
- [ ] Modify minting protocol to consume RT
- [ ] Analyze security implications
- **Deliverable:** RT-bounded minting implementation

### Week 4 (Nov 24 - Nov 30): Comparative Evaluation
- [ ] Run simulations: unbounded vs. bounded
- [ ] Generate comparison plots
- [ ] Statistical analysis of scarcity
- [ ] Verification time measurements
- **Deliverable:** Experimental results & analysis

### Week 5 (Nov 30 - Dec 5): Report & Poster
- [ ] Write final report (all 4 parts)
- [ ] Create visualization for poster
- [ ] Prepare defense arguments
- **Deliverable:** Final paper draft

### Week 6 (Dec 5 - Dec 9): Finalization
- [ ] Revise based on feedback
- [ ] Practice poster presentation
- [ ] Prepare for Q&A
- **Deliverable:** Poster & defense ready

---

## Part 8: Risk Analysis

### High-Risk Items

1. **Qiskit circuit too large**
   - Mitigation: Use smaller parameters (n=2 or n=3)
   - Fallback: Classical simulation of quantum behavior

2. **RT mechanism breaks security**
   - Mitigation: Formal security proof (sketch level)
   - Fallback: Acknowledge as open problem, propose mitigation

3. **Time constraints**
   - Mitigation: Focus on Part 1 & 2.1 first (core contribution)
   - Defer Part 2.3 (physical realizability) if needed

### Medium-Risk Items

4. **Simulation results unclear**
   - Mitigation: Multiple visualization strategies
   - Get feedback early from instructor/TA

5. **Mathematical rigor**
   - Mitigation: Cite Zhandry's theorems, adapt proofs
   - Acceptable to make plausible conjectures with evidence

---

## Part 9: Code & Data Organization

### Recommended Repository Structure
```
Phys-C191A/FinalProject/
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
├── data/                              # Simulation results
│   ├── inflation_unbounded.csv
│   ├── inflation_bounded.csv
│   └── verification_timings.csv
├── notebooks/                         # Jupyter notebooks
│   ├── 01_degree2_hash_analysis.ipynb
│   ├── 02_inflation_simulation.ipynb
│   ├── 03_quantum_circuits.ipynb
│   └── 04_rt_mechanism.ipynb
├── src/                               # Source code
│   ├── hash_functions.py             # Degree-2 polynomial hash
│   ├── collision_finder.py           # Multi-collision algorithm
│   ├── quantum_lightning.py          # Qiskit circuits
│   ├── resource_tokens.py            # RT mechanism
│   └── visualization.py              # Plotting utilities
├── tests/                             # Unit tests
│   ├── test_hash.py
│   ├── test_collision.py
│   └── test_circuits.py
├── docs/                              # Documentation
│   ├── Mathematical_Proofs.pdf
│   └── Technical_Details_Analysis.md  # This file!
└── report/                            # Final deliverables
    ├── Final_Report.tex
    ├── Poster.pdf
    └── Presentation_Slides.pdf
```

### Key Dependencies
```txt
# requirements.txt
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
qiskit>=0.45.0
qiskit-aer>=0.13.0
jupyter>=1.0.0
sympy>=1.12        # For symbolic math
pytest>=7.4.0      # For testing
```

---

## Part 10: Discussion Points for Group Meeting

### Immediate Decisions Needed:

1. **Parameter choices:**
   - What n, k, m for our "toy" implementation?
   - Trade-off: realism vs. computational feasibility

2. **RT cost function:**
   - Linear in log(dim)? Or square root? Or exponential?
   - What gives most meaningful economic behavior?

3. **Division of labor:**
   - Who focuses on mathematical proofs?
   - Who implements Qiskit circuits?
   - Who writes report/makes poster?

4. **Evaluation priorities:**
   - Focus on clear demonstration of inflation problem? (safer)
   - Or emphasize novel RT solution? (higher risk, higher reward)

### Questions for Professor/TA:

1. Is simplified parameter regime (n=3) acceptable for demonstration?
2. Can we cite Zhandry's hardness assumption without proving it?
3. How much mathematical rigor expected for "conjecture" statements?
4. Is classical simulation of quantum inflation sufficient, or must we use real Qiskit circuits?

---

## Conclusion

This analysis reveals that the quantum money inflation project has clear technical depth:

**Core Technical Challenges:**
1. Modeling inflation dynamics in quantum systems
2. Understanding Zhandry's quantum lightning construction
3. Designing resource-bounded minting mechanisms
4. Implementing and simulating in Qiskit
5. Proving security properties are preserved

**Novel Contributions:**
1. First quantitative analysis of quantum money inflation
2. Proposal of resource-token mechanism for scarcity control
3. Simulation-based validation of economic stability
4. Bridge between cryptographic security and economic soundness

**Feasibility:** High, if we:
- Use simplified parameters for proof-of-concept
- Focus on simulation over real quantum hardware
- Accept conjectures with evidence rather than full proofs
- Iterate on feedback from instructor

**Impact:** This work addresses a fundamental gap between quantum cryptography (security) and practical digital currency (economic stability), making it both theoretically interesting and potentially impactful for future quantum monetary systems.

---

## Appendix: Mathematical Notation Reference

| Symbol | Meaning |
|--------|---------|
| \|ψ⟩ | Quantum state (ket notation) |
| ⟨ψ\| | Dual state (bra notation) |
| ⊗ | Tensor product |
| H | Hadamard gate |
| λ | Security parameter |
| n | Number of hash outputs |
| m | Input dimension |
| k | Collision set size |
| Q(t) | Quantum computational power |
| D | Minting difficulty |
| R(t) | Minting rate |
| S(t) | Total money supply |
| RT | Resource token |
| f_A | Degree-2 polynomial hash |
| \|⚡⟩ | Lightning bolt state |

---

**Document Version:** 1.0  
**Last Updated:** October 30, 2025  
**Status:** Ready for group review and implementation planning
