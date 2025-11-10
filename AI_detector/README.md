# LaTeX AI 内容检测器

这个工具通过计算词元的困惑度（perplexity）来检测 LaTeX 文档中可能由 AI 生成的内容。

## 原理

该工具使用 OpenAI API 来预测每个词元基于前文出现的概率：

1. **困惑度计算**：对文档中的每个词，根据前文上下文预测该词出现的概率
2. **AI 概率推断**：困惑度越低（即预测概率越高），表示该词越符合统计模式，AI 生成的可能性越大
3. **颜色标记**：使用不同颜色高亮显示 AI 生成概率：
   - 🔵 蓝色：极低 AI 概率
   - 🟢 绿色：低 AI 概率  
   - 🟡 黄色：中等 AI 概率
   - 🟠 橙色：高 AI 概率
   - 🔴 红色：极高 AI 概率

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或者使用 conda
conda install numpy
pip install openai
```

## 配置

### 方式 1: 使用 LMStudio 本地模型（推荐，免费）

1. 下载并安装 LMStudio: https://lmstudio.ai/
2. 下载一个模型（推荐 Llama 3.1 8B）
3. 启动 LMStudio 的本地服务器
4. 运行脚本时添加 `--lmstudio` 参数

详细步骤请查看 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md)

### 方式 2: 使用 OpenAI API

设置 OpenAI API 密钥：

```bash
export OPENAI_API_KEY='your-api-key-here'
```

或者在运行时通过 `-k` 参数传入。

## 使用方法

### 基本用法（使用 LMStudio，推荐）

```bash
# 启动 LMStudio 并开启服务器后
python aidetector.py input.tex --lmstudio
```

### 使用 OpenAI API

```bash
python aidetector.py input.tex -k your-api-key
```

这将生成 `input_highlighted.tex` 文件，其中包含带颜色标记的内容。

### 指定输出文件

```bash
python aidetector.py input.tex -o output.tex
```

### 使用 LMStudio 本地模型

```bash
python aidetector.py input.tex --lmstudio
```

### 使用不同的 OpenAI 模型

```bash
python aidetector.py input.tex -k your-key -m gpt-4
```

### 调整上下文窗口

```bash
python aidetector.py input.tex -w 100
```

上下文窗口越大，考虑的前文越多，但处理速度越慢。

### 完整参数示例

使用 LMStudio（推荐）：
```bash
python aidetector.py research_paper.tex \
  -o analyzed_paper.tex \
  --lmstudio \
  -w 50
```

使用 OpenAI API：
```bash
python aidetector.py research_paper.tex \
  -o analyzed_paper.tex \
  -k sk-your-api-key \
  -m gpt-3.5-turbo \
  -w 50
```

## 参数说明

- `input`: 输入的 LaTeX 文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认为 `input_highlighted.tex`）
- `--lmstudio`: 使用 LMStudio 本地模型（推荐，免费）
- `--lmstudio-url`: LMStudio 服务器地址（可选，默认为 `http://localhost:1234/v1`）
- `-k, --api-key`: OpenAI API 密钥（使用 OpenAI 时需要）
- `-m, --model`: 使用的模型（可选，默认为 `gpt-3.5-turbo`）
- `-w, --window`: 上下文窗口大小（可选，默认为 50 个词）

## 编译输出的 LaTeX 文档

生成的 LaTeX 文档需要以下包：

- `xcolor`: 颜色支持
- `soul`: 高亮支持

确保你的 LaTeX 发行版已安装这些包，然后正常编译：

```bash
pdflatex output.tex
```

## 注意事项

1. **费用**：
   - 使用 LMStudio：完全免费，但需要本地硬件资源
   - 使用 OpenAI API：按使用付费，长文档可能产生较高费用
2. **处理速度**：由于需要逐词调用 API/模型，处理速度较慢
3. **准确性**：困惑度只是一个指标，不能完全准确判断内容是否由 AI 生成
4. **LaTeX 兼容性**：工具会尽量提取文本内容，但复杂的 LaTeX 命令可能影响分析
5. **LMStudio 要求**：推荐 16GB+ RAM，GPU 加速可显著提升速度

## 输出示例

运行后，终端会显示统计信息：

```
=== 统计报告 ===
总词元数: 1250
平均困惑度: 35.42
困惑度中位数: 28.15
最低困惑度: 2.34
最高困惑度: 98.76

颜色分布:
blue: 125 (10.0%)
green: 375 (30.0%)
yellow: 500 (40.0%)
orange: 188 (15.0%)
red: 62 (5.0%)
```

## 工作流程示例

```bash
# 1. 设置 API 密钥
export OPENAI_API_KEY='sk-...'

# 2. 分析 LaTeX 文档
python aidetector.py my_paper.tex -o analyzed_paper.tex

# 3. 编译查看结果
pdflatex analyzed_paper.tex
open analyzed_paper.pdf
```

## 高级用法

### 批量处理多个文件

```bash
for file in *.tex; do
  python aidetector.py "$file" -o "analyzed_$file"
done
```

### 只分析特定部分

如果只想分析文档的特定部分，可以先手动编辑 LaTeX 文件，只保留需要分析的内容。

## 故障排除

### 问题：ImportError: No module named 'openai'
**解决**：安装 openai 包
```bash
pip install openai
```

### 问题：API 请求失败
**解决**：
1. 检查 API 密钥是否正确
2. 检查网络连接
3. 检查 OpenAI API 配额

### 问题：生成的 LaTeX 编译错误
**解决**：
1. 确保安装了 `xcolor` 和 `soul` 包
2. 检查原始 LaTeX 文件是否可以正常编译
3. 查看生成文件中是否有格式错误

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
