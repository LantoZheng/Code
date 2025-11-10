# 📚 AI Detector 文档索引

## 🚀 快速导航

### 我想要...

#### ⚡ 5分钟快速开始
→ [QUICKSTART.md](QUICKSTART.md)

#### 🏠 了解如何使用 LMStudio（免费本地模型）
→ [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md)

#### 🆚 比较 OpenAI 和 LMStudio，选择最适合我的
→ [COMPARISON.md](COMPARISON.md)

#### 📖 查看完整使用文档
→ [README.md](README.md)

#### 🔧 了解技术实现细节
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

#### 🎉 查看最新更新（LMStudio 支持）
→ [LMSTUDIO_UPDATE.md](LMSTUDIO_UPDATE.md)

---

## 📋 完整文档列表

### 用户文档

| 文档 | 描述 | 适合人群 |
|------|------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速开始指南 | 🟢 所有用户 |
| [README.md](README.md) | 完整使用文档 | 🟢 所有用户 |
| [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) | LMStudio 详细教程 | 🟡 想用免费本地模型的用户 |
| [COMPARISON.md](COMPARISON.md) | OpenAI vs LMStudio 对比 | 🟡 不确定选哪个的用户 |
| [LMSTUDIO_UPDATE.md](LMSTUDIO_UPDATE.md) | LMStudio 新功能说明 | 🟡 老用户 |

### 开发文档

| 文档 | 描述 | 适合人群 |
|------|------|---------|
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目技术总结 | 🔴 开发者 |

### 脚本文件

| 文件 | 描述 | 用法 |
|------|------|------|
| `aidetector_lite.py` | 轻量版检测器 ⭐ | `python aidetector_lite.py paper.tex --lmstudio` |
| `aidetector.py` | 完整版检测器 | `python aidetector.py paper.tex --lmstudio` |
| `test_lmstudio.py` | LMStudio 连接测试 | `python test_lmstudio.py` |
| `test.sh` | 自动化测试脚本 | `./test.sh` |

### 配置文件

| 文件 | 描述 |
|------|------|
| `requirements.txt` | Python 依赖 |
| `.gitignore` | Git 忽略规则 |
| `example.tex` | 示例 LaTeX 文档 |

---

## 🎯 按场景查找

### 我是新手
1. 阅读 [QUICKSTART.md](QUICKSTART.md) 快速入门
2. 运行 `./test.sh` 检查环境
3. 选择 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) 或直接用 OpenAI API

### 我想免费使用
1. 阅读 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) 安装 LMStudio
2. 下载模型（推荐 Llama 3.1 8B）
3. 运行 `python test_lmstudio.py` 测试连接
4. 使用 `python aidetector_lite.py paper.tex --lmstudio`

### 我追求最高质量
1. 获取 OpenAI API 密钥
2. 运行 `python aidetector_lite.py paper.tex -k YOUR_KEY -m gpt-4`

### 我处理敏感文档
1. 必须使用 LMStudio（数据不离开电脑）
2. 参考 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md)

### 我在选择后端
1. 阅读 [COMPARISON.md](COMPARISON.md) 详细对比
2. 运行 `./test.sh` 查看推荐

### 我遇到问题
1. 运行 `./test.sh` 自动诊断
2. 如用 LMStudio：运行 `python test_lmstudio.py`
3. 查看 [README.md](README.md) 故障排除章节
4. 查看 [LMSTUDIO_GUIDE.md](LMSTUDIO_GUIDE.md) 常见问题

### 我想了解技术细节
1. 阅读 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. 查看源代码 `aidetector_lite.py`

---

## 🎓 推荐学习路径

### 初学者路径
```
1. QUICKSTART.md (5分钟)
   ↓
2. 运行 ./test.sh
   ↓
3. LMSTUDIO_GUIDE.md 或直接用 OpenAI
   ↓
4. 开始使用！
```

### 进阶路径
```
1. QUICKSTART.md (5分钟)
   ↓
2. COMPARISON.md (了解选择)
   ↓
3. 配置最适合的后端
   ↓
4. README.md (深入了解所有功能)
   ↓
5. PROJECT_SUMMARY.md (技术细节)
```

---

## 📊 文档长度参考

| 文档 | 预计阅读时间 | 详细程度 |
|------|------------|---------|
| QUICKSTART.md | 5 分钟 | ⭐ 简明 |
| README.md | 15 分钟 | ⭐⭐⭐ 详细 |
| LMSTUDIO_GUIDE.md | 20 分钟 | ⭐⭐⭐⭐ 非常详细 |
| COMPARISON.md | 10 分钟 | ⭐⭐⭐ 详细 |
| PROJECT_SUMMARY.md | 10 分钟 | ⭐⭐⭐ 详细 |
| LMSTUDIO_UPDATE.md | 5 分钟 | ⭐⭐ 中等 |

---

## 🔗 外部资源

- **LMStudio 官网**: https://lmstudio.ai/
- **OpenAI API 文档**: https://platform.openai.com/docs
- **OpenAI 定价**: https://openai.com/api/pricing/
- **Llama 模型**: https://huggingface.co/meta-llama
- **Qwen 模型**: https://huggingface.co/Qwen

---

## 💬 需要帮助？

1. 查找对应场景的文档（见上方）
2. 运行诊断工具 (`./test.sh` 或 `test_lmstudio.py`)
3. 查看故障排除章节
4. 提交 GitHub Issue

---

**提示**: 用 `Ctrl+F` / `Cmd+F` 快速搜索关键词！
