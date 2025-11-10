#!/bin/bash

# 测试脚本 - 验证工具是否正常工作

echo "🧪 AI Detector 测试脚本"
echo "======================="
echo ""

# 检查 Python
echo "1. 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python3 已安装: $(python3 --version)"
echo ""

# 检查依赖
echo "2. 检查依赖..."
python3 -c "import openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  openai 包未安装，正在安装..."
    pip install openai
fi

python3 -c "import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  numpy 包未安装，正在安装..."
    pip install numpy
fi
echo "✅ 依赖检查完成"
echo ""

# 检查后端选择
echo "3. 检查可用后端..."
BACKEND_AVAILABLE=false

# 检查 LMStudio
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LMStudio 本地服务器正在运行"
    BACKEND_AVAILABLE=true
    USE_LMSTUDIO=true
else
    echo "⚠️  LMStudio 服务器未运行"
    USE_LMSTUDIO=false
fi

# 检查 OpenAI API
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY 环境变量未设置"
    if [ "$BACKEND_AVAILABLE" = false ]; then
        echo ""
        echo "❌ 错误：没有可用的后端！"
        echo ""
        echo "请选择以下之一："
        echo "  1. 启动 LMStudio 服务器（推荐，免费）"
        echo "     - 下载: https://lmstudio.ai/"
        echo "     - 详细指南: 查看 LMSTUDIO_GUIDE.md"
        echo ""
        echo "  2. 设置 OpenAI API 密钥"
        echo "     - 运行: export OPENAI_API_KEY='your-api-key'"
        exit 1
    fi
else
    echo "✅ OpenAI API 密钥已设置"
    BACKEND_AVAILABLE=true
fi
echo ""

# 检查示例文件
echo "4. 检查示例文件..."
if [ ! -f "example.tex" ]; then
    echo "❌ example.tex 不存在"
    exit 1
fi
echo "✅ 示例文件存在"
echo ""

# 显示使用说明
echo "📖 使用说明"
echo "==========="
echo ""
if [ "$USE_LMSTUDIO" = true ]; then
    echo "🏠 使用 LMStudio（推荐，免费）："
    echo "  python3 aidetector_lite.py example.tex --lmstudio"
    echo ""
    echo "完整版（LMStudio）："
    echo "  python3 aidetector.py example.tex --lmstudio"
    echo ""
else
    echo "☁️  使用 OpenAI API："
    echo "  python3 aidetector_lite.py example.tex -k $OPENAI_API_KEY"
    echo ""
    echo "完整版（OpenAI）："
    echo "  python3 aidetector.py example.tex -k $OPENAI_API_KEY"
    echo ""
fi
echo "自定义输出："
echo "  python3 aidetector_lite.py example.tex -o my_report.html"
echo ""
echo "调整块大小："
echo "  python3 aidetector_lite.py example.tex -c 50"
echo ""

# 询问是否运行测试
read -p "是否运行测试示例？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ "$BACKEND_AVAILABLE" = false ]; then
        echo "❌ 没有可用的后端"
        exit 1
    fi
    
    echo ""
    if [ "$USE_LMSTUDIO" = true ]; then
        echo "🚀 运行轻量版测试（使用 LMStudio）..."
        echo "========================================"
        python3 aidetector_lite.py example.tex --lmstudio -c 50
    else
        echo "🚀 运行轻量版测试（使用 OpenAI API）..."
        echo "========================================"
        python3 aidetector_lite.py example.tex -k "$OPENAI_API_KEY" -c 50
    fi
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 测试成功！"
        echo "📄 查看报告: open example_report.html"
    else
        echo ""
        echo "❌ 测试失败"
        exit 1
    fi
fi

echo ""
echo "✨ 测试完成！"
