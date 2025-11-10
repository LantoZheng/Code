# LMStudio 使用指南

## 🏠 什么是 LMStudio？

LMStudio 是一个桌面应用程序，允许你在本地运行大型语言模型（LLM），无需调用云端 API。

### 优势
- ✅ **完全免费** - 不需要 API 密钥，无需付费
- ✅ **隐私保护** - 数据不会发送到外部服务器
- ✅ **离线使用** - 不需要网络连接
- ✅ **无限制** - 没有请求次数限制
- ✅ **自定义模型** - 可以选择各种开源模型

### 劣势
- ⚠️ 需要较好的硬件（推荐 16GB+ RAM，GPU 更佳）
- ⚠️ 首次下载模型需要时间和存储空间
- ⚠️ 响应速度可能比云端 API 慢

## 📥 安装 LMStudio

### 1. 下载 LMStudio

访问官网下载：https://lmstudio.ai/

支持平台：
- macOS (Apple Silicon / Intel)
- Windows
- Linux

### 2. 安装并启动

1. 双击下载的安装包
2. 按照提示完成安装
3. 启动 LMStudio

## 🤖 选择和下载模型

### 推荐模型

#### 小型模型（8GB RAM 可用）
- **Llama 3.2 3B** - 快速，适合日常任务
- **Phi-3 Mini** - 微软的轻量级模型
- **Mistral 7B** - 性能和速度平衡良好

#### 中型模型（16GB RAM 推荐）
- **Llama 3.1 8B** - 强大且流行
- **Qwen 2.5 7B** - 中文支持优秀
- **Gemma 2 9B** - Google 的开源模型

#### 大型模型（32GB+ RAM）
- **Llama 3.1 70B** (量化版本)
- **Mixtral 8x7B**
- **Qwen 2.5 14B**

### 下载步骤

1. 打开 LMStudio
2. 点击左侧的 🔍 **Discover** 标签
3. 搜索你想要的模型（如 "llama 3.1 8b"）
4. 选择一个量化版本（推荐 `Q4_K_M` 或 `Q5_K_M`）
5. 点击下载按钮

> 💡 **量化说明**：
> - Q4 = 4位量化（更小，更快，质量稍低）
> - Q5 = 5位量化（平衡）
> - Q8 = 8位量化（更大，更慢，质量更高）

## 🚀 启动 API 服务器

### 1. 加载模型

1. 点击左侧的 💬 **Chat** 标签
2. 在顶部选择已下载的模型
3. 等待模型加载完成

### 2. 启动本地服务器

1. 点击左侧的 🔌 **Local Server** 标签
2. 确认端口号（默认 `1234`）
3. 点击 **Start Server** 按钮
4. 看到 "Server running" 提示即成功

### 3. 验证服务器

在终端运行：

```bash
curl http://localhost:1234/v1/models
```

应该看到类似输出：
```json
{
  "data": [
    {
      "id": "llama-3.1-8b-instruct",
      ...
    }
  ]
}
```

## 🎯 在 AI Detector 中使用

### 基本用法

```bash
# 使用 LMStudio（轻量版，推荐）
python aidetector_lite.py example.tex --lmstudio

# 使用 LMStudio（完整版）
python aidetector.py example.tex --lmstudio
```

### 自定义服务器地址

如果你修改了 LMStudio 的端口：

```bash
python aidetector_lite.py paper.tex --lmstudio --lmstudio-url http://localhost:5000/v1
```

### 调整块大小

LMStudio 处理速度可能较慢，建议增大块大小：

```bash
python aidetector_lite.py paper.tex --lmstudio -c 200
```

## 🔧 性能优化

### 1. GPU 加速

确保 LMStudio 使用 GPU：
- 在 LMStudio 设置中检查 GPU 选项
- macOS: 自动使用 Metal
- Windows/Linux: 确保安装了 CUDA 驱动

### 2. 调整上下文窗口

