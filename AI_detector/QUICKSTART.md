# 快速开始指南

## 1. 安装依赖

```bash
cd AI_detector
pip install -r requirements.txt
```

## 2. 选择使用方式

### 方式 A: 使用 LMStudio（推荐，免费）

1. 下载 LMStudio: https://lmstudio.ai/
2. 下载模型（如 Llama 3.1 8B）
3. 启动本地服务器
4. 详细步骤见 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md)

### 方式 B: 使用 OpenAI API

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

## 3. 运行示例

### 使用轻量版 + LMStudio（最推荐）

```bash
# 启动 LMStudio 服务器后
python aidetector_lite.py example.tex --lmstudio

# 查看结果
open example_report.html
```

### 使用轻量版 + OpenAI API

```bash
# 分析示例文档
python aidetector_lite.py example.tex -k your-api-key

# 查看结果
open example_report.html
```

### 使用完整版（详细分析，但 API 调用多）

```bash
# 分析示例文档
python aidetector.py example.tex

# 编译查看结果
pdflatex example_highlighted.tex
open example_highlighted.pdf
```

## 4. 分析你自己的文档

```bash
# 轻量版
python aidetector_lite.py your_paper.tex -o my_report.html

# 完整版
python aidetector.py your_paper.tex -o my_paper_highlighted.tex
```

## 两个版本的区别

| 特性 | aidetector.py (完整版) | aidetector_lite.py (轻量版) |
|------|----------------------|---------------------------|
| API 调用次数 | 每个词调用一次（较多）| 每100词调用一次（较少） |
| 处理速度 | 较慢 | 较快 |
| 费用（OpenAI） | 较高 | 较低 |
| 费用（LMStudio）| 免费 | 免费 |
| 输出格式 | LaTeX PDF | HTML 网页 |
| 精确度 | 词级别精确 | 块级别近似 |
| 推荐场景 | 短文档、精确分析 | 长文档、快速预览 |

## 推荐组合

🥇 **最佳**: `aidetector_lite.py` + `--lmstudio` (快速、免费、隐私)
🥈 **次选**: `aidetector_lite.py` + OpenAI API (快速、付费、质量好)
🥉 **精确**: `aidetector.py` + `--lmstudio` (慢、免费、精确)

## 5. 常见问题

### Q: 如何获取 OpenAI API 密钥？
A: 访问 https://platform.openai.com/api-keys 创建密钥

### Q: 运行时提示 "无法解析导入 openai"？
A: 运行 `pip install openai` 安装依赖

### Q: API 调用太贵了？
A: 使用轻量版 `aidetector_lite.py`，或增加 `--chunk-size` 参数

### Q: 可以使用其他模型吗？
A: 可以！
- LMStudio: 在 LMStudio 中选择任何已下载的模型
- OpenAI: 使用 `-m` 参数，例如：`-m gpt-4` 或 `-m gpt-3.5-turbo`

### Q: LMStudio 和 OpenAI 哪个更好？
A: 
- **LMStudio**: 免费、隐私、无限制，但需要好硬件
- **OpenAI**: 质量高、速度快，但需付费
- 推荐先试 LMStudio，不满意再用 OpenAI

## 6. 进阶使用

### 使用 LMStudio

```bash
# 基本使用
python aidetector_lite.py paper.tex --lmstudio

# 自定义服务器地址
python aidetector_lite.py paper.tex --lmstudio --lmstudio-url http://localhost:5000/v1

# 调整块大小（更大=更快）
python aidetector_lite.py paper.tex --lmstudio -c 200
```

### 批量处理

```bash
# 使用 LMStudio 批量处理
for file in *.tex; do
    python aidetector_lite.py "$file" --lmstudio
done
```

### 自定义块大小

```bash
# 使用更大的块（减少 API 调用）
python aidetector_lite.py paper.tex -c 200

# 使用更小的块（提高精度）
python aidetector_lite.py paper.tex -c 50
```

### 使用不同模型

```bash
# 使用 GPT-4（更准确但更贵）
python aidetector_lite.py paper.tex -m gpt-4

# 使用 GPT-3.5 Turbo（默认，性价比高）
python aidetector_lite.py paper.tex -m gpt-3.5-turbo
```

## 7. 输出解读

### 困惑度（Perplexity）说明

- **低困惑度 (1-10)**：文本高度可预测，可能由 AI 生成
- **中等困惑度 (10-50)**：正常文本范围
- **高困惑度 (50+)**：创造性或不寻常的用词

### 颜色含义

- 🔴 **红色区域**：高度可疑，建议重点检查
- 🟠 **橙色区域**：中度可疑
- 🟡 **黄色区域**：轻微可疑
- 🟢 **绿色区域**：可能为人工撰写
- 🔵 **蓝色区域**：很可能为人工撰写

## 8. 注意事项

⚠️ **重要提示**：

1. 该工具只是一个辅助判断工具，不能作为确凿证据
2. 某些技术性强的文本可能误判
3. 使用前请了解 OpenAI API 的定价
4. 长文档处理可能需要较长时间

## 9. 获取帮助

```bash
# 查看完整帮助
python aidetector.py --help
python aidetector_lite.py --help
```

需要更多帮助？查看 README.md 或提交 Issue。
