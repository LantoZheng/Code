import os
import subprocess
import shutil

def create_dmg(app_name, app_path, dmg_name, output_dir):
    # 创建临时文件夹来存放 .dmg 文件内容
    temp_dir = os.path.join(output_dir, "temp_dmg")
    os.makedirs(temp_dir, exist_ok=True)

    # 将 .app 文件复制到临时文件夹
    app_dest = os.path.join(temp_dir, f"{app_name}.app")
    shutil.copytree(app_path, app_dest)

    # 创建指向系统应用程序文件夹的快捷方式
    applications_symlink = os.path.join(temp_dir, "Applications")
    if not os.path.exists(applications_symlink):
        os.symlink("/Applications", applications_symlink)

    # 创建 .dmg 文件路径
    dmg_path = os.path.join(output_dir, f"{dmg_name}.dmg")
    
    # 使用 hdiutil 创建可写的 .dmg 文件
    create_dmg_command = [
        "hdiutil", "create", "-volname", dmg_name, "-srcfolder", temp_dir,
        "-ov", "-format", "UDRW", dmg_path
    ]
    subprocess.run(create_dmg_command, check=True)

    # 挂载 .dmg 文件
    attach_command = ["hdiutil", "attach", dmg_path, "-mountpoint", "/Volumes/" + dmg_name]
    subprocess.run(attach_command, check=True)

    # 卸载 .dmg 文件
    detach_command = ["hdiutil", "detach", "/Volumes/" + dmg_name]
    subprocess.run(detach_command, check=True)

    # 将 .dmg 文件转换为只读模式
    final_dmg_path = os.path.join(output_dir, f"{dmg_name}_final.dmg")
    convert_command = ["hdiutil", "convert", dmg_path, "-format", "UDZO", "-o", final_dmg_path]
    subprocess.run(convert_command, check=True)

    # 删除临时文件夹和可写的 .dmg 文件
    shutil.rmtree(temp_dir)
    os.remove(dmg_path)

    print(f"{final_dmg_path} 创建成功！")

# 使用方法
app_name = "PicaComic"  # 替换为你的应用名称
app_path = "/Users/zhengxiaoyang/Downloads/PicaComic.app "  # 替换为你的 .app 文件路径
dmg_name = "PicaComic"  # 替换为 .dmg 文件名称
output_dir = "/Users/zhengxiaoyang/Downloads"  # 替换为你想要输出的文件夹

create_dmg(app_name, app_path, dmg_name, output_dir)