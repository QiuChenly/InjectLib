#!/bin/bash

cd "${0%/*}" || exit 1
read -p "⚙️ 请输入密码(明文)然后回车: " -r passwd
printf "\r\033[1A%s" "" 1>&2
printf "\r\033[K%s" "" 1>&2
echo "${passwd}" | sudo -S echo "⚙️ 当前是 $(sudo -S whoami) 用户"

if [[ -n "$1" ]]; then
    file="/etc/hosts"
    lines=(
        "127.0.0.1 download.parallels.com"
        "127.0.0.1 update.parallels.com"
        "127.0.0.1 desktop.parallels.com"
        "127.0.0.1 download.parallels.com.cdn.cloudflare.net"
        "127.0.0.1 update.parallels.com.cdn.cloudflare.net"
        "127.0.0.1 desktop.parallels.com.cdn.cloudflare.net"
        "127.0.0.1 www.parallels.cn"
        "127.0.0.1 www.parallels.com"
        "127.0.0.1 www.parallels.de"
        "127.0.0.1 www.parallels.es"
        "127.0.0.1 www.parallels.fr"
        "127.0.0.1 www.parallels.nl"
        "127.0.0.1 www.parallels.pt"
        "127.0.0.1 www.parallels.ru"
        "127.0.0.1 www.parallelskorea.com"
        "127.0.0.1 reportus.parallels.com"
        "127.0.0.1 parallels.cn"
        "127.0.0.1 parallels.com"
        "127.0.0.1 parallels.de"
        "127.0.0.1 parallels.es"
        "127.0.0.1 parallels.fr"
        "127.0.0.1 parallels.nl"
        "127.0.0.1 parallels.pt"
        "127.0.0.1 parallels.ru"
        "127.0.0.1 parallelskorea.com"
        "127.0.0.1 pax-manager.myparallels.com"
        "127.0.0.1 myparallels.com"
        "127.0.0.1 my.parallels.com"
        "# 127.0.0.1 download.parallels.com"
        "# 127.0.0.1 update.parallels.com"
        "# 127.0.0.1 desktop.parallels.com"
        "# 127.0.0.1 download.parallels.com.cdn.cloudflare.net"
        "# 127.0.0.1 update.parallels.com.cdn.cloudflare.net"
        "# 127.0.0.1 desktop.parallels.com.cdn.cloudflare.net"
        "# 127.0.0.1 www.parallels.com"
        "# 127.0.0.1 reportus.parallels.com"
        "# 127.0.0.1 parallels.com"
        "# 127.0.0.1 my.parallels.com"
    )
    if [[ "$1" == "add" ]]; then
        if [[ "$(sudo -S awk 'END {print}' "${file}")" != "" ]]; then
            sudo -S tee -a "${file}" >/dev/null <<-EOF

EOF
        fi
        # 循环检查和添加行
        for line in "${lines[@]}"; do
            if ! sudo -S grep -q "^${line}" "${file}"; then
                sudo -S tee -a "${file}" >/dev/null <<-EOF
${line}
EOF
            fi
        done
        echo "⚙️ 已屏蔽 Parallels Desktop."
        exit 0
    elif [[ "$1" == "del" ]]; then
        # 循环检查和删除行
        for line in "${lines[@]}"; do
            if sudo -S grep -q "^${line}" "${file}"; then
                sudo -S sed -i "" "/^${line}/d" "${file}"
            fi
        done
        echo "⚙️ 已取消屏蔽 Parallels Desktop."
        exit 0
    else
        echo "⚙️ 参数错误: add / del"
    fi
fi

PDFM_DIR="/Applications/Parallels Desktop.app"
PDFM_DISP_DST="${PDFM_DIR}/Contents/MacOS/Parallels Service.app/Contents/MacOS/prl_disp_service"
PDFM_DISP_PATCH="${PDFM_DISP_DST}_patched"
PDFM_DISP_BCUP="${PDFM_DISP_DST}_backup"

if [ "$(pgrep -x prl_disp_service)" != "" ] && [ "$(pgrep -x prl_client_app)" != "" ]; then
    open "${PDFM_DIR}"
    exit 0
fi

if [ ! -e "${PDFM_DISP_PATCH}" ]; then
    sudo -S cp -f "${PDFM_DISP_DST}" "${PDFM_DISP_PATCH}"
fi

sudo -S cp -f "${PDFM_DISP_PATCH}" "${PDFM_DISP_DST}"
open "${PDFM_DIR}"

sleep 2

sudo -S cp -f "${PDFM_DISP_BCUP}" "${PDFM_DISP_DST}"
