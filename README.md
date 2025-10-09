## 这里是郑晓旸的所有代码的合集
这里的代码按照主题分在不同的文件夹内，可能缺少一些注释，如果有需要请与我联系。
## Here're all codes written by XiaoyangZheng
Code here are sorted by projects and placed in different folders. Shortage of notations may do exists, so please don't hesitate contacting me for more explanation or further requests. 

## 开发环境建议
- 优先使用 conda 的 `base` 环境作为默认 Python 解释器（若系统已安装）。如果要确保 VS Code/GUI 进程能看到 conda 的环境变量，建议从已激活 conda 的 shell 启动 VS Code，例如先运行：

```bash
conda activate base
code .
```

对于需要其它解释器或虚拟环境的子项目，请在对应子目录的 `README` 中说明如何切换或激活环境。

（注：仓库内部的 `.gpt-runner/copilot.gpt.md` 已包含相同的 Copilot 优先使用 `conda base` 的指示。）

## VS Code 同步配置提示
- C/C++ 任务：`.vscode/tasks.json` 已改为自动根据系统选择编译器（Windows 使用 MinGW `g++.exe`，macOS 使用 `/usr/bin/clang++`，Linux 默认 `g++`）。请确保各平台的编译器已安装并加入 PATH，若需自定义路径，可在个人设置中覆盖 `C/C++` 扩展的编译器路径。
- LaTeX 构建：`.vscode/settings.json` 将默认使用 `XeLaTeX -> Biber -> XeLaTeX*2` 配方，确保跨平台的 BibTeX/字体处理一致。macOS 建议使用 MacTeX，Windows 建议使用 TeX Live。
