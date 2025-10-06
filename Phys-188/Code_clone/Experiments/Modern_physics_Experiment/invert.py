import sys
import os
from PIL import Image, ImageOps

def invert_image(image_path):
    """反相图像并保存在同一目录下，文件名添加 "_inverted"."""
    try:
        # 打开图像
        img = Image.open(image_path)

        # 检查并转换图像模式
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        # 反相图像
        inverted_img = ImageOps.invert(img)

        # 生成输出文件名
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_inverted{ext.lower()}" # 确保扩展名为小写


        # 保存反相后的图像
        inverted_img.save(output_path)
        print(f"图像已反相并保存到: {output_path}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {image_path}")
    except IOError:
        print(f"错误：无法打开或处理图像 {image_path}。请确保它是有效的图像文件。")
    except Exception as e:
        print(f"处理图像时发生错误: {e}")



def main():
    """主函数，处理拖拽的文件。"""
    if len(sys.argv) > 1:
        # 遍历所有拖拽的文件
        for image_path in sys.argv[1:]:
            # 检查文件扩展名 (简单的检查, 实际应该用更可靠的方式)
            _, ext = os.path.splitext(image_path)
            if ext.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'):
                invert_image(image_path)
            else:
                print(f"警告：跳过非图像文件: {image_path}")
    else:
        print("请将一个或多个图像文件拖拽到此脚本上。")
    
    # 暂停，以便用户看到输出结果（在双击运行脚本时很有用）
    input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