在 LMStudio 的 Chat 设置中：
- **Context Length**: 推荐 4096-8192
- **Max Tokens**: 根据需求设置

### 3. 选择合适的量化级别

根据你的硬件：
- 8GB RAM → Q4
- 16GB RAM → Q5
- 32GB+ RAM → Q6 或 Q8

## 📊 性能对比

| 指标 | OpenAI API | LMStudio 本地 |
|------|-----------|--------------|
| 费用 | 按使用付费 | 完全免费 |
| 速度 | 很快 | 中等（取决于硬件）|
| 隐私 | 数据上传 | 完全本地 |
| 质量 | 很高 | 良好（取决于模型）|
| 限制 | 有配额限制 | 无限制 |
| 网络 | 需要 | 不需要 |

## 🐛 常见问题

### Q: LMStudio 服务器无法启动？

**A:** 检查：
1. 端口 1234 是否被占用
2. 模型是否正确加载
3. 重启 LMStudio 应用

### Q: 连接错误：Connection refused？

**A:** 确保：
1. LMStudio 服务器正在运行
2. 端口号正确（默认 1234）
3. 防火墙未阻止连接

### Q: 处理速度很慢？

**A:** 尝试：
1. 使用更小的模型或更低的量化
2. 增加块大小 `-c 200`
3. 确保 GPU 加速已启用
4. 关闭其他占用资源的程序

### Q: 结果质量不如 OpenAI？

**A:** 
1. 尝试更大的模型
2. 使用更高的量化级别（Q6/Q8）
3. 调整温度参数（在代码中）

### Q: 模型下载失败？

**A:**
1. 检查网络连接
2. 使用 VPN（某些地区可能需要）
3. 尝试从 Hugging Face 手动下载

## 🔄 切换使用模式

### 场景 1: 快速测试
```bash
# 使用 LMStudio，快速预览
python aidetector_lite.py paper.tex --lmstudio -c 200
```

### 场景 2: 精确分析
```bash
# 使用 OpenAI API，获得最佳质量
python aidetector_lite.py paper.tex -k YOUR_API_KEY -m gpt-4
```

### 场景 3: 隐私文档
```bash
# 必须使用 LMStudio（数据不外传）
python aidetector_lite.py confidential.tex --lmstudio
```

## 📱 高级配置

### 自定义 LMStudio 设置

在 LMStudio 的 **Settings** 中：

**推荐设置：**
```
Temperature: 0.1-0.3 (更确定性的输出)
Top P: 0.9
Top K: 40
Context Length: 4096
Max Tokens: 512
```

### 模型参数调优

如果需要修改代码中的参数，编辑 `aidetector_lite.py`：

```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    max_tokens=50,
    temperature=0.1,  # 降低随机性
    # 对于 LMStudio，可能不支持 logprobs
)
```

## 🎓 推荐工作流

### 初学者
1. 下载 LMStudio
2. 安装 Llama 3.2 3B (Q4)
3. 启动服务器
4. 运行 `python aidetector_lite.py example.tex --lmstudio`

### 进阶用户
1. 使用 Llama 3.1 8B (Q5)
2. 启用 GPU 加速
3. 调整块大小和温度
4. 批量处理多个文档

### 专业用户
1. 部署 Llama 3.1 70B (Q4) 或 Mixtral 8x7B
2. 使用专用 GPU 服务器
3. 设置 API 代理服务
4. 集成到自动化工作流

## 📚 更多资源

- **LMStudio 官方文档**: https://lmstudio.ai/docs
- **模型排行榜**: https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard
- **Llama 模型**: https://huggingface.co/meta-llama
- **Qwen 模型**: https://huggingface.co/Qwen

## 🤝 社区支持

- LMStudio Discord: https://discord.gg/lmstudio
- Reddit r/LMStudio: https://reddit.com/r/lmstudio

---

**祝你使用愉快！** 🚀 有问题随时查看本指南或提交 Issue。
