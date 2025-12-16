#!/bin/bash
# NextFrame Bypass Dylib 注入脚本
# 将 dylib 注入到 NextFrame.app 中

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DYLIB_FILE="$SCRIPT_DIR/NextFrameBypass.dylib"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# 应用路径 (优先使用本地副本)
APP_BUNDLE="$PARENT_DIR/Contents"
APP_EXECUTABLE="$APP_BUNDLE/MacOS/NextFrame"
APP_FRAMEWORKS="$APP_BUNDLE/Frameworks"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}NextFrame Bypass Dylib 注入${NC}"
echo -e "${CYAN}========================================${NC}"
echo

# 检查 dylib
if [ ! -f "$DYLIB_FILE" ]; then
    echo -e "${RED}错误: Dylib 不存在: $DYLIB_FILE${NC}"
    echo "请先运行 ./build.sh 编译"
    exit 1
fi

echo -e "${GREEN}✓ Dylib: $DYLIB_FILE${NC}"

# 检查应用
if [ ! -f "$APP_EXECUTABLE" ]; then
    echo -e "${YELLOW}未找到本地应用副本${NC}"
    echo "请输入 NextFrame.app 的路径 (例如 /Applications/NextFrame.app):"
    read -r APP_PATH
    
    if [ ! -d "$APP_PATH" ]; then
        echo -e "${RED}错误: 应用不存在${NC}"
        exit 1
    fi
    
    APP_BUNDLE="$APP_PATH/Contents"
    APP_EXECUTABLE="$APP_BUNDLE/MacOS/NextFrame"
    APP_FRAMEWORKS="$APP_BUNDLE/Frameworks"
fi

echo -e "${GREEN}✓ 应用: $APP_EXECUTABLE${NC}"

# 检查是否已经注入
if otool -L "$APP_EXECUTABLE" 2>/dev/null | grep -q "NextFrameBypass.dylib"; then
    echo -e "${YELLOW}⚠ 应用已经注入过 dylib${NC}"
    read -p "是否重新注入? [y/N]: " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        exit 0
    fi
fi

# 创建备份
echo
echo -e "${CYAN}创建备份...${NC}"
BACKUP_FILE="$APP_EXECUTABLE.backup.$(date +%Y%m%d%H%M%S)"
cp "$APP_EXECUTABLE" "$BACKUP_FILE"
echo -e "${GREEN}✓ 备份: $BACKUP_FILE${NC}"

# 创建 Frameworks 目录 (如果不存在)
mkdir -p "$APP_FRAMEWORKS"

# 复制 dylib 到应用内
echo -e "${CYAN}复制 dylib 到应用包...${NC}"
cp "$DYLIB_FILE" "$APP_FRAMEWORKS/"
echo -e "${GREEN}✓ 已复制到: $APP_FRAMEWORKS/NextFrameBypass.dylib${NC}"

# 检查是否有 insert_dylib 工具
if command -v insert_dylib &> /dev/null; then
    echo -e "${CYAN}使用 insert_dylib 注入...${NC}"
    insert_dylib --strip-codesig --all-yes \
        "@executable_path/../Frameworks/NextFrameBypass.dylib" \
        "$APP_EXECUTABLE" \
        "$APP_EXECUTABLE"
else
    echo -e "${YELLOW}未找到 insert_dylib 工具，使用 install_name_tool...${NC}"
    
    # 首先需要移除代码签名
    echo -e "${CYAN}移除原有签名...${NC}"
    codesign --remove-signature "$APP_EXECUTABLE" 2>/dev/null || true
    
    # 使用 install_name_tool 添加 load command
    echo -e "${CYAN}添加 LC_LOAD_DYLIB...${NC}"
    install_name_tool -add_rpath "@executable_path/../Frameworks" "$APP_EXECUTABLE" 2>/dev/null || true
    
    # 注意: install_name_tool 不能直接添加 LC_LOAD_DYLIB
    # 需要使用其他工具或手动修改
    
    echo -e "${YELLOW}⚠ install_name_tool 无法直接注入 LC_LOAD_DYLIB${NC}"
    echo -e "${YELLOW}  推荐安装 insert_dylib: brew install insert-dylib${NC}"
    echo
    echo -e "${CYAN}备选方案: 使用 DYLD_INSERT_LIBRARIES 环境变量运行${NC}"
    echo
    echo -e "  ${GREEN}DYLD_INSERT_LIBRARIES=\"$APP_FRAMEWORKS/NextFrameBypass.dylib\" \\${NC}"
    echo -e "  ${GREEN}\"$APP_EXECUTABLE\"${NC}"
    echo
    
    # 创建启动脚本
    LAUNCH_SCRIPT="$PARENT_DIR/launch_bypassed.sh"
    cat > "$LAUNCH_SCRIPT" << EOF
#!/bin/bash
# 使用注入的 dylib 启动 NextFrame

DYLD_INSERT_LIBRARIES="$APP_FRAMEWORKS/NextFrameBypass.dylib" \\
"$APP_EXECUTABLE" "\$@"
EOF
    chmod +x "$LAUNCH_SCRIPT"
    echo -e "${GREEN}✓ 已创建启动脚本: $LAUNCH_SCRIPT${NC}"
    
    # 重新签名
    echo -e "${CYAN}重新签名应用...${NC}"
    codesign -fs - --deep "$APP_BUNDLE/.." 2>/dev/null || codesign -fs - "$APP_EXECUTABLE"
    echo -e "${GREEN}✓ 签名完成${NC}"
    
    exit 0
fi

# 重新签名
echo -e "${CYAN}重新签名应用...${NC}"
codesign -fs - --deep "$APP_BUNDLE/.." 2>/dev/null || codesign -fs - "$APP_EXECUTABLE"
echo -e "${GREEN}✓ 签名完成${NC}"

# 验证
echo
echo -e "${CYAN}验证注入:${NC}"
otool -L "$APP_EXECUTABLE" | grep -E "(NextFrameBypass|Frameworks)" || echo "(无法验证)"

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}注入完成!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${YELLOW}现在可以正常启动 NextFrame，bypass 将自动生效${NC}"
echo -e "${YELLOW}查看日志: log stream --predicate 'eventMessage contains \"NextFrame Bypass\"'${NC}"
