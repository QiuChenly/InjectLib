#!/bin/bash
/usr/bin/codesign -f -s - --timestamp=none --all-architectures --deep "tool/CoreInject.dylib"
sudo mkdir -p /usr/local/lib
sudo cp "tool/CoreInject.dylib" /usr/local/lib/qcly
cp '/Applications/Sublime Text.app/Contents/MacOS/sublime_text' '/Applications/Sublime Text.app/Contents/MacOS/sublime_text_backup'
sudo tool/insert_dylib qcly '/Applications/Sublime Text.app/Contents/MacOS/sublime_text_backup' '/Applications/Sublime Text.app/Contents/MacOS/sublime_text'
sudo xattr -cr "/Applications/Sublime Text.app"

if [[ $(arch) == "arm64" ]]; then
  echo "当前是 arm64 架构"
  sudo codesign -fs - --deep /Applications/Sublime\ Text.app
else
  echo "当前不是 arm64 架构"
fi

echo "注册码:\n----- BEGIN LICENSE -----
秋城落叶@outlook.com
Unlimited User License
EA7E-8888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
------ END LICENSE ------"