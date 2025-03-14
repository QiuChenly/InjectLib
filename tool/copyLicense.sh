codesign -fs - tool/CoreInject.dylib
cp tool/CoreInject.dylib '/Applications/IDA Professional 9.1.app/Contents/MacOS/91QiuChenly.dylib'
cp "/Applications/IDA Professional 9.1.app/Contents/MacOS/ida" /tmp/ida
codesign -fs - /tmp/ida
cp /tmp/ida "/Applications/IDA Professional 9.1.app/Contents/MacOS/ida"