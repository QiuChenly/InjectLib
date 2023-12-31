#!/usr/bin/env bash

BASE_PATH=$(
  cd $(dirname "$0")
  pwd
)

COLOR_INFO='\033[0;34m'
COLOR_ERR='\033[0;35m'
NOCOLOR='\033[0m'

PDFM_DIR="/Applications/Parallels Desktop.app"
PDFM_VER="19.1.0-54729"

PDFM_DISP_DIR="${PDFM_DIR}/Contents/MacOS/Parallels Service.app/Contents/MacOS"
PDFM_DISP_DST="${PDFM_DISP_DIR}/prl_disp_service"

LICENSE_FILE="${BASE_PATH}/licenses.json"
LICENSE_DST="/Library/Preferences/Parallels/licenses.json"

echo "${COLOR_INFO}[*] 确保你的版本是: https://download.parallels.com/desktop/v19/${PDFM_VER}/ParallelsDesktop-${PDFM_VER}.dmg"

# check parallels desktop version
VERSION_1=$(defaults read "${PDFM_DIR}/Contents/Info.plist" CFBundleShortVersionString)
VERSION_2=$(defaults read "${PDFM_DIR}/Contents/Info.plist" CFBundleVersion)
INSTALL_VER="${VERSION_1}-${VERSION_2}"
# if [ "${PDFM_VER}" != "${VERSION_1}-${VERSION_2}" ]; then
#   echo -e "${COLOR_ERR}[-] This script is for ${PDFM_VER}, but your's is ${INSTALL_VER}.${NOCOLOR}"
#   exit 2
# fi

echo "${COLOR_INFO}[*] 复制伪造的授权文件 licenses.json${NOCOLOR}"

# stop prl_disp_service
if pgrep -x "prl_disp_service" &> /dev/null; then
  echo -e "${COLOR_INFO}[*] Stopping Parallels Desktop${NOCOLOR}"
  pkill -9 prl_client_app &>/dev/null
  # ensure prl_disp_service has stopped
  "${PDFM_DIR}/Contents/MacOS/Parallels Service" service_stop &>/dev/null
  sleep 1
  launchctl stop /Library/LaunchDaemons/com.parallels.desktop.launchdaemon.plist &>/dev/null
  sleep 1
  pkill -9 prl_disp_service &>/dev/null
  sleep 1
  rm -f "/var/run/prl_*"
fi

if [ -f "${LICENSE_DST}" ]; then
  chflags -R 0 "${LICENSE_DST}" || {
    echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
    exit $?
  }
  rm -f "${LICENSE_DST}" >/dev/null || {
    echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
    exit $?
  }
fi

cp -f "${LICENSE_FILE}" "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}
chown root:wheel "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}
chmod 444 "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}
chflags -R 0 "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}
chflags uchg "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}
chflags schg "${LICENSE_DST}" || {
  echo -e "${COLOR_ERR}error $? at line $LINENO.${NOCOLOR}"
  exit $?
}

chmod 755 "${PDFM_DISP_DST}"

cp -f "/Applications/Parallels Desktop.app/Contents/MacOS/Parallels Service.app/Contents/MacOS/prl_disp_service" "/Applications/Parallels Desktop.app/Contents/MacOS/Parallels Service.app/Contents/MacOS/prl_disp_service_patched"

echo "${COLOR_INFO}[*] 破解完成。${NOCOLOR}"