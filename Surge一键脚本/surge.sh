#!/bin/bash

# 错误处理函数
handle_error() {
  echo ""
  echo "⚠️ 脚本发生错误!,请检查错误,正在后退出..."
  exit 1
}

# 定义信号处理函数，用于响应 Ctrl+C
function handle_ctrl_c {
  echo ""
    echo "接收到 Ctrl+C，正在退出..."
    exit 0
}

# 设置信号处理程序，捕捉 SIGINT 信号（Ctrl+C）
trap handle_ctrl_c SIGINT

# 设置错误处理函数
trap handle_error ERR

function Wipes_Data {
  user=$(whoami)

  sudo rm -rf "/Applications/Surge.app" || true
  sudo rm -rf "/tmp/Surge-*.zip" || true
  sudo rm -rf "/Users/${user}/Library/Logs/Surge/" || true
  sudo rm -rf "/Users/${user}/Library/Preferences/com.nssurge.surge-mac.plist" || true
  sudo rm -rf "/Users/${user}/Library/Application Support/com.nssurge.surge-mac" || true
  sudo rm -rf "/Users/${user}/Library/HTTPStorages/com.nssurge.surge-mac" || true

  sudo /bin/launchctl unload /Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist || true
  sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper || true
  sudo /bin/rm "/Library/LaunchDaemons/com.nssurge.surge-mac.helper.plist" || true
  sudo /bin/rm "/Library/PrivilegedHelperTools/com.nssurge.surge-mac.helper" || true
  sudo rm -rf "/Users/${user}/Library/Preferences/com.nssurge.surge-mac.plist" || true
  sudo rm -rf "/Users/${user}/Library/Application\ Support/com.nssurge.surge-mac" || true
}

# 检查是否为root用户，非root用户可能无法访问某些文件
if [[ $EUID -ne 0 ]]; then
  echo '⚠️ 请使用root权限运行此脚本!'
  echo '⚠️ 若你担心安全问题,请审阅本脚本!'
  exit 1
fi

# 获取脚本文件的绝对路径和目录
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
cd "${SCRIPT_DIR}" || exit 1

echo "⚙️ 是否需要清除Surge相关内容?"
echo "⚙️ 若需要全新安装Surge,请输入y并回车,只进行破解,直接回车即可."
read -r flag
if [[ $flag == y ]]; then
  echo "⚙️ 若你安装过Surge,请确保Surge卸载干净,建议用App Cleaner & Uninstaller工具"
  echo '⚙️ 若你有配置文件等信息,请备份到其他目录,都确认无误后输入y,开始纯净安装!'
  read -r flag
  if [[ $flag != y ]]; then
    exit 1
  fi
  Wipes_Data > /dev/null 2>&1
  download_link=$(grep '| Surge 5    '  < "../readme.md" | grep 'https://dl.nssurge.com' | awk -F '[()]' '{print $2}')
  download_link_bak="https://github.com/LanYunDev/InjectLib_bak/releases/download/surge/Surge-5.4.4-2548-d7d99d568f03d3a87a049d3b6148bee6.zip"
  if [[ ! "${download_link}" ]]; then
    download_link="${download_link_bak}"
  fi
  version=$(echo "${download_link}" | awk -F '-' '{print $2 "-" $3}')

  read -r -t 5 -p "⚙️ 是否(y/n)已安装 Surge-${version} ? 5秒后自动安装." flag || true
  echo ""
  if [[ $flag != n ]]; then
    if ! curl -k -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" -o "/tmp/Surge-${version}.zip" "${download_link}"; then
      echo "❌ 下载失败,尝试采用仓库链接🔗"
      download_link="${download_link_bak}"
      version=$(echo "${download_link}" | awk -F '-' '{print $2 "-" $3}')
      curl -k -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" -o "/tmp/Surge-${version}.zip" "${download_link}" || (echo "Surge-${version}安装失败☹️,网络原因,请检查网络." && exit 1)
    fi
    unzip -qq -o "/tmp/Surge-${version}.zip" -d "/Applications" || (echo "解压失败☹️,压缩包可能已损坏.请重新下载." && exit 1)
  fi
fi

if [[ ! -e "../tool/insert_dylib" ]]; then
  echo "⚠️ 确保上级tool目录中存在insert_dylib" && exit 1
fi
if [[ ! -e "../tool/libInjectLib.dylib" ]]; then
  echo "⚠️ 确保上级tool目录中存在libInjectLib.dylib" && exit 1
fi

chmod +x "../tool/insert_dylib"
sudo cp -f "../tool/libInjectLib.dylib" "/Applications/Surge.app/Contents/Frameworks/libInjectLib.dylib" || exit 1
sudo cp -f "/Applications/Surge.app/Contents/Frameworks/Bugsnag.framework/Versions/A/Bugsnag" "/Applications/Surge.app/Contents/Frameworks/Bugsnag.framework/Versions/A/Bugsnag_backup" || exit 1
sudo ../tool/insert_dylib "/Applications/Surge.app/Contents/Frameworks/libInjectLib.dylib" "/Applications/Surge.app/Contents/Frameworks/Bugsnag.framework/Versions/A/Bugsnag_backup" "/Applications/Surge.app/Contents/Frameworks/Bugsnag.framework/Versions/A/Bugsnag" || exit 1

cd "${SCRIPT_DIR}/.." || exit 1
sudo bash ./tool/surgeAgent.sh

# sudo codesign -f -s - --all-architectures --deep /Applications/Surge.app/Contents/Library/LaunchServices/com.nssurge.surge-mac.helper || true
# sudo codesign -f -s - --all-architectures --deep /Applications/Surge.app || true

echo "✅ 完成"
open /Applications/Surge.app



