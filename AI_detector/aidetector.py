#!/usr/bin/env python3
"""
LaTeX AI Content Detector
通过计算词元的困惑度（perplexity）来检测 LaTeX 文档中可能由 AI 生成的内容
使用颜色高亮显示：蓝色（低概率）-> 绿色 -> 黄色 -> 红色（高概率）
"""

import os
import re
import argparse
import numpy as np
from typing import List, Tuple, Optional
from openai import OpenAI


class LaTeXAIDetector:
    """LaTeX 文档 AI 内容检测器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo", 
                 use_lmstudio: bool = False, lmstudio_url: str = "http://localhost:1234/v1"):
        """
        初始化检测器
        
        Args:
            api_key: OpenAI API 密钥（use_lmstudio=True 时可选）
            model: 使用的模型名称
            use_lmstudio: 是否使用 LMStudio 本地模型
            lmstudio_url: LMStudio 服务器地址
        """
        self.use_lmstudio = use_lmstudio
        self.model = model
        
        if use_lmstudio:
            # 使用 LMStudio 本地服务
            self.client = OpenAI(
                api_key="lm-studio",  # LMStudio 不需要真实密钥
                base_url=lmstudio_url
            )
            print(f"🏠 使用 LMStudio 本地模型: {lmstudio_url}")
        else:
            # 使用 OpenAI API
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数，或使用 --lmstudio 选项")
            
            self.client = OpenAI(api_key=self.api_key)
            print(f"☁️  使用 OpenAI API")
        
    def extract_text_from_latex(self, latex_content: str) -> List[str]:
        """
        从 LaTeX 文档中提取文本内容
        
        Args:
            latex_content: LaTeX 源代码
            
        Returns:
            List of tokens (words)
        """
        # 移除注释
        lines = latex_content.split('\n')
        processed_lines = []
        
        for line in lines:
            # 保留 % 前的内容（除非 % 被转义）
            comment_pos = line.find('%')
            if comment_pos > 0 and line[comment_pos - 1] != '\\':
                line = line[:comment_pos]
            processed_lines.append(line)
        
        content = '\n'.join(processed_lines)
        
        # 移除常见的 LaTeX 命令但保留文本
        # 移除 \begin{} 和 \end{} 但保留内容
        content = re.sub(r'\\begin\{[^}]+\}', '', content)
        content = re.sub(r'\\end\{[^}]+\}', '', content)
        
        # 移除常见的格式命令但保留参数
        content = re.sub(r'\\(textbf|textit|emph|underline)\{([^}]+)\}', r'\2', content)
        content = re.sub(r'\\(section|subsection|subsubsection|chapter|paragraph)\{([^}]+)\}', r'\2', content)
        
        # 移除其他单行命令
        content = re.sub(r'\\[a-zA-Z]+\s*', ' ', content)
        
        # 移除数学模式
        content = re.sub(r'\$[^$]+\$', ' [MATH] ', content)
        content = re.sub(r'\\\[[^\]]+\\\]', ' [MATH] ', content)
        
        # 分词（简单按空格和标点分割）
        words = re.findall(r'\b\w+\b|[.,;:!?]', content)
        
        return words
    
    def calculate_token_perplexity(self, context: str, token: str) -> float:
        """
        计算给定上下文中某个词元出现的困惑度
        
        Args:
            context: 前文上下文
            token: 待检测的词元
            
        Returns:
            困惑度值（越低表示越可能由 AI 生成）
        """
        try:
            # 构建提示，让模型预测下一个词
            prompt = f"请根据以下文本，预测下一个最可能出现的词。只返回一个词，不要解释。\n\n文本：{context}\n\n下一个词："
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个文本预测助手，只返回最可能的下一个词。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1,
                logprobs=True,
                top_logprobs=20
            )
            
            # 获取 logprobs
            if response.choices[0].logprobs and response.choices[0].logprobs.content:
                top_logprobs = response.choices[0].logprobs.content[0].top_logprobs
                
                # 查找目标 token 的 logprob
                token_lower = token.lower()
                for logprob_item in top_logprobs:
                    if logprob_item.token.lower().strip() == token_lower:
                        # 转换为概率
                        prob = np.exp(logprob_item.logprob)
                        # 困惑度 = 1 / 概率
                        perplexity = 1.0 / prob if prob > 0 else float('inf')
                        return perplexity
                
                # 如果没找到，返回一个较高的困惑度
                return 100.0
            
            return 50.0  # 默认中等困惑度
            
        except Exception as e:
            print(f"计算困惑度时出错: {e}")
            return 50.0
    
    def analyze_document(self, latex_content: str, window_size: int = 50) -> List[Tuple[str, float]]:
        """
        分析整个文档，计算每个词元的困惑度
        
        Args:
            latex_content: LaTeX 源代码
            window_size: 上下文窗口大小（词数）
            
        Returns:
            List of (token, perplexity) tuples
        """
        tokens = self.extract_text_from_latex(latex_content)
        results = []
        
        print(f"开始分析，共 {len(tokens)} 个词元...")
        
        for i, token in enumerate(tokens):
            # 构建上下文（前 window_size 个词）
            start_idx = max(0, i - window_size)
            context = ' '.join(tokens[start_idx:i])
            
            if len(context.strip()) == 0:
                # 第一个词，困惑度设为中等
                perplexity = 50.0
            else:
                perplexity = self.calculate_token_perplexity(context, token)
            
            results.append((token, perplexity))
            
            if (i + 1) % 10 == 0:
                print(f"已处理 {i + 1}/{len(tokens)} 个词元...")
        
        return results
    
    def perplexity_to_color(self, perplexity: float) -> str:
        """
        将困惑度映射到颜色
        困惑度越低，AI 生成概率越高，颜色越红
        
        Args:
            perplexity: 困惑度值
            
        Returns:
            LaTeX 颜色代码
        """
        # 归一化困惑度到 [0, 1] 区间
        # 假设困惑度范围是 [1, 100]
        if perplexity <= 1:
            normalized = 0.0
        elif perplexity >= 100:
            normalized = 1.0
        else:
            # 使用对数尺度
            normalized = np.log(perplexity) / np.log(100)
        
        # 反转：困惑度低 -> normalized 低 -> AI 概率高
        ai_prob = 1.0 - normalized
        
        if ai_prob >= 0.75:
            return "red"  # 高 AI 概率
        elif ai_prob >= 0.5:
            return "orange"  # 中高 AI 概率
        elif ai_prob >= 0.25:
            return "yellow"  # 中等 AI 概率
        elif ai_prob >= 0.1:
            return "green"  # 低 AI 概率
        else:
            return "blue"  # 很低 AI 概率
    
    def generate_highlighted_latex(self, latex_content: str, analysis_results: List[Tuple[str, float]]) -> str:
        """
        生成带颜色高亮的 LaTeX 文档
        
        Args:
            latex_content: 原始 LaTeX 内容
            analysis_results: 分析结果
            
        Returns:
            带高亮的 LaTeX 内容
        """
        # 在文档开头添加必要的包
        preamble = r"""\usepackage{xcolor}
