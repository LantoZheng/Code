

### **Title**

Intelligent Adaptive Optics for Deep-Tissue Hyperspectral Stimulated Raman Scattering Microscopy

### **Introduction**

Stimulated Raman Scattering (SRS) microscopy is a revolutionary label-free imaging technique that provides real-time chemical contrast based on intrinsic molecular vibrations, enabling profound insights into biological systems.1 The Ozeki Laboratory at the University of Tokyo stands at the forefront of this field, having developed world-leading SRS systems characterized by exceptional imaging speed, hyperspectral capabilities, and quantum-enhanced sensitivity.4 However, a fundamental physical barrier currently limits the full potential of these advanced instruments: optical aberrations induced by the biological tissue itself. As light penetrates deep into complex samples like organoids or brain tissue, its wavefront becomes distorted, severely degrading image resolution, contrast, and signal strength, thus constraining the effective imaging depth.7

This research proposal addresses this central problem by proposing the development and integration of an **Intelligent Adaptive Optics (iAO)** system into the laboratory's existing SRS microscopes. The core of this study is to employ a spatial light modulator to actively correct for tissue-induced aberrations. Critically, we will pioneer a novel control method driven by deep learning, which promises to overcome the speed and accuracy limitations of conventional AO algorithms. The successful implementation of this project is significant because it will directly tackle the primary bottleneck in deep-tissue SRS imaging. By restoring diffraction-limited performance in highly scattering environments, this work will empower the Ozeki Lab's state-of-the-art technology to investigate complex biological questions in more physiologically relevant models, opening new frontiers in fields such as neurobiology, cancer research, and metabolic studies.

### **Background**

To understand the context of this proposal, it is essential to grasp two key concepts: the principles of SRS microscopy and the challenge of optical aberrations. SRS microscopy utilizes two synchronized laser pulses (pump and Stokes) to coherently amplify a specific molecular vibrational signal, allowing for rapid, quantitative, and chemically specific imaging without the need for fluorescent labels.1 This has made it an invaluable tool for observing lipids, proteins, and other biomolecules in living systems. However, the efficiency of this nonlinear optical process is critically dependent on achieving a tight, diffraction-limited laser focus within the sample. When imaging deep within biological tissue—a turbid and optically inhomogeneous medium—the laser wavefront is severely distorted. This phenomenon, known as optical aberration, scatters photons, broadens the focal spot, and drastically reduces the signal intensity and spatial resolution, creating a "soft limit" on achievable imaging depth.7

The Ozeki Laboratory has established a world-class research program focused on advancing SRS technology. Their work can be summarized by three main pillars: 

(1) **High-Speed Hyperspectral Imaging**, achieved through the development of novel, rapidly tunable fiber laser sources that enable the acquisition of rich chemical information across a wide spectral range at near-video rates 4; 

(2)**Quantum-Enhanced Sensitivity**, a pioneering effort to surpass the standard quantum limit of detection by incorporating "squeezed light" to reduce shot noise, thereby enabling imaging at lower, less phototoxic power levels 2;

(3)**High-Throughput Analysis**, integrating SRS with microfluidics and machine learning to perform chemical phenotyping of tens of thousands of single cells.4

Despite these remarkable advances in signal generation, detection, and data analysis, a systematic review of the lab's publications reveals that active wavefront correction, specifically through adaptive optics (AO), has not been a primary research focus.12 AO is the gold-standard technique for compensating for optical aberrations in real-time.8 This proposal identifies a critical research gap: the absence of an AO system prevents the lab's cutting-edge technologies from being effectively applied to the thick, scattering samples that are of paramount biological interest. This study builds directly upon the lab's existing strengths by introducing a missing, enabling technology. By solving the aberration problem, this research will unlock the full potential of the lab's hyperspectral and quantum-enhanced systems for deep-tissue biological discovery.

### **Research Methodology**

This study is an experimental and computational project designed to develop, validate, and apply a novel intelligent adaptive optics system for SRS microscopy. The research will be conducted in three distinct phases over a two-year period.

