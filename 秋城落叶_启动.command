#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")" || exit 1

SERVICE_NAME="InjectLib"
ACCOUNT_NAME="sudo"

askpass() {               
  IFS= read -r -s -p "⚙️ 请输入密码(明文)然后回车: " pass
  printf '\n'              
  echo "$pass"
}

validate() {               # 校验密码是否能用来 sudo
  printf '%s\n' "$1" | sudo -S -v &>/dev/null
}

save_to_keychain() {       # 写入或更新 Keychain
  security add-generic-password \
    -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w "$1" -U
}

load_from_keychain() {     # 读取 Keychain
  security find-generic-password \
    -s "$SERVICE_NAME" -a "$ACCOUNT_NAME" -w 2>/dev/null || true
}

PASSWD="${PASSWD:-}"             
[[ -z $PASSWD ]] && PASSWD="$(load_from_keychain)" 

# 如果取不到，或取到了但验证失败，就循环让用户输入
until validate "$PASSWD"; do
  [[ -n $PASSWD ]] && echo "❌ 密码错误，请重试"
  PASSWD="$(askpass)"
  validate "$PASSWD" || continue
  save_to_keychain "$PASSWD"
done

printf '%s\n' "$PASSWD" | sudo -S -v

sudo -E python3 main.py
