COLOR_INFO='\033[0;34m'
COLOR_ERR='\033[0;35m'
NOCOLOR='\033[0m'
PDFM_VER="19.4.0-54962"

echo "${COLOR_INFO}[*] 确保你的版本是: https://download.parallels.com/desktop/v19/${PDFM_VER}/ParallelsDesktop-${PDFM_VER}.dmg"

if pgrep -x "prl_disp_service" &>/dev/null; then
  echo "${COLOR_INFO}[*] 正在停止 Parallels Desktop 主程序..."
  pkill -9 prl_client_app &>/dev/null
  "/Applications/Parallels Desktop.app/Contents/MacOS/Parallels Service" service_stop &>/dev/null
  sleep 1
  launchctl stop /Library/LaunchDaemons/com.parallels.desktop.launchdaemon.plist &>/dev/null
  sleep 1
  pkill -9 prl_disp_service &>/dev/null
  sleep 1
  rm -f "/var/run/prl_*"
fi

sudo cp "./tool/91QiuChenly.dylib" "/Applications/Parallels Desktop.app/Contents/Frameworks/91QiuChenly.dylib"

para_load="@rpath/91QiuChenly.dylib"
pd_dir="/Applications/Parallels Desktop.app"
insert_dylib_file="tool/insert_dylib"

# patch dispatcher
pd_dispatcher_file="$pd_dir/Contents/MacOS/Parallels Service.app/Contents/MacOS/prl_disp_service"

# 判断文件是否存在 如果不存在就备份
if [ ! -f "$pd_dispatcher_file"_backup ]; then
    cp "$pd_dispatcher_file" "$pd_dispatcher_file"_backup
fi
cp "$pd_dispatcher_file"_backup "$pd_dispatcher_file"

"$insert_dylib_file" "$para_load" "$pd_dispatcher_file"_backup "$pd_dispatcher_file"
codesign -f -s - --timestamp=none --all-architectures --entitlements "./tool/ParallelsDesktop/Service.entitlements" "$pd_dispatcher_file"

# patch vm
pd_vm_file="$pd_dir/Contents/MacOS/Parallels VM.app/Contents/MacOS/prl_vm_app"

if [ ! -f "$pd_vm_file"_backup ]; then
    cp "$pd_vm_file" "$pd_vm_file"_backup
fi
cp "$pd_vm_file"_backup "$pd_vm_file"

"$insert_dylib_file" "$para_load" "$pd_vm_file"_backup "$pd_vm_file"
codesign -f -s - --timestamp=none --all-architectures --entitlements "./tool/ParallelsDesktop/VM.entitlements" "$pd_vm_file"

# patch console
pd_console_file="$pd_dir/Contents/MacOS/prl_client_app"

if [ ! -f "$pd_console_file"_backup ]; then
    cp "$pd_console_file" "$pd_console_file"_backup
fi
cp "$pd_console_file"_backup "$pd_console_file"

"$insert_dylib_file" "$para_load" "$pd_console_file"_backup "$pd_console_file"
codesign -f -s - --timestamp=none --all-architectures --entitlements "./tool/ParallelsDesktop/Console.entitlements" "$pd_console_file"

# install fake license
license_file_dst="/Library/Preferences/Parallels/licenses.json"

if [ -f "$license_file_dst" ]; then
  chflags -R 0 "$license_file_dst"
  rm -f "$license_file_dst" > /dev/null
fi

cp "./tool/ParallelsDesktop/licenses.json" "$license_file_dst"
chown root:wheel "$license_file_dst"
chmod 444 "$license_file_dst"
chflags -R 0 "$license_file_dst"
chflags uchg "$license_file_dst"
chflags schg "$license_file_dst"

# start prl_disp_service
if ! pgrep -x "prl_disp_service" &>/dev/null; then
  echo "${COLOR_INFO}[*] 正在启动 Parallels Service ..."
  "$pd_dir/Contents/MacOS/Parallels Service" service_restart &>/dev/null
  for (( i=0; i < 10; ++i ))
  do
    if pgrep -x "prl_disp_service" &>/dev/null; then
      break
    fi
    sleep 1
  done
  if ! pgrep -x "prl_disp_service" &>/dev/null; then
    echo -e "${COLOR_ERR}[x] 启动 Service 失败."
  fi
fi

# configure parallels
"$pd_dir/Contents/MacOS/prlsrvctl" web-portal signout &>/dev/null
"$pd_dir/Contents/MacOS/prlsrvctl" set --cep off &>/dev/null
"$pd_dir/Contents/MacOS/prlsrvctl" set --allow-attach-screenshots off &>/dev/null

# 需要管理员权限启动PD才会正常访问网络
# (echo "you_pass_word" | sudo -S -b /Applications/Parallels\ Desktop.app/Contents/MacOS/prl_client_app &)