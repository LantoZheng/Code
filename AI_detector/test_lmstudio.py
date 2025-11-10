#!/usr/bin/env python3
"""
LMStudio 连接测试工具
用于验证 LMStudio 服务器是否正常运行
"""

import sys
import argparse
from openai import OpenAI


def test_lmstudio_connection(url: str = "http://localhost:1234/v1"):
    """测试 LMStudio 连接"""
    
    print(f"🔍 测试 LMStudio 连接: {url}")
    print("=" * 60)
    
    try:
        client = OpenAI(
            api_key="lm-studio",
            base_url=url
        )
        
        # 1. 测试模型列表
        print("\n1️⃣  获取可用模型...")
        models = client.models.list()
        
        if not models.data:
            print("❌ 没有找到可用模型")
            print("   请在 LMStudio 中加载模型")
            return False
        
        print(f"✅ 找到 {len(models.data)} 个模型:")
        for model in models.data:
            print(f"   - {model.id}")
        
        # 2. 测试简单对话
        print("\n2️⃣  测试对话功能...")
        model_id = models.data[0].id
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "你是一个测试助手。"},
                {"role": "user", "content": "请回复'测试成功'"}
            ],
            max_tokens=20,
            temperature=0.1
        )
        
        reply = response.choices[0].message.content
        print(f"✅ 模型响应: {reply}")
        
        # 3. 测试 logprobs（用于困惑度计算）
        print("\n3️⃣  测试 logprobs 支持...")
        try:
            response_with_logprobs = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "user", "content": "测试"}
                ],
                max_tokens=5,
                logprobs=True
            )
            
            if response_with_logprobs.choices[0].logprobs:
                print("✅ Logprobs 支持正常")
            else:
                print("⚠️  Logprobs 可能不受支持")
                print("   AI 检测功能可能受限")
        except Exception as e:
            print(f"⚠️  Logprobs 测试失败: {e}")
            print("   AI 检测功能可能受限")
        
        print("\n" + "=" * 60)
        print("✅ LMStudio 连接测试通过！")
        print(f"✅ 可以使用 --lmstudio 参数运行脚本")
        print("\n使用示例:")
        print(f"  python aidetector_lite.py paper.tex --lmstudio")
        if url != "http://localhost:1234/v1":
            print(f"  python aidetector_lite.py paper.tex --lmstudio --lmstudio-url {url}")
        
        return True
        
    except ConnectionError as e:
        print(f"\n❌ 连接失败: {e}")
        print("\n请检查:")
        print("  1. LMStudio 是否正在运行")
        print("  2. 本地服务器是否已启动")
        print("  3. 端口号是否正确")
        print(f"  4. URL 是否正确: {url}")
        return False
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='测试 LMStudio 连接',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 测试默认地址
  python test_lmstudio.py
  
  # 测试自定义地址
  python test_lmstudio.py --url http://localhost:5000/v1
        """
    )
    parser.add_argument(
        '--url',
        default='http://localhost:1234/v1',
        help='LMStudio 服务器地址（默认: http://localhost:1234/v1）'
    )
    
    args = parser.parse_args()
    
    success = test_lmstudio_connection(args.url)
    
    if not success:
        print("\n💡 需要帮助？")
        print("   查看详细指南: LMSTUDIO_GUIDE.md")
        print("   或访问: https://lmstudio.ai/docs")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
