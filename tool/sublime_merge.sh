#!/bin/bash
/usr/bin/codesign -f -s - --timestamp=none --all-architectures --deep "tool/CoreInject.dylib"
sudo mkdir -p /usr/local/lib
sudo cp "tool/CoreInject.dylib" /usr/local/lib/qcly
cp '/Applications/Sublime Merge.app/Contents/MacOS/sublime_merge' '/Applications/Sublime Merge.app/Contents/MacOS/sublime_merge_backup'
sudo tool/insert_dylib qcly '/Applications/Sublime Merge.app/Contents/MacOS/sublime_merge_backup' '/Applications/Sublime Merge.app/Contents/MacOS/sublime_merge'
sudo xattr -cr "/Applications/Sublime Merge.app"

if [[ $(arch) == "arm64" ]]; then
  echo "当前是 arm64 架构"
  sudo codesign -fs - --deep /Applications/Sublime\ Merge.app
else
  echo "当前不是 arm64 架构"
fi

echo "注册码:\n-----BEGIN LICENSE-----
qiuchenly@outlook.com
Unlimited User License
E52D-73WX6E7KFW
3WSY28516XZBBBUAKIE3K62SPQ9TDRHV
TDLUO8M6ADKRAA888FEXKAPAF0HJE60W
92AVK103WAW1294SMQI9QJBEL4OT646C
DT5KM9OO0JWVCAKZV2SKTVQ395W9CM74
CY24F9VXU6AHJ2ZD41UW6MXEBBGBMVJT
MDWWA666OTZL1UHLULMPLYKIKRK7CLFJ
VASMFT7HHGHZK2LLO09R2ECMV9SEEWMK
E64V59PRUXKBKZBA9404KXIXDJRK4TOC
-----END LICENSE-----"