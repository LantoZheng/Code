# 中国科学技术大学Beamer模板

本项目是基于 [thomasWeise/ustcSlides](https://github.com/thomasWeise/ustcSlides) 修改而来，加了几种不同的颜色主题。

科大官网上有与之对应的[USTC公用PPT模板](http://lswhw.ustc.edu.cn/public/inc/editer/attached/file/20181106/20181106152958_72346.zip)。

## 使用说明

主文件 `main.tex`， 使用 `xelatex` 引擎编译。

宏包使用了TikZ代码形式的背景文件（在子文件夹theme中），默认选项 `bluetheme` 是科大校徽的蓝色；此外 `ustcbeamer` 还内置了红色和黑色主题 `redtheme`、`blacktheme`。

## 自定义你的主题颜色

一旦在 `main.tex` 中载入 `ustcbeamer` 后使用了下述命令就会覆盖 `ustcbeamer` 指定的内置颜色选项，你可以设置自己喜欢的RGB色值：

`\definecolor{themecolor}{RGB}{0,150,150}` % 这是青色主题；

`\definecolor{themecolor}{rgb}{0,0.5,0.3}` % 这是深绿色主题；

注意小写rgb和大写RGB表示的色值相差255倍，即RGB{255,255,255}=rgb{1,1,1}；建议自定义的主题颜色选择偏深色。


## 下载地址

- GitHub Releases：https://github.com/ustctug/ustcbeamer/releases


## 其他

采纳了 [Freed-Wu](https://github.com/Freed-Wu) 的建议，使用 `svg2tikz` 来生成TikZ格式的背景文件，得以保留各类主题色的同时还能摆脱繁重的背景PDF文件，在此致谢！

欢迎同学们反馈其他问题。
