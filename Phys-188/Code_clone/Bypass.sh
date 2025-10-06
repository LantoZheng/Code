#!/bin/bash

# 定义颜色代码，用于格式化输出
RED='\033[1;31m'
GRN='\033[1;32m'
BLU='\033[1;34m'
YEL='\033[1;33m'
PUR='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m'  # 无颜色，重置颜色

# 打印程序的头部信息
echo -e "${CYAN}*-------------------*---------------------*${NC}"
echo -e "${YEL}* Check MDM - Skip MDM Auto for MacOS by *${NC}"
echo -e "${RED}*      SKIPMDM.COM      *${NC}"
echo -e "${RED}*      Phoenix Team      *${NC}"
echo -e "${CYAN}*-------------------*---------------------*${NC}"
echo ""

# 设置菜单提示符
PS3='Please enter your choice: '

# 定义菜单选项
options=("Autoypass on Recovery" "Reboot")

# 使用 select 提供菜单选择
select opt in "${options[@]}"; do
    case $opt in
    # 如果选择 "Autoypass on Recovery"
    "Autoypass on Recovery")
        echo -e "${GRN}Bypass on Recovery"
        
        # 检查是否存在 "Macintosh HD - Data" 分区，如果有则重命名
        if [ -d "/Volumes/Macintosh HD - Data" ]; then
            diskutil rename "Macintosh HD - Data" "Data"
        fi

        echo -e "${GRN}Create a new user / Tạo User mới"
        echo -e "${BLU}Press Enter to continue, Note: Leaving it blank will default to the automatic user / Nhấn Enter để tiếp tục, Lưu ý: có thể không điền sẽ tự động nhận User mặc định"

        # 提示输入用户名，默认为 "Apple"
        echo -e "Enter the username (Default: Apple) / Nhập tên User (Mặc định: Apple)"
        read realName
        realName="${realName:=Apple}"

        echo -e "${BLUE}Nhận username ${RED}WRITE WITHOUT SPACES / VIẾT LIỀN KHÔNG DẤU ${GRN} (Mặc định: Apple)"
        read username
        username="${username:=Apple}"

        # 提示输入密码，默认为 "1234"
        echo -e "${BLUE}Enter the password (default: 1234) / Nhập mật khẩu (mặc định: 1234)"
        read passw
        passw="${passw:=1234}"

        # 定义用户数据库路径
        dscl_path='/Volumes/Data/private/var/db/dslocal/nodes/Default'

        echo -e "${GREEN}Creating User / Đang tạo User"
        
        # 使用 dscl 命令创建用户并设置属性
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username"
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username" UserShell "/bin/zsh"
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username" RealName "$realName"
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username" UniqueID "501"
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username" PrimaryGroupID "20"
        
        # 创建用户主目录
        mkdir "/Volumes/Data/Users/$username"
        dscl -f "$dscl_path" localhost -create "/Local/Default/Users/$username" NFSHomeDirectory "/Users/$username"
        
        # 设置用户密码
        dscl -f "$dscl_path" localhost -passwd "/Local/Default/Users/$username" "$passw"
        
        # 将用户添加到管理员组
        dscl -f "$dscl_path" localhost -append "/Local/Default/Groups/admin" GroupMembership $username

        # 修改 /etc/hosts 文件，阻止与 MDM 相关的域名
        echo "0.0.0.0 deviceenrollment.apple.com" >>/Volumes/Macintosh\ HD/etc/hosts
        echo "0.0.0.0 mdmenrollment.apple.com" >>/Volumes/Macintosh\ HD/etc/hosts
        echo "0.0.0.0 iprofiles.apple.com" >>/Volumes/Macintosh\ HD/etc/hosts
        
        echo -e "${GREEN}Successfully blocked host / Thành công chặn host${NC}"

        # 创建 AppleSetupDone 文件，标记设置已完成
        touch /Volumes/Data/private/var/db/.AppleSetupDone
        
        # 删除 MDM 配置文件
        rm -rf /Volumes/Macintosh\ HD/var/db/ConfigurationProfiles/Settings/.cloudConfigHasActivationRecord
        rm -rf /Volumes/Macintosh\ HD/var/db/ConfigurationProfiles/Settings/.cloudConfigRecordFound
        
        # 创建伪造的 MDM 配置文件，避免设备再次被配置
        touch /Volumes/Macintosh\ HD/var/db/ConfigurationProfiles/Settings/.cloudConfigProfileInstalled
        touch /Volumes/Macintosh\ HD/var/db/ConfigurationProfiles/Settings/.cloudConfigRecordNotFound

        echo -e "${CYAN}------ Autobypass SUCCESSFULLY / Autobypass HOÀN TẤT ------${NC}"
        echo -e "${CYAN}------ Exit Terminal , Reset Macbook and ENJOY ! ------${NC}"
        break
        ;;

    # 重启选项
    "Reboot")
        echo "Rebooting..."
        reboot
        break
        ;;

    # 无效选项处理
    *) 
        echo "Invalid option $REPLY"
        ;;
    esac
done