**Phase 1 : Design, Integration, and Validation of a Polychromatic AO-SRS Microscope**

The initial phase focuses on constructing the core hardware. An optical relay system will be designed to integrate a reflective liquid-crystal-on-silicon spatial light modulator (LCoS-SLM) 16 into an existing SRS microscope, placing it conjugate to the objective's back focal plane. A key design challenge is the polychromatic nature of SRS, requiring simultaneous correction for both the pump (\~800 nm) and Stokes (\~1040 nm) beams; this will be addressed through careful optical design to minimize chromatic errors. A baseline control system will be developed in Python, implementing a classic sensorless AO algorithm, such as a Zernike mode-based hill-climbing algorithm.18 This approach, which iteratively adjusts aberration modes to maximize an image quality metric (e.g., total SRS signal), will serve as a functional benchmark. The system's performance will be rigorously validated using standard samples (e.g., polystyrene beads in scattering phantoms) to quantify the improvement in signal intensity and the restoration of the point spread function (PSF) at various depths.

**Phase 2 : Development of a Deep Learning-Driven Sensorless AO Framework**

This phase represents the core innovation of the project. We will replace the slow, iterative hill-climbing algorithm with a predictive deep learning model. A large-scale training dataset will be generated by using the Phase 1 system to systematically apply thousands of known, random aberrations with the SLM and capturing the corresponding degraded SRS images. A convolutional neural network (CNN) will then be designed and trained using the PyTorch framework.21 The network will be trained to solve an image-to-vector regression task: inputting a single aberrated SRS image and outputting the precise set of Zernike coefficients required to correct it. This "single-shot" prediction approach is expected to be orders of magnitude faster and more robust than iterative methods. The performance of this intelligent AO (iAO) controller will be quantitatively compared against the baseline algorithm from Phase 1 in terms of correction speed, accuracy, and robustness to noise.

**Phase 3 : Application in Advanced Biological Imaging and Development of a Semi-Supervised Segmentation Pipeline**

In the final phase, the fully optimized iAO-SRS system will be applied to a challenging biological problem relevant to the Ozeki Lab's interests, such as imaging metabolic dynamics in 3D tumor spheroids or mapping myelination in thick brain tissue slices.22 A significant challenge in analyzing the resulting large, complex datasets is the difficulty of obtaining pixel-perfect annotations for training segmentation models. To address this, we will develop a

**semi-supervised learning (SSL)** workflow.23 This approach will leverage a small amount of manually labeled data from clear, superficial image regions to train an initial segmentation network (e.g., U-Net). This model will then be used to generate "pseudo-labels" for the vast amount of unlabeled data from deeper tissue regions. Advanced techniques like consistency regularization (e.g., Mean Teacher 24) and tailored data augmentation strategies 27 will be employed to ensure the model learns robust features from these imperfect labels.

**Data Analysis and Evaluation**

The performance of the AO system will be evaluated using standard image quality metrics such as Peak Signal-to-Noise Ratio (PSNR) and the Structural Similarity Index (SSIM).30 The accuracy of the biological image segmentation models will be rigorously assessed using metrics appropriate for medical imaging, primarily the Dice Similarity Coefficient (DSC) and Intersection over Union (IoU), which are robust to class imbalance.33

### **Qualifications**

I am uniquely qualified to undertake this research due to a combination of hands-on experience in adaptive optics, computational optics, and machine learning, supported by a strong foundation in physics.