\usepackage{soul}

% 定义高亮命令
\newcommand{\hlblue}[1]{\sethlcolor{blue!20}\hl{#1}}
\newcommand{\hlgreen}[1]{\sethlcolor{green!20}\hl{#1}}
\newcommand{\hlyellow}[1]{\sethlcolor{yellow!40}\hl{#1}}
\newcommand{\hlorange}[1]{\sethlcolor{orange!40}\hl{#1}}
\newcommand{\hlred}[1]{\sethlcolor{red!40}\hl{#1}}

"""
        
        # 查找 \begin{document} 并在其前插入 preamble
        if r'\begin{document}' in latex_content:
            parts = latex_content.split(r'\begin{document}', 1)
            highlighted_content = parts[0] + preamble + r'\begin{document}' + parts[1]
        else:
            highlighted_content = preamble + latex_content
        
        # 为每个检测到的词元添加高亮
        # 这部分需要更复杂的实现来准确定位原文中的词元
        # 简化版本：添加图例
        legend = r"""
\vspace{1cm}
\noindent\textbf{AI 检测图例：}\\
\hlblue{蓝色} - 极低 AI 概率 \quad
\hlgreen{绿色} - 低 AI 概率 \quad
\hlyellow{黄色} - 中等 AI 概率 \quad
\hlorange{橙色} - 高 AI 概率 \quad
\hlred{红色} - 极高 AI 概率

\vspace{0.5cm}
"""
        
        # 在 \begin{document} 后添加图例
        highlighted_content = highlighted_content.replace(
            r'\begin{document}',
            r'\begin{document}' + '\n' + legend
        )
        
        return highlighted_content
    
    def process_file(self, input_file: str, output_file: str, window_size: int = 50):
        """
        处理 LaTeX 文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            window_size: 上下文窗口大小
        """
        print(f"读取文件: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        print("开始分析文档...")
        analysis_results = self.analyze_document(latex_content, window_size)
        
        print("生成带高亮的 LaTeX 文档...")
        highlighted_latex = self.generate_highlighted_latex(latex_content, analysis_results)
        
        print(f"保存结果到: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(highlighted_latex)
        
        # 生成统计报告
        perplexities = [p for _, p in analysis_results]
        print("\n=== 统计报告 ===")
        print(f"总词元数: {len(analysis_results)}")
        print(f"平均困惑度: {np.mean(perplexities):.2f}")
        print(f"困惑度中位数: {np.median(perplexities):.2f}")
        print(f"最低困惑度: {np.min(perplexities):.2f}")
        print(f"最高困惑度: {np.max(perplexities):.2f}")
        
        # 统计各颜色区间的词元数
        colors = [self.perplexity_to_color(p) for _, p in analysis_results]
        color_counts = {
            'blue': colors.count('blue'),
            'green': colors.count('green'),
            'yellow': colors.count('yellow'),
            'orange': colors.count('orange'),
            'red': colors.count('red')
        }
        
        print("\n颜色分布:")
        for color, count in color_counts.items():
            percentage = (count / len(colors)) * 100 if colors else 0
            print(f"{color}: {count} ({percentage:.1f}%)")
        
        print("\n完成！")


def main():
    parser = argparse.ArgumentParser(
        description='LaTeX AI 内容检测器 - 通过困惑度分析识别可能由 AI 生成的内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用 OpenAI API
  python aidetector.py paper.tex -k YOUR_API_KEY
  
  # 使用 LMStudio 本地模型（推荐，免费）
  python aidetector.py paper.tex --lmstudio
  
  # 指定 LMStudio 服务器地址
  python aidetector.py paper.tex --lmstudio --lmstudio-url http://localhost:1234/v1
        """
    )
    parser.add_argument('input', help='输入的 LaTeX 文件路径')
    parser.add_argument('-o', '--output', help='输出的 LaTeX 文件路径（默认为 input_highlighted.tex）')
    parser.add_argument('-k', '--api-key', help='OpenAI API 密钥（也可通过 OPENAI_API_KEY 环境变量设置）')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo', help='使用的模型（默认: gpt-3.5-turbo）')
    parser.add_argument('-w', '--window', type=int, default=50, help='上下文窗口大小（默认: 50）')
    parser.add_argument('--lmstudio', action='store_true', help='使用 LMStudio 本地模型（免费，需先启动 LMStudio 服务）')
    parser.add_argument('--lmstudio-url', default='http://localhost:1234/v1', help='LMStudio 服务器地址（默认: http://localhost:1234/v1）')
    
    args = parser.parse_args()
    
    # 确定输出文件名
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(args.input)[0]
        output_file = f"{base_name}_highlighted.tex"
    
    # 创建检测器并处理文件
    try:
        detector = LaTeXAIDetector(
            api_key=args.api_key, 
            model=args.model,
            use_lmstudio=args.lmstudio,
            lmstudio_url=args.lmstudio_url
        )
        detector.process_file(args.input, output_file, args.window)
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
