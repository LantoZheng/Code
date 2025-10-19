# 编译说明

## 文件说明

- `ResearchPlan_Toma.tex` - 主 LaTeX 文档（优化后的格式）
- `references.bib` - BibTeX 参考文献数据库
- `ResearchPlan_Toma.pdf` - 编译生成的 PDF 文件

## 使用 XeLaTeX + Biber 编译

文档采用专业的学术格式，使用 Times New Roman 字体和 1.5 倍行距。完整的编译流程如下：

```bash
# 1. 首次编译生成辅助文件
xelatex ResearchPlan_Toma.tex

# 2. 运行 Biber 处理参考文献
biber ResearchPlan_Toma

# 3. 再次编译以插入引用
xelatex ResearchPlan_Toma.tex

# 4. 最后一次编译确保所有交叉引用正确
xelatex ResearchPlan_Toma.tex
```

## 或使用一键命令

```bash
cd /Users/zhengxiaoyang/Code/CV-LaTeX/ResearchPlan/Toma
biber ResearchPlan_Toma && xelatex -interaction=nonstopmode ResearchPlan_Toma.tex && xelatex -interaction=nonstopmode ResearchPlan_Toma.tex
```

## 或使用 latexmk 自动化编译

```bash
latexmk -xelatex -bibtex ResearchPlan_Toma.tex
```

## 系统要求

- XeLaTeX 发行版（TeX Live 或 MiKTeX）
- Biber（通常随 TeX 发行版一起安装）
- Times New Roman 字体（macOS 和 Windows 系统自带）

## 格式特点

### 参考 Ozeki 教授研究计划的优化：

1. **专业排版**：
   - 使用 Times New Roman 字体（学术标准）
   - 1.5 倍行距（onehalfspacing）
   - 1 英寸页边距
   - microtype 包优化字符间距

2. **结构优化**：
   - 清晰的 Abstract 环境
   - 简洁的章节组织
   - Phase-based Methods 结构
   - 添加了 Risks and Mitigation 部分
   - **包含详细的 Timeline and Milestones (24 个月)**

3. **引用格式**：
   - 数字编号格式（numeric style）
   - 按出现顺序排序（sorting=none）
   - 使用 biblatex + biber 管理参考文献

4. **内容呈现**：
   - 使用 `\textbf{}` 强调关键术语
   - 使用 `\textit{}` 标注技术细节
   - 使用 enumerate 和 itemize 清晰组织要点
   - 在参考文献前添加 `\newpage`

## Timeline 结构

文档包含详细的 24 个月研究计划，分为 4 个阶段：

1. **Months 1-6**: Foundation and Data Generation
2. **Months 7-12**: AI Model Development and Training
3. **Months 13-18**: Design Library Generation and Selection
4. **Months 19-24**: Experimental Validation and Thesis Completion

每个阶段都包含具体任务和里程碑（Milestone）。

## 引用格式

在正文中使用 `\cite{key}` 命令引用文献，例如：
- `\cite{toma_researches}` 会显示为 [1]
- `\cite{dl_nanophotonics_rg}` 会显示为 [3]

所有引用会在文档末尾的 "References" 部分自动生成完整的参考文献列表。

## 清理临时文件

```bash
rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.synctex.gz
```

