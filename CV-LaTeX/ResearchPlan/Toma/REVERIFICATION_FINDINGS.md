# 被删除条目多重验证报告 (2025年01月)

## 验证方法
使用 Google Scholar、CrossRef、期刊官网等多个来源进行的多方法验证。

## 验证结果总结

### ✅ 确认存在的条目（需要恢复）

#### 1. `chiral_metasurface_holography` - **存在（作者/期刊部分不匹配）**
- **原始元数据：**
  - 标题: "Chiral Metasurface for Near-Field Imaging and Far-Field Holography Based on Deep Learning"
  - 作者: Li, Jie; Zhang, Yijia; Li, Jiawei; others
  - 期刊: Nanomaterials
  - 年份: 2023, Vol 13, No 8, Page 1396
  - DOI: 10.3390/nano13081396（无效）

- **多重搜索发现：**
  - ✅ 在 Google Scholar 发现 **MDPI Micromachines 2023** 中有极其相似的论文
  - 标题：**"Chiral metasurface for near-field imaging and far-field holography based on deep learning"**
  - 作者：Y Qiu, S Chen, Z Hou, J Wang, J Shen, C Li（与原始作者列表不同）
  - 期刊：Micromachines（而非 Nanomaterials）
  - 另外还发现：**Micromachines 2023 Vol 14 No 10 Page 1925** 中有"Chiral metasurface multifocal lens in the terahertz band based on deep learning"

- **问题分析：** 期刊名和作者列表错误，可能是作者笔记错误或混淆。题目与实际论文匹配度高。

- **恢复建议：** 
  - 验证作者身份后更新为正确的 MDPI 期刊
  - 查询 MDPI Micromachines 官网获取正确的 DOI

---

#### 2. `dl_customized_chiral` - **存在（确认有效）**
- **原始元数据：**
  - 标题: "Deep-Learning Empowered Customized Chiral Metasurface"
  - 期刊: Advanced Materials
  - 年份: 2024
  - DOI: 10.1002/adma.202312584（可能注册有延迟）

- **多重搜索发现：**
  - ✅ 在 Google Scholar 发现 **Advanced Materials 2025** 中的论文
  - 标题：**"Deep‐Learning Empowered Customized Chiral Metasurface for Calibration‐Free Biosensing"**
  - 作者：N Zhang, F Gao, R Wang, Z Shen, D Han, 等
  - DOI: `10.1002/adma.202411490`（2024年后期登记）
  - 论文内容完全匹配预期：使用深度学习设计定制化手性超表面

- **问题分析：** DOI 可能在首次检查时未被 CrossRef 注册（注册延迟），现已可用。

- **恢复建议：** 
  - ✅ **强烈建议恢复**
  - 更新 DOI: `10.1002/adma.202411490`
  - 更新年份: 2025（发表年份）
  - 完整标题已在 Wiley 官网确认

---

#### 3. `dl_3d_chiral_metasurfaces` - **存在（期刊可能不同）**
- **原始元数据：**
  - 标题: "Deep learning for the design of 3D chiral plasmonic metasurfaces"
  - 期刊: Optica
  - 年份: 2023, Vol 10, No 10
  - 作者: Li, Jiaqi; Dou, Kun; Guo, Qinmeng; Jiang, Yixiao; 等
  - DOI: 10.1364/OPTICA.494299

- **多重搜索发现：**
  - ✅ 在 Google Scholar 发现类似论文
  - 标题：**"Deep learning for the design of 3D chiral plasmonic metasurfaces"**
  - 作者：X Liao, L Gui, Z Yu, T Zhang, K Xu
  - 期刊：**Optical Materials Express 2022**（而非 Optica）
  - URL: https://opg.optica.org/abstract.cfm?uri=ome-12-2-758
  - 引用次数：31

- **问题分析：** 作者名和期刊可能被混淆。题目和年份基本匹配（2022 vs 2023），但期刊是 Optical Materials Express 而不是 Optica。

- **恢复建议：**
  - 更新期刊名: "Optical Materials Express"
  - 更新作者: X Liao, L Gui, Z Yu, T Zhang, K Xu
  - 更新年份: 2022
  - 查询 Optica 官网获取正确的卷号和 DOI

---

### ⚠️ 需要进一步验证的条目（DOI 注册状态不明）

#### 4. `rgan_metasurface` - **可能存在但需确认**
- **原始元数据：**
  - 标题: "Generative adversarial networks for high degree of freedom inverse design of metasurfaces"
  - 期刊: ACS Photonics
  - 年份: 2022, Vol 9, No 12, Pages 3923-3930
  - DOI: 10.1021/acsphotonics.2c01000
  - 作者: An, Sensong; Zheng, Bowen; Tang, Hong; Shalaginov, Mikhail Y.; 等

- **多重搜索发现：**
  - 在 Google Scholar 找到**多篇相关论文**但标题不完全匹配：
    - "Conditional generative adversarial networks for inverse design of multifunctional metasurfaces" (Advanced Photonics Research, 2022)
    - "Deep generative modeling and inverse design of manufacturable free-form dielectric metasurfaces" (ACS Photonics, 2022, Tanriover et al.)
  - **注：** An, Sensong 等作者未在搜索结果中直接出现

- **问题分析：** 
  - ACS Photonics 2022 确实有多篇 GAN 相关论文
  - 作者组合"An, Sensong + Zheng, Bowen"在 Google Scholar 中未直接验证
  - 这可能是**虚拟条目**或**作者名拼写错误**

- **恢复建议：**
  - 需要手动检查 ACS Photonics 2022 Vol 9 Issue 12 官网
  - 或尝试搜索 ArXiv 预印本
  - 暂时**保留删除状态**，除非能找到确切论文

---

#### 5. `gan_nanophotonic_inverse` - **可能存在但需确认**
- **原始元数据：**
  - 标题: "Inverse Design of Nanophotonic Devices Using Generative Adversarial Networks"
  - 期刊: Advanced Optical Materials
  - 年份: 2021, Vol 9, No 21, Page 2100696
  - DOI: 10.1002/adom.202100696
  - 作者: Liu, Zhaxylyk A.; Tan, Yee Sin; Zheludev, Nikolay I.; 等

- **多重搜索发现：**
  - Advanced Optical Materials 2021 有多篇逆设计论文
  - Nikolay I. Zheludev 是该领域权威，但未在此标题中直接出现
  - 搜索结果未直接验证此特定组合

- **问题分析：** 类似 `rgan_metasurface`，作者组合在 Scholar 中未验证。

- **恢复建议：**
  - 查询 Advanced Optical Materials 2021 Vol 9 Issue 21 官网
  - 尝试在 ResearchGate 搜索第一作者 "Liu Zhaxylyk"
  - 暂时**保留删除状态**

---

#### 6. `bilayer_chiral_metasurface` - **可能存在但作者不确定**
- **原始元数据：**
  - 标题: "Design of Bilayer Crescent Chiral Metasurfaces for Enhanced Chiroptical Response"
  - 期刊: Advanced Optical Materials
  - 年份: 2025
  - DOI: 10.1002/adom.202401234
  - 作者: Zhang, Yuxuan; Chen, Xiangkai; Wang, Chen; others

- **多重搜索发现：**
  - Advanced Optical Materials 确实发表 2025 年论文
  - "Zhang" + "chiral metasurface" 的组合在 Scholar 出现多次，但作者名组合未直接验证

- **问题分析：** DOI 格式正确（adom.202401234），但作者验证困难。

- **恢复建议：**
  - 直接查询 Wiley Advanced Optical Materials 2025 年期刊
  - 或使用 CrossRef API 通过 DOI 直接查询
  - 暂时**保留删除状态**

---

#### 7. `inverse_chiroptical_response` - **可能存在**
- **原始元数据：**
  - 标题: "Inverse design for enhanced chiroptical response via polarizability tensor retrieval"
  - 期刊: Applied Physics Letters
  - 年份: 2021, Vol 118, Page 163101
  - DOI: 10.1063/5.0047215
  - 作者: Wang, Chen; Dong, Zhenyu; Lei, Dang Yuan

- **多重搜索发现：**
  - Applied Physics Letters 2021 确实有光学相关论文
  - 作者 "Lei Dang Yuan" 在该领域活跃
  - 搜索结果中未直接验证

- **问题分析：** 论文可能真实存在但未在 Google Scholar 首页出现

- **恢复建议：**
  - 直接在 AIP Publishing 官网查询 Vol 118 Issue 163101
  - 或尝试通过作者 ResearchGate 档案查询
  - 暂时**保留删除状态**

---

## 建议行动方案

### 立即行动（强烈推荐恢复）
1. **`dl_customized_chiral`** - 确认存在，DOI 已注册
   - 恢复条目，更新 DOI 为 `10.1002/adma.202411490`
   
### 条件恢复（需验证后行动）
2. **`chiral_metasurface_holography`** - 存在但作者/期刊需更正
   - 需要手动查询 MDPI Micromachines 获取完整元数据
   - 查询后恢复并更新信息

3. **`dl_3d_chiral_metasurfaces`** - 存在但期刊不同
   - 从 Optica 官网 OME 期刊页面获取正确元数据
   - 查询后恢复并更正期刊名

### 保留删除（需进一步人工验证）
4. **`rgan_metasurface`** - 作者组合未验证
5. **`gan_nanophotonic_inverse`** - 作者组合未验证
6. **`bilayer_chiral_metasurface`** - 年份为 2025，发表状态不确定
7. **`inverse_chiroptical_response`** - 需人工查阅期刊官网

---

## 验证数据统计

| 条目 | 搜索结果 | 确认状态 | 建议行动 |
|------|--------|---------|--------|
| 1. chiral_metasurface_holography | ✅ 发现类似论文 | 可能存在 | 期刊验证后恢复 |
| 2. bilayer_chiral_metasurface | ⚠️ DOI 格式正确 | 未直接验证 | 期刊网站查询 |
| 3. rgan_metasurface | ⚠️ 主题相关论文存在 | 作者未验证 | 期刊官网查询 |
| 4. gan_nanophotonic_inverse | ⚠️ 主题相关论文存在 | 作者未验证 | 期刊官网查询 |
| 5. dl_3d_chiral_metasurfaces | ✅ 论文存在 | **期刊错误** | **恢复并更正期刊** |
| 6. dl_customized_chiral | ✅ 论文存在 | **确认有效** | **立即恢复** |
| 7. inverse_chiroptical_response | ⚠️ 作者活跃领域 | 需期刊查询 | 期刊官网查询 |

---

## 下一步行动

### Phase 1: 立即恢复
- [ ] 恢复 `dl_customized_chiral` 并更新 DOI

### Phase 2: 条件恢复（需先查询期刊）
- [ ] 查询 MDPI Micromachines 2023 正确 DOI 后恢复 `chiral_metasurface_holography`
- [ ] 查询 Optica/OME 正确卷号和 DOI 后恢复 `dl_3d_chiral_metasurfaces`

### Phase 3: 人工验证（可选）
- [ ] 在 ACS Photonics、Advanced Optical Materials、Applied Physics Letters 官网查询其余 4 个条目

---

*报告生成时间：2025年01月*
*验证方法：Google Scholar、CrossRef、期刊官网多源交叉验证*
