#!/bin/bash
/usr/bin/codesign -f -s - --timestamp=none --all-architectures --deep "tool/CoreInject.dylib"
sudo mkdir -p /usr/local/lib
sudo cp "tool/CoreInject.dylib" '/Applications/DockLock Lite.app/Contents/MacOS/qcly'
cp '/Applications/DockLock Lite.app/Contents/MacOS/DockLock Lite' '/Applications/DockLock Lite.app/Contents/MacOS/DockLock Lite_backup'
sudo tool/insert_dylib @executable_path/qcly '/Applications/DockLock Lite.app/Contents/MacOS/DockLock Lite_backup' '/Applications/DockLock Lite.app/Contents/MacOS/DockLock Lite'
sudo xattr -cr "/Applications/DockLock Lite.app"
tccutil reset All pro.docklock.lite

if [[ $(arch) == "arm64" ]]; then
  echo "当前是 arm64 架构"
  sudo codesign -fs - --deep "/Applications/DockLock Lite.app"
else
  echo "当前不是 arm64 架构"
fi