#!/bin/bash
# NextFrame Bypass Dylib 编译脚本
# 编译为 Universal Binary (x86_64 + arm64)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_FILE="$SCRIPT_DIR/NextFrameBypass.m"
OUTPUT_FILE="$SCRIPT_DIR/NextFrameBypass.dylib"

# 临时文件
ARM64_OUTPUT="$SCRIPT_DIR/NextFrameBypass_arm64.dylib"
X86_64_OUTPUT="$SCRIPT_DIR/NextFrameBypass_x86_64.dylib"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}NextFrame Bypass Dylib 编译${NC}"
echo -e "${CYAN}========================================${NC}"
echo

# 检查源文件
if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}错误: 源文件不存在: $SOURCE_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 源文件: $SOURCE_FILE${NC}"

# 编译选项
COMMON_FLAGS="-dynamiclib -framework Foundation -framework AppKit -framework Security -fobjc-arc -O2"

# 编译 arm64
echo
echo -e "${CYAN}编译 arm64...${NC}"
clang $COMMON_FLAGS \
    -arch arm64 \
    -o "$ARM64_OUTPUT" \
    "$SOURCE_FILE"
echo -e "${GREEN}✓ arm64 编译完成${NC}"

# 编译 x86_64
echo -e "${CYAN}编译 x86_64...${NC}"
clang $COMMON_FLAGS \
    -arch x86_64 \
    -o "$X86_64_OUTPUT" \
    "$SOURCE_FILE"
echo -e "${GREEN}✓ x86_64 编译完成${NC}"

# 合并为 Universal Binary
echo -e "${CYAN}合并为 Universal Binary...${NC}"
lipo -create "$ARM64_OUTPUT" "$X86_64_OUTPUT" -output "$OUTPUT_FILE"
echo -e "${GREEN}✓ Universal Binary 创建完成${NC}"

# 清理临时文件
rm -f "$ARM64_OUTPUT" "$X86_64_OUTPUT"

# 签名 (ad-hoc)
echo -e "${CYAN}签名 dylib...${NC}"
codesign -fs - "$OUTPUT_FILE"
echo -e "${GREEN}✓ 签名完成${NC}"

# 验证
echo
echo -e "${CYAN}验证输出:${NC}"
file "$OUTPUT_FILE"
echo
codesign -dv "$OUTPUT_FILE" 2>&1 | head -5

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}编译成功!${NC}"
echo -e "${GREEN}输出文件: $OUTPUT_FILE${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${YELLOW}下一步: 运行 ./inject.sh 注入到应用${NC}"
