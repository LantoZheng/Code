# 自动生成的依赖草案说明

以下 `requirements.txt` 草案由仓库内 Python 脚本与 Jupyter 笔记本中的 `import`/`from` 语句自动汇总生成，用作快速 smoke-run 环境准备：

- `GeneralRelativity/requirements.txt` (numpy, sympy, matplotlib)
- `LearnDL/requirements.txt` (torch, numpy, matplotlib)
- `Phys-C191A/requirements.txt` (qiskit, qiskit-aer, numpy)
- `BNUPT/requirements.txt` (pandas, numpy, matplotlib, scipy)

如何验证：

1. 在 macOS 下创建并激活虚拟环境（示例）：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r <folder>/requirements.txt
python3 <script>.py   # 或 jupyter nbconvert --to notebook --execute <notebook>.ipynb
```

2. 注意：这些文件为草案，可能缺少小众依赖（例如 `umap-learn`, `plotly`, `otter` 等）。若执行时出现 ImportError，请把缺失包名追加到对应 `requirements.txt` 并重新安装。

3. qiskit 与 qiskit-aer 在不同平台/版本间 API 有差异（`Aer`、`QFT` 等在新版/旧版中可能移动或被弃用），建议通过在 `Phys-C191A/` 目录运行 `python3 -c "import qiskit; print(qiskit.__version__)"` 来确认安装版本。

如果你希望，我可以：

- 扫描更多子目录并生成额外 `requirements.txt`。 
- 为每个子目录生成 `environment.yml`（conda）或 pin 具体版本号。
