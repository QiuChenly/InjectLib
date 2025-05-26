#!/bin/sh
cd "${0%/*}" || exit 1

# 定义 Keychain 服务名称和账户名称
SERVICE_NAME="InjectLib"
ACCOUNT_NAME="sudo"

# 获取 Keychain 中保存的密码
get_keychain_password() {
    security find-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w 2>/dev/null
}

# 验证密码是否正确的函数
verify_password() {
    local password="$1"
    # 使用 printf 而不是 echo 来避免特殊字符解释问题
    printf '%s\n' "$password" | sudo -S true 2>/dev/null
}

# 安全地提示用户输入密码
prompt_password() {
    printf "⚙️ 请输入密码(明文)然后回车: "
    # 使用 IFS= 和 -r 标志来保留所有字符，包括空格
    IFS= read -r passwd
    # 清除显示的密码输入行
    printf "\r\033[1A\033[K" >&2
    echo "$passwd"
}

# 保存密码到 Keychain
save_to_keychain() {
    local password="$1"
    # 删除可能存在的旧密码
    security delete-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" 2>/dev/null
    # 添加新密码，使用引号保护特殊字符
    security add-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w "$password" -U
}

# 主逻辑
PASSWD=$(get_keychain_password)

if [ -z "$PASSWD" ]; then
    # Keychain 中没有密码，提示用户输入
    passwd=$(prompt_password)
    
    # 验证密码是否正确
    if verify_password "$passwd"; then
        # 密码正确，保存到 Keychain
        save_to_keychain "$passwd"
        PASSWD="$passwd"
        echo "✅ 密码已保存到 Keychain"
    else
        echo "❌ 密码错误，请重试"
        exit 1
    fi
else
    # Keychain 中有密码，验证是否正确
    if verify_password "$PASSWD"; then
        echo "✅ 使用 Keychain 中的密码"
    else
        echo "❌ Keychain 中的密码已失效，请重新输入"
        # 删除错误的密码
        security delete-generic-password -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" 2>/dev/null
        
        # 提示用户重新输入
        passwd=$(prompt_password)
        
        # 验证新密码
        if verify_password "$passwd"; then
            # 保存新密码到 Keychain
            save_to_keychain "$passwd"
            PASSWD="$passwd"
            echo "✅ 新密码已保存到 Keychain"
        else
            echo "❌ 密码错误，请重试"
            exit 1
        fi
    fi
fi

# 执行其他命令
find . -name "*.*" 2>/dev/null | xargs otool -l 2>/dev/null | grep -E "(minos|sdk)" 2>/dev/null

# 使用 printf 而不是 echo 来避免密码中的特殊字符被解释
printf '%s\n' "$PASSWD" | sudo -S sh -c 'echo "⚙️ 当前是 $(whoami) 用户"'

chmod +x tool/optool
printf '%s\n' "$PASSWD" | sudo -S python3 main.py