* **Adaptive Optics Hardware and Control:** My undergraduate project, "Self-calibrating Beam Shaping Based on Reflective Spatial Light Modulator," provided me with end-to-end experience in designing, building, and programming a complete AO system. This included integrating an SLM, using a wavefront sensor, and implementing feedback control algorithms in Python—skills that are directly transferable to Phase 1 of this proposal.21  
* **Machine Learning and Computational Optics:** In the "Single-layer Diffractive Neural Network (D2NN)" project, I used the PyTorch framework to design and train an optical neural network, achieving over 97% accuracy on the MNIST dataset through optical simulation. This project demonstrates my proficiency with the exact deep learning tools required for Phase 2 and my ability to apply them to solve complex problems at the intersection of optics and AI.21  
* **Physics and Simulation Foundation:** My physics major has provided me with a deep understanding of the underlying principles of nonlinear optics (essential for SRS) and quantum mechanics (relevant to the lab's advanced projects). Furthermore, my experience with FDTD and COMSOL simulations will be invaluable for modeling the AO-SRS system prior to and during its construction.21

The following table explicitly maps my skills to the project's needs:

### **Conclusion**

This research project directly addresses a critical bottleneck—tissue-induced optical aberrations—that currently limits the application of the Ozeki Laboratory's world-class SRS microscopy technologies. The proposed development of an intelligent, deep learning-driven adaptive optics system is a novel approach that leverages my specific expertise in both optical engineering and machine learning to create a powerful new capability for the lab. The primary implication of this study is the significant enhancement of imaging depth and quality in complex biological samples. This will, in turn, enable new avenues of scientific inquiry, allowing for the label-free, quantitative chemical analysis of dynamic processes deep within physiologically relevant models such as tumor spheroids and brain tissue. By bridging the gap between cutting-edge instrumentation and challenging biological applications, this research promises to make a substantial contribution to the fields of biophotonics and biomedical imaging.

### **References**

1 Freudiger, C. W. et al. Label-Free Biomedical Imaging with High Sensitivity by Stimulated Raman Scattering Microscopy.Science 322, 1857–1861 (2008).

2 Ozeki, Y. et al. Quantum-Enhanced Stimulated Raman Scattering Microscopy. J. Opt. Soc. Am. B 37, 3288 (2020).

3 Ozeki, Y. et al. Analysis and experimental assessment of the sensitivity of stimulated Raman scattering microscopy. Opt. Express 17, 3651–3658 (2009).  
4 Ozeki, Y. et al. High-speed molecular spectral imaging of tissue with stimulated Raman scattering.Nature Photon. 6, 845–851 (2012).  
5 Ozeki, Y., Asai, T., Shou, J. & Yoshimi, H. Multicolor stimulated Raman scattering microscopy with fast wavelength-tunable Yb fiber laser.IEEE Journal of selected topics in quantum electronics 25, 1-11 (2018).  
11 Ozeki, Y. et al. Stimulated Raman hyperspectral imaging based on spectral filtering of broadband fiber laser pulses.Opt. Lett. 37, 431–433 (2012).  
12 Ma, Y., Mizuguchi, T., Spratt, S. J., & Ozeki, Y. Label-free organelle image prediction using deep learning and large-scale hyperspectral stimulated Raman scattering.Photonics West, BiOS, paper 13332-70 (2025).  
37 Suzuki, Y. et al. Label-free chemical imaging flow cytometry by high-speed multicolor stimulated Raman scattering.Proc. Natl. Acad. Sci. U.S.A. 116, 15842–15847 (2019).  
6 Xu, Z. et al. Picosecond pulsed squeezing at 844 nm with a PPLN waveguide.  
12th Asia-Pacific Laser Symposium (APLS2023), CTu1-03 (2023).  
15 Ozeki, Y. Recent Advances in Stimulated Raman Scattering Microscopy.  
2nd Advanced Forum on Chemical Imaging Technology and Applications (2025).  
13 Kobayashi, H. et al. Label-free detection of cellular drug responses by high-throughput bright-field imaging and machine learning.  
Scientific reports 7, 12454 (2017).  
38 Ozeki, Y. et al. Label-free chemical imaging flow cytometry by high-speed multicolor stimulated Raman scattering.  
Lab on a Chip 20, 2263-2273 (2020).  
14 Oda, R., Shou, J., Shiramizu, B., & Ozeki, Y. High speed imaging of B-cells by stimulated Raman scattering.  
Proc. SPIE 11252, 112520W (2020).  
7 Wang, W. & Huang, Z. Phase-controlled stimulated Raman scattering microscopy for deep tissue 3D chemical imaging.  
Opto-Electron. Adv. (2024).  
8 Wang, W. & Huang, Z. Polychromatic Adaptive Optics-Assisted Stimulated Raman Scattering Microscopy Enables Deep Tissue Chemical Imaging.  
Laser & Photonics Reviews (2025).  
9 Luna, S. K. & Evans, C. L. Adaptive optics stimulated Raman scattering microscopy for topical product pharmacokinetic tomography.  
Proc. SPIE 13315, 133150E (2025).  
10 Ji, M. et al. Epi-detected and transmitted stimulated Raman scattering microscopy for deep tissue imaging.  
J. Biomed. Opt. 25, 1 (2020).  
21 Zheng, X. Curriculum Vitae. (2025).  
16 Holoeye Photonics AG. HES 6001-VIS Phase Only Spatial Light Modulator.

17 Thorlabs, Inc. EXULUS-HD3HP \- 1920 x 1200 LCoS-SLM, 650-1100 nm.

18 Booth, M. J. Wave front sensor-less adaptive optics: a model-based approach using sphere packings.

Opt. Express 14, 1339–1352 (2006).  
19 Débarre, D., Botcherby, E. J., Watanabe, T., Kara, P., & Booth, M. J. Image-based adaptive optics for two-photon microscopy.  
Opt. Lett. 34, 2495–2497 (2009).  
20 Tao, X., Liu, W., & Li, D. Modified hill-climbing algorithm based on Zernike modes for wavefront sensorless adaptive optics.  
Appl. Opt. 52, 4443–4449 (2013).  
22 Ji, M. et al. Rapid, label-free detection of brain tumors with stimulated Raman scattering microscopy.  
Sci. Transl. Med. 5, 201ra119 (2013).  
23 Ouali, Y., Hudelot, C. & Tami, M. An Overview of Deep Semi-Supervised Learning.  
arXiv \[cs.LG\] (2020).  
24 Tarvainen, A. & Valpola, H. Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results.  
Advances in neural information processing systems 30 (2017).  
25 Cheplygina, V., de Bruijne, M. & Pluim, J. P. W. Not-so-supervised: a survey of semi-supervised, multi-instance, and weakly supervised learning in medical image analysis.  
Medical Image Analysis 54, 280–296 (2019).  
26 Yu, L. et al. Uncertainty-aware Mean Teacher for Semi-supervised Medical Image Segmentation.  
Medical Image Computing and Computer Assisted Intervention – MICCAI 2019, 436–444 (2019).  
27 Chlap, P., Min, H., Vandenberg, N., Dowling, J., Holloway, L., & Haworth, A. A review of medical image data augmentation techniques for deep learning applications.  
Journal of Medical Imaging and Radiation Oncology, 65(5), 545-563 (2021).  
28 Taylor, L., & Nitschke, G. Improving deep learning using generic data augmentation.  
arXiv \[cs.LG\] (2017).  
29 Shorten, C., & Khoshgoftaar, T. M. A survey on Image Data Augmentation for Deep Learning.  
Journal of Big Data, 6(1), 60 (2019).  
33 Taha, A. A. & Hanbury, A. Metrics for evaluating 3D medical image segmentation: analysis, selection, and tool.  
BMC Med Imaging 15, 29 (2015).  
34 Müller, D. et al. Towards a guideline for evaluation metrics in medical image segmentation.  
BMC Res Notes 15, 210 (2022).  
35 Siddique, N., Paheding, S., Elkin, C. P., & Devabhaktuni, V. U-net and its variants for medical image segmentation: A review of theory and applications.  
IEEE Access, 9, 82031-82057 (2021).  
36 Milletari, F., Navab, N., & Ahmadi, S. A. V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation.  
2016 Fourth International Conference on 3D Vision (3DV), 565-571 (2016).  
30 Wang, Z., Zhou, Y., & Lischinski, D. SSIM, the structural similarity index measure.  
IEEE Transactions on Image Processing, 13(4), 600-612 (2004).  
31 Hore, A., & Ziou, D. Image quality metrics: A survey.  
2010 20th International Conference on Pattern Recognition, 2366-2369 (2010).  
32 Zhang, L., Zhang, L., Mou, X., & Zhang, D. FSIM: A feature similarity index for image quality assessment.  
*IEEE Transactions on Image Processing*, 20(8), 2378-2386 (2011).

#### **引用的著作**

1. Ozeki Group \- Google Sites, 访问时间为 九月 28, 2025， [https://sites.google.com/site/ozekibp/](https://sites.google.com/site/ozekibp/)  
2. Yasuyuki OZEKI | RCAST, 访问时间为 九月 28, 2025， [https://www.rcast.u-tokyo.ac.jp/en/research/people/staff-ozeki\_yasuyuki.html](https://www.rcast.u-tokyo.ac.jp/en/research/people/staff-ozeki_yasuyuki.html)  
3. OZEKI Yasuyuki | The University of Tokyo, 访问时间为 九月 28, 2025， [https://www.u-tokyo.ac.jp/focus/en/people/people003160.html](https://www.u-tokyo.ac.jp/focus/en/people/people003160.html)  
4. OZEKI Yasuyuki \- 東京大学 大学院工学系研究科 電気系工学専攻, 访问时间为 九月 28, 2025， [https://www.eeis.t.u-tokyo.ac.jp/en/staff/ozeki-yasuyuki/](https://www.eeis.t.u-tokyo.ac.jp/en/staff/ozeki-yasuyuki/)  
5. OZEKI Yasuyuki, 访问时间为 九月 28, 2025， [https://www.ee.t.u-tokyo.ac.jp/en/staff/ozeki-yasuyuki/](https://www.ee.t.u-tokyo.ac.jp/en/staff/ozeki-yasuyuki/)  
6. Yasuyuki OZEKI | The University of Tokyo, Tokyo | Todai | Department of Electrical Engineering and Information Systems | Research profile \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/profile/Yasuyuki-Ozeki](https://www.researchgate.net/profile/Yasuyuki-Ozeki)  
7. Tissue imaging depth limit of stimulated Raman scattering microscopy \- PMC, 访问时间为 九月 28, 2025， [https://pmc.ncbi.nlm.nih.gov/articles/PMC7041472/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7041472/)  
8. Polychromatic Adaptive Optics‐Assisted Stimulated Raman Scattering Microscopy Enables Deep Tissue Chemical Imaging | Request PDF \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/394235311\_Polychromatic\_Adaptive\_Optics-Assisted\_Stimulated\_Raman\_Scattering\_Microscopy\_Enables\_Deep\_Tissue\_Chemical\_Imaging](https://www.researchgate.net/publication/394235311_Polychromatic_Adaptive_Optics-Assisted_Stimulated_Raman_Scattering_Microscopy_Enables_Deep_Tissue_Chemical_Imaging)  
9. Adaptive optics stimulated Raman scattering microscopy for topical product pharmacokinetic tomography (Conference Presentation) \- SPIE Digital Library, 访问时间为 九月 28, 2025， [https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13315/133150E/Adaptive-optics--stimulated-Raman-scattering-microscopy-for-topical-product/10.1117/12.3046782.full](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13315/133150E/Adaptive-optics--stimulated-Raman-scattering-microscopy-for-topical-product/10.1117/12.3046782.full)  
10. Stimulated Raman scattering microscopy with phase-controlled light focusing and aberration correction for rapid and label-free, volumetric deep tissue imaging \- OE Journals, 访问时间为 九月 28, 2025， [https://www.oejournal.org/article/doi/10.29026/oea.2024.240064](https://www.oejournal.org/article/doi/10.29026/oea.2024.240064)  
11. Ozeki Group \- Research \- Google Sites, 访问时间为 九月 28, 2025， [https://sites.google.com/site/ozekibp/research](https://sites.google.com/site/ozekibp/research)  
12. ‪Yasuyuki OZEKI‬ \- ‪Google Scholar‬, 访问时间为 九月 28, 2025， [https://scholar.google.com/citations?user=g\_dXGXgAAAAJ\&hl=en](https://scholar.google.com/citations?user=g_dXGXgAAAAJ&hl=en)  
13. Label-free chemical imaging flow cytometry by high-speed multicolor stimulated Raman scattering \- PubMed, 访问时间为 九月 28, 2025， [https://pubmed.ncbi.nlm.nih.gov/31324741/](https://pubmed.ncbi.nlm.nih.gov/31324741/)  
14. High speed imaging of B-cells by stimulated Raman scattering \- SPIE Digital Library, 访问时间为 九月 28, 2025， [https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11252/112520W/High-speed-imaging-of-B-cells-by-stimulated-Raman-scattering/10.1117/12.2545274.short](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11252/112520W/High-speed-imaging-of-B-cells-by-stimulated-Raman-scattering/10.1117/12.2545274.short)  
15. Ozeki Group \- News, 访问时间为 九月 28, 2025， [https://sites.google.com/site/ozekibp/news](https://sites.google.com/site/ozekibp/news)  
16. SLM microscopy: scanless two-photon imaging and photostimulation using spatial light modulators \- Frontiers, 访问时间为 九月 28, 2025， [https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/neuro.04.005.2008/full](https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/neuro.04.005.2008/full)  
17. Spatial Light Modulators \- Thorlabs, 访问时间为 九月 28, 2025， [https://www.thorlabs.com/newgrouppage9.cfm?objectgroup\_id=10378](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10378)  
18. Hill-climbing algorithm based on Zernike modes for wavefront sensorless adaptive optics | Request PDF \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/258807880\_Hill-climbing\_algorithm\_based\_on\_Zernike\_modes\_for\_wavefront\_sensorless\_adaptive\_optics](https://www.researchgate.net/publication/258807880_Hill-climbing_algorithm_based_on_Zernike_modes_for_wavefront_sensorless_adaptive_optics)  
19. Sensorless Adaptive Optics | AO tutorials, 访问时间为 九月 28, 2025， [https://aomicroscopy.org/sensorless-ao](https://aomicroscopy.org/sensorless-ao)  
20. Optimum deformable mirror modes for sensorless adaptive optics \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/228901975\_Optimum\_deformable\_mirror\_modes\_for\_sensorless\_adaptive\_optics](https://www.researchgate.net/publication/228901975_Optimum_deformable_mirror_modes_for_sensorless_adaptive_optics)  
21. CV\_XiaoyangZheng-General2025.pdf  
22. SRS Microscopy \- Spectra-Physics, 访问时间为 九月 28, 2025， [https://www.spectra-physics.com/en/n/srs-microscopy](https://www.spectra-physics.com/en/n/srs-microscopy)  
23. Semi-Supervised Medical Image Segmentation with Co-Distribution Alignment \- MDPI, 访问时间为 九月 28, 2025， [https://www.mdpi.com/2306-5354/10/7/869](https://www.mdpi.com/2306-5354/10/7/869)  
24. (PDF) Review of Semi-Supervised Medical Image Segmentation based on the U-Net, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/381538048\_Review\_of\_Semi-Supervised\_Medical\_Image\_Segmentation\_based\_on\_the\_U-Net](https://www.researchgate.net/publication/381538048_Review_of_Semi-Supervised_Medical_Image_Segmentation_based_on_the_U-Net)  
25. Semi-Supervised Medical Image Segmentation Based on Deep Consistent Collaborative Learning \- MDPI, 访问时间为 九月 28, 2025， [https://www.mdpi.com/2313-433X/10/5/118](https://www.mdpi.com/2313-433X/10/5/118)  
26. A review of research and development of semi-supervised learning strategies for medical image processing \- EAI Endorsed Transactions, 访问时间为 九月 28, 2025， [https://publications.eai.eu/index.php/el/article/view/4822](https://publications.eai.eu/index.php/el/article/view/4822)  
27. (PDF) Differential Data Augmentation Techniques for Medical Imaging Classification Tasks, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/325532618\_Differential\_Data\_Augmentation\_Techniques\_for\_Medical\_Imaging\_Classification\_Tasks](https://www.researchgate.net/publication/325532618_Differential_Data_Augmentation_Techniques_for_Medical_Imaging_Classification_Tasks)  
28. Calibration‐Jitter: Augmentation of hyperspectral data for improved surgical scene segmentation \- PMC, 访问时间为 九月 28, 2025， [https://pmc.ncbi.nlm.nih.gov/articles/PMC11665780/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11665780/)  
29. Data Augmentation and Spectral Structure Features for Limited Samples Hyperspectral Classification \- MDPI, 访问时间为 九月 28, 2025， [https://www.mdpi.com/2072-4292/13/4/547](https://www.mdpi.com/2072-4292/13/4/547)  
30. Pathology-Guided Virtual Staining Metric for Evaluation and Training \- arXiv, 访问时间为 九月 28, 2025， [https://arxiv.org/html/2507.12624v1](https://arxiv.org/html/2507.12624v1)  
31. Stain Normalization of Histopathological Images Based on Deep Learning: A Review \- MDPI, 访问时间为 九月 28, 2025， [https://www.mdpi.com/2075-4418/15/8/1032](https://www.mdpi.com/2075-4418/15/8/1032)  
32. Evaluation methods for virtual staining neural network models. a... \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/figure/Evaluation-methods-for-virtual-staining-neural-network-models-a-Standard-quantitative\_fig1\_368970616](https://www.researchgate.net/figure/Evaluation-methods-for-virtual-staining-neural-network-models-a-Standard-quantitative_fig1_368970616)  
33. What are different evaluation metrics used to evaluate image segmentation models?, 访问时间为 九月 28, 2025， [https://www.geeksforgeeks.org/computer-vision/what-are-different-evaluation-metrics-used-to-evaluate-image-segmentation-models/](https://www.geeksforgeeks.org/computer-vision/what-are-different-evaluation-metrics-used-to-evaluate-image-segmentation-models/)  
34. (PDF) Towards a guideline for evaluation metrics in medical image segmentation \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/publication/361423278\_Towards\_a\_guideline\_for\_evaluation\_metrics\_in\_medical\_image\_segmentation](https://www.researchgate.net/publication/361423278_Towards_a_guideline_for_evaluation_metrics_in_medical_image_segmentation)  
35. Understanding Evaluation Metrics in Medical Image Segmentation | by Nghi Huynh | Mastering Data Science | Medium, 访问时间为 九月 28, 2025， [https://medium.com/mastering-data-science/understanding-evaluation-metrics-in-medical-image-segmentation-d289a373a3f](https://medium.com/mastering-data-science/understanding-evaluation-metrics-in-medical-image-segmentation-d289a373a3f)  
36. Understanding Evaluation Metrics in Segmentation \- Kaggle, 访问时间为 九月 28, 2025， [https://www.kaggle.com/code/nghihuynh/understanding-evaluation-metrics-in-segmentation](https://www.kaggle.com/code/nghihuynh/understanding-evaluation-metrics-in-segmentation)  
37. High-speed molecular spectral imaging of tissues by video-rate, wavelength-tunable stimulated Raman scattering microscopy \- ResearchGate, 访问时间为 九月 28, 2025， [https://www.researchgate.net/profile/Yasuyuki-Ozeki/publication/233753803\_High-speed\_molecular\_spectral\_imaging\_of\_tissue\_with\_stimulated\_Raman\_scattering/links/541050290cf2d8daaad37e4d/High-speed-molecular-spectral-imaging-of-tissue-with-stimulated-Raman-scattering.pdf](https://www.researchgate.net/profile/Yasuyuki-Ozeki/publication/233753803_High-speed_molecular_spectral_imaging_of_tissue_with_stimulated_Raman_scattering/links/541050290cf2d8daaad37e4d/High-speed-molecular-spectral-imaging-of-tissue-with-stimulated-Raman-scattering.pdf)  
38. ‪Akihiro Isozaki‬ \- ‪Google Scholar‬, 访问时间为 九月 28, 2025， [https://scholar.google.co.il/citations?user=x12VpAwAAAAJ\&hl=fil](https://scholar.google.co.il/citations?user=x12VpAwAAAAJ&hl=fil)