cp tool/idalic.hexlic /Users/qiuchenly/.idapro/idalic.hexlic
cp "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida64" /tmp/ida
codesign -fs - /tmp/ida
cp /tmp/ida "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida64"