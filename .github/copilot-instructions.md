## 仓库速览（对 AI 代理重要的“地形图”）

- 这是一个个人多项目集合（notebooks、LaTeX 文档、独立 Python 脚本、数据文件）。主要目录示例：
  - `CV-LaTeX/`：LaTeX 简历与 ResearchPlan（例如 `ResearchPlan/Ozeki/ResearchPlan.tex`）。
  - `BNUPT/`, `Experiments/`, `Phys-*`：实验与数据分析（大量 `.ipynb`、`.csv`）。
  - `GeneralRelativity/`, `LearnDL/` 等：独立可运行的 Python 脚本和演示。

## 为什么这样组织
- 每个子目录通常是一个独立的“小项目”或笔记本集合，缺少统一的包管理或 CI。AI 代理在改动时应将变更限制在单个子目录，并验证该子目录下可复现的运行步骤。

## 关键工作流（可直接运行的示例）
- 编译 LaTeX（常见）：在包含 `.tex` 的目录运行：
  - `latexmk -pdf <file>.tex` 或 `pdflatex`（多次运行以解决交叉引用）。示例：`latexmk ResearchPlan/Ozeki/ResearchPlan.tex`。
- 运行/执行 Jupyter 笔记本：
  - 使用 `jupyter nbconvert --to notebook --execute <nb>.ipynb` 或 `papermill` 执行并保存输出。示例：`jupyter nbconvert --to notebook --execute Phys-C191A/Shor.ipynb`。
- 运行独立 Python 脚本：
  - 直接用系统 Python：`python3 GeneralRelativity/EinsteinTensor.py`（检查脚本顶部的依赖导入）。

## 项目检测与依赖发现策略（自动化步骤）
- 仓库没有统一的 `requirements.txt` / `package.json`。建议：搜索 `import `（`.py` / `.ipynb`）以推断所需第三方库（例如：`qiskit` 在 `Phys-C191A/Shor.ipynb`；`torch` 在 `LearnDL`）。
- 对每个子项目：
  1. 查找 README 或 notebook 顶部的环境说明。  
  2. 用 `pip`/`conda` 在隔离环境中安装列出的包并执行一个小的 smoke-run（notebook 的前几 cell / 简单脚本）。

## 代码风格与约定（可被代理利用）
- 大量内容为交互式笔记本和实验脚本，常见模式：
  - 数据以 CSV 放在同目录或 `BNUPT/` 等文件夹，脚本通过相对路径读取（保持相对路径不变以便复现）。
  - LaTeX 项目使用 `latexmk` / `pdflatex` 并假设系统已安装 TeX 发行版。
  - 少量脚本会打印或生成图像/PDF，代理做改动时请手动运行生成命令以验证输出。

## 编辑/提交建议（针对自动化代理）
- 小步提交：改动限定在单一子目录，包含运行验证步骤（例如：已成功生成 PDF / 已执行 notebook 无错误）。
- 不要修改仓库全局结构（不要假设存在虚拟环境或统一依赖文件），除非你同时添加了明确的依赖清单和运行说明。

## 已知特殊文件（供参考）
- `.gpt-runner/copilot.gpt.md`：包含自定义系统提示片段，可能影响仓内 AI 工具的行为；谨慎修改。  
- `Experiments/*/**/## Copilot.md`：一些实验目录下包含 Copilot / 环境诊断信息，表明作者在本地使用代理与代理相关设置。

## 快速任务举例（AI 代理可直接执行）
- 验证 LaTeX 编译：在 `CV-LaTeX/ResearchPlan/Ozeki/` 目录运行 `latexmk -pdf ResearchPlan.tex` 并检查生成的 PDF。  
- 执行 notebook：`jupyter nbconvert --to notebook --execute Phys-C191A/Shor.ipynb`，若出错，读取 traceback 中缺失库名并在该子目录附上说明。

## 发现问题时的优先级与报告格式
- 若运行报错（缺包或 API 变更），生成简短问题报告包含：子目录、命令、错误摘要、最小可复现步骤。把修复/建议作为单独 commit/PR。

## 结束语
- 目标是让 AI 代理在不破坏其它子项目的前提下，高效地在单个子目录内迭代：小改动、运行验证、清晰的 PR 描述与复现说明。
