# NextFrame Bypass

NextFrame v1.081 授权绕过工具。

## 目录结构

```
NextFrame/
├── Contents/                    # 原始应用内容（已注入 dylib）
├── Distribution/
│   └── NextFrame.app           # 可直接运行的绕过版本
├── Dylib/
│   ├── NextFrameBypass.m       # 绕过源代码
│   ├── NextFrameBypass.dylib   # 编译后的 dylib
│   ├── build.sh                # 编译脚本
│   ├── inject.sh               # 注入脚本
│   └── insert_dylib            # 注入工具
├── NextFrame_Bypassed.zip      # 分发包（解压即用）
├── REVERSE_ENGINEERING_REPORT.md  # 逆向分析报告
├── nextframe_mitm.py           # MITM 代理（可选）
└── run_mitm_bypass.sh          # MITM 运行脚本（可选）
```

## 使用方法

### 方法一：直接运行（推荐）

1. 解压 `NextFrame_Bypassed.zip`
2. 双击运行 `NextFrame.app`
3. 首次运行可能需要右键 -> 打开 来绑过 Gatekeeper

### 方法二：从源码构建

```bash
cd Dylib
./build.sh    # 编译 dylib
./inject.sh   # 注入到应用
```

## 绕过功能

- ✅ 跳过激活码验证
- ✅ 跳过登录验证
- ✅ 无限导出次数 (999999)
- ✅ 永久订阅状态
- ✅ 所有 API 响应修改

## 技术说明

使用 Objective-C runtime hook 技术：
- Hook `NSJSONSerialization` 修改 API 响应
- Hook `NSUserDefaults` 伪造本地状态
- Hook Swift ViewModel 类跳过 UI 验证
- 通过 `insert_dylib` 注入 LC_LOAD_DYLIB

## 注意事项

- 仅供学习研究使用
- 绕过版本仅在本地测试有效
- 如遇问题，可配合 MITM 代理使用
