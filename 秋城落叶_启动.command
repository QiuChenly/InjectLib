#!/bin/sh
cd "${0%/*}" || exit 1
# 定义 Keychain 服务名称和账户名称
SERVICE_NAME="InjectLib"
ACCOUNT_NAME="sudo"
# 如果 Keychain 中没有密码，则提示用户输入
if [ -z "$PASSWD" ]; then
    read -p "⚙️ 请输入密码(明文)然后回车: " -r passwd
    printf "\r\033[1A%s" "" 1>&2
    printf "\r\033[K%s" "" 1>&2
    
    # 验证密码是否正确
    if ! echo "$passwd" | sudo -S true 2>/dev/null; then
        echo "❌ 密码错误，请重试"
        exit 1
    fi
    
    # 将密码保存到 Keychain
    security add-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w "$passwd" -U
    PASSWD=$passwd
else
    # 验证 Keychain 中的密码是否正确
    if ! echo "$PASSWD" | sudo -S true 2>/dev/null; then
        echo "❌ Keychain 中的密码已失效，请重新输入"
        # 删除错误的密码
        security delete-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" 2>/dev/null
        read -p "⚙️ 请输入密码(明文)然后回车: " -r passwd
        printf "\r\033[1A%s" "" 1>&2
        printf "\r\033[K%s" "" 1>&2
        
        # 再次验证新密码
        if ! echo "$passwd" | sudo -S true 2>/dev/null; then
            echo "❌ 密码错误，请重试"
            exit 1
        fi
        
        # 保存新密码到 Keychain
        security add-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w "$passwd" -U
        PASSWD=$passwd
    fi
fi

find . -name "*.*" 2>/dev/null | xargs otool -l 2>/dev/null | grep -E "(minos|sdk)" 2>/dev/null
echo "$PASSWD" | sudo -S echo "⚙️ 当前是 $(sudo -S whoami) 用户"
chmod +x tool/optool
sudo -S python3 main.py