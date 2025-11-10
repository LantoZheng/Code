# AI Detector 项目总结

## 📁 项目结构

```
AI_detector/
├── aidetector.py          # 完整版检测器（词级别精确分析）
├── aidetector_lite.py     # 轻量版检测器（块级别快速分析）
├── requirements.txt       # Python 依赖
├── example.tex           # 示例 LaTeX 文档
├── test.sh               # 自动化测试脚本
├── README.md             # 详细文档
├── QUICKSTART.md         # 快速开始指南
└── .gitignore           # Git 忽略文件
```

## 🎯 核心功能

### 1. aidetector.py (完整版)
- **功能**：对每个词元进行独立的困惑度分析
- **输出**：带颜色标记的 LaTeX 文档
- **优点**：词级别精确分析
- **缺点**：API 调用多，速度慢，费用高
- **适用**：短文档、需要精确分析的场景

### 2. aidetector_lite.py (轻量版) ⭐️ 推荐
- **功能**：按文本块进行批量困惑度分析
- **输出**：交互式 HTML 报告
- **优点**：API 调用少，速度快，费用低
- **缺点**：块级别近似分析
- **适用**：长文档、快速预览、成本控制

## 🔧 技术实现

### 支持的后端
1. **OpenAI API** - 云端服务，质量高但需付费
2. **LMStudio** - 本地模型，完全免费且保护隐私 ⭐️

### 核心算法
1. **文本提取**：从 LaTeX 中提取纯文本内容
   - 移除注释
   - 处理 LaTeX 命令
   - 保留实际文本内容

2. **困惑度计算**：
   ```
   困惑度 = 1 / P(token|context)
   ```
   - 使用 OpenAI API 或 LMStudio 获取 logprobs
   - 计算词元在给定上下文中的概率
   - 低困惑度 → 高可预测性 → 可能由 AI 生成

3. **颜色映射**：
   ```
   AI概率 = 1 - log(perplexity) / log(100)
   ```
   - 蓝色：AI 概率 < 10%
   - 绿色：AI 概率 10-25%
   - 黄色：AI 概率 25-50%
   - 橙色：AI 概率 50-75%
   - 红色：AI 概率 > 75%

## 📊 使用示例

### 快速开始（LMStudio，推荐）
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 LMStudio 服务器（见 LMSTUDIO_GUIDE.md）

# 3. 运行分析
python aidetector_lite.py example.tex --lmstudio
```

### 使用 OpenAI API
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API 密钥
export OPENAI_API_KEY='your-key'

# 3. 运行分析
python aidetector_lite.py example.tex
```

### 高级用法
```bash
# 使用 LMStudio（免费）
python aidetector_lite.py paper.tex --lmstudio

# 使用 GPT-4（付费）
python aidetector_lite.py paper.tex -k your-key -m gpt-4

# 自定义块大小
python aidetector_lite.py paper.tex --lmstudio -c 200

# 指定输出文件
python aidetector_lite.py paper.tex --lmstudio -o report.html

# 自定义 LMStudio 地址
python aidetector_lite.py paper.tex --lmstudio --lmstudio-url http://localhost:5000/v1
```

## 📈 性能对比

### 版本对比
| 指标 | 完整版 | 轻量版 |
|------|--------|--------|
| API 调用/1000词 | ~1000次 | ~10次 |
| 处理时间/1000词 (OpenAI) | ~10分钟 | ~1分钟 |
| 处理时间/1000词 (LMStudio) | ~20-30分钟 | ~2-3分钟 |
| OpenAI 费用/1000词 | $0.50-1.00 | $0.01-0.05 |
| LMStudio 费用 | 免费 | 免费 |
| 精确度 | 词级别 | 块级别 |
| 输出格式 | LaTeX PDF | HTML |

### 后端对比
| 指标 | OpenAI API | LMStudio |
|------|-----------|----------|
| 费用 | 按使用付费 | 完全免费 ✅ |
| 速度 | 很快 ✅ | 中等（取决于硬件）|
| 质量 | 很高 ✅ | 良好 |
| 隐私 | 数据上传 | 完全本地 ✅ |
| 网络 | 需要 | 不需要 ✅ |
| 硬件要求 | 无 ✅ | 16GB+ RAM 推荐 |

*OpenAI 费用基于 GPT-3.5-turbo 价格估算*

## 🎨 输出示例

### 轻量版 HTML 输出
- 交互式网页报告
- 彩色文本块标记
- 详细统计信息
- 可直接在浏览器中查看

### 完整版 LaTeX 输出
- 带颜色高亮的 PDF
- 使用 `soul` 包高亮
- 包含图例说明
- 需要编译后查看

⚠️ **注意事项**

1. **费用控制**
   - 长文档建议使用轻量版
   - 或使用 LMStudio（完全免费）
   - 或增加 `--chunk-size` 参数
   - 监控 OpenAI API 使用量（如使用）

2. **准确性限制**
   - 这只是一个辅助工具
   - 不能作为确凿证据
   - 技术性文本可能误判

3. **隐私安全**
   - OpenAI API：文本会上传到云端
   - LMStudio：数据完全本地处理，保护隐私 ✅
   - 敏感内容强烈建议使用 LMStudio

4. **硬件要求**（仅 LMStudio）
   - 最低：8GB RAM + 小模型（Llama 3.2 3B）
   - 推荐：16GB RAM + 中等模型（Llama 3.1 8B）
   - 理想：32GB+ RAM + GPU + 大模型

## 🔮 未来改进

### 可能的增强功能
- [ ] 支持批量文件处理
- [ ] 添加本地模型选项（避免 API 调用）
- [ ] 支持更多文档格式（Word, Markdown）
- [ ] 提供 Web 界面
- [ ] 添加详细的统计分析图表
- [ ] 支持多语言检测
- [ ] 优化 LaTeX 解析器

### 性能优化
- [ ] 实现并行 API 调用
- [ ] 添加结果缓存机制
- [ ] 优化内存使用
- [ ] 支持流式处理

## 📚 依赖说明

```
openai>=1.0.0    # OpenAI API 客户端
numpy>=1.20.0    # 数值计算
```

可选依赖：
- `pdflatex`：编译完整版输出
- `xcolor`, `soul`：LaTeX 颜色包

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置
```bash
git clone <repo>
cd AI_detector
pip install -r requirements.txt
export OPENAI_API_KEY='your-key'
python test.sh
```

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🆘 获取帮助

1. 查看 `README.md` - 详细文档
2. 查看 `QUICKSTART.md` - 快速开始
3. 运行 `./test.sh` - 自动化测试
4. 运行 `python aidetector_lite.py --help` - 命令帮助

## 📧 联系方式

有问题或建议？请提交 Issue 或 Pull Request。

---

**享受使用！** 🚀
