# 🎉 新功能：LMStudio 本地模型支持

## ✨ 更新内容

我们为 AI Detector 添加了 **LMStudio 本地模型支持**，现在你可以完全免费、离线、保护隐私地使用该工具！

## 🆕 新增功能

### 1. LMStudio 后端支持

两个主要脚本现在都支持 LMStudio：

- `aidetector.py` - 完整版
- `aidetector_lite.py` - 轻量版

### 2. 新增命令行参数

```bash
--lmstudio              # 启用 LMStudio 模式
--lmstudio-url URL      # 自定义 LMStudio 服务器地址
```

### 3. 新增文档

- **LMSTUDIO_GUIDE.md** - 完整的 LMStudio 使用指南
- **COMPARISON.md** - OpenAI vs LMStudio 详细对比
- **test_lmstudio.py** - LMStudio 连接测试工具

### 4. 更新的文档

- **README.md** - 添加 LMStudio 使用说明
- **QUICKSTART.md** - 更新快速开始步骤
- **PROJECT_SUMMARY.md** - 添加性能对比
- **test.sh** - 自动检测可用后端

## 📖 使用方法

### 快速开始

```bash
# 1. 下载并启动 LMStudio
# 访问 https://lmstudio.ai/

# 2. 在 LMStudio 中下载模型（推荐 Llama 3.1 8B）

# 3. 启动本地服务器（在 LMStudio 中）

# 4. 使用 AI Detector
python aidetector_lite.py paper.tex --lmstudio
```

### 详细步骤

查看 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) 获取完整教程。

## 🎯 优势

### LMStudio 模式
- ✅ **完全免费** - 无需 API 密钥
- ✅ **保护隐私** - 数据不离开你的电脑
- ✅ **离线使用** - 不需要网络连接
- ✅ **无限制** - 没有请求次数限制

### OpenAI API 模式
- ✅ **即刻可用** - 不需要安装
- ✅ **质量最高** - GPT-3.5/4 效果优秀
- ✅ **速度最快** - 云端强大算力
- ✅ **零硬件要求** - 任何设备可用

## 🔄 向后兼容

所有现有功能完全保留，你可以：

1. 继续使用 OpenAI API（默认行为）
2. 切换到 LMStudio（添加 `--lmstudio` 参数）
3. 混合使用（根据需求选择）

## 📊 对比示例

### 成本对比（1000 词文档）

| 模式 | 轻量版 | 完整版 |
|------|--------|--------|
| OpenAI GPT-3.5 | $0.01 | $0.50 |
| OpenAI GPT-4 | $0.05 | $2.00 |
| LMStudio | **$0.00** | **$0.00** |

### 速度对比（1000 词文档）

| 模式 | 轻量版 | 完整版 |
|------|--------|--------|
| OpenAI | ~1 分钟 | ~10 分钟 |
| LMStudio (16GB RAM) | ~2-3 分钟 | ~20-30 分钟 |
| LMStudio (32GB RAM + GPU) | ~1-2 分钟 | ~10-15 分钟 |

## 🧪 测试工具

### 自动测试脚本

```bash
./test.sh
```

自动检测：
- Python 和依赖
- LMStudio 服务器状态
- OpenAI API 密钥
- 推荐最佳后端

### LMStudio 连接测试

```bash
python test_lmstudio.py
```

测试：
- 服务器连接
- 可用模型
- 对话功能
- Logprobs 支持

## 📚 完整文档导航

### 新手入门
1. [QUICKSTART.md](QUICKSTART.md) - 5分钟快速开始
2. [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) - LMStudio 完整教程
3. [COMPARISON.md](COMPARISON.md) - 帮你选择最适合的方式

### 深入了解
1. [README.md](README.md) - 完整使用文档
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 技术实现细节

### 工具脚本
1. `test.sh` - 自动化测试
2. `test_lmstudio.py` - LMStudio 连接测试

## 🎓 推荐使用场景

### 场景 1: 日常使用（推荐 LMStudio）
```bash
python aidetector_lite.py draft.tex --lmstudio
```
- 免费无限使用
- 保护隐私
- 适合学生和研究者

### 场景 2: 重要文档（推荐 OpenAI GPT-4）
```bash
python aidetector_lite.py paper.tex -k $API_KEY -m gpt-4
```
- 最高质量
- 最准确结果
- 适合论文发表前检查

### 场景 3: 保密文档（必须用 LMStudio）
```bash
python aidetector_lite.py confidential.tex --lmstudio
```
- 数据完全本地
- 绝对隐私保护
- 适合敏感内容

## 💡 使用技巧

### 提高 LMStudio 速度
1. 使用 GPU 加速
2. 选择较小的模型（Llama 3.2 3B）
3. 增大块大小 `-c 200`
4. 关闭其他程序释放资源

### 降低 OpenAI 费用
1. 使用轻量版而非完整版
2. 使用 GPT-3.5 而非 GPT-4
3. 增大块大小减少调用次数

### 获得最佳质量
1. 使用完整版（词级别分析）
2. 使用 GPT-4 模型
3. 减小块大小增加精度

## 🐛 故障排除

### LMStudio 连接失败
```bash
# 运行诊断
python test_lmstudio.py

# 检查服务器状态
curl http://localhost:1234/v1/models
```

### 性能慢
- 检查硬件资源（RAM/GPU）
- 尝试更小的模型
- 增大块大小

### 质量不理想
- 尝试更大的模型
- 调整温度参数
- 或切换到 OpenAI API

## 📞 获取帮助

1. 查看 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) 详细教程
2. 查看 [COMPARISON.md](COMPARISON.md) 使用建议
3. 运行 `./test.sh` 自动诊断
4. 运行 `python test_lmstudio.py` 测试连接
5. 提交 GitHub Issue

## 🙏 鸣谢

感谢 LMStudio 团队提供优秀的本地 LLM 解决方案！

---

**现在就试试 LMStudio 模式，享受免费、隐私、无限制的 AI 检测！** 🚀
