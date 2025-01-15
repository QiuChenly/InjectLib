cp tool/CoreInject.dylib '/Applications/IDA Professional 9.0.app/Contents/MacOS/91QiuChenly.dylib'
cp "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida" /tmp/ida
codesign -fs - /tmp/ida
cp /tmp/ida "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida"