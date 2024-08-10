cp tool/idalic.hexlic "/Applications/IDA Professional 9.0.app/Contents/MacOS/idalic.hexlic"
cp "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida64" /tmp/ida
codesign -fs - /tmp/ida
cp /tmp/ida "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida64"

# 还没处理好 先删除吧
mv "/Applications/IDA Professional 9.0.app/Contents/MacOS/plugins/arm_mac_user64.dylib" "/Applications/IDA Professional 9.0.app/Contents/MacOS/arm_mac_user64.backup"