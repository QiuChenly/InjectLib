BASE_PATH=$(
  pwd
)

chmod +x $BASE_PATH/insert_dylib

main='/Applications/Autodesk/AutoCAD 2024/AutoCAD 2024.app/Contents/MacOS/AutoCAD'

sudo cp "$main" "$main.bak"

# 签名主程序
sudo $BASE_PATH/insert_dylib $BASE_PATH/libInjectLib.dylib "$main.bak" "$main"

# 修改通过服务器认证文件
helper='/Library/Application Support/Autodesk/AdskLicensing/13.3.0.9688/AdskLicensingAgent/AdskLicensingAgent.app/Contents/PlugIns/libadlmint.dylib'
echo C7010: 6A 00 58 C3 |sudo xxd -r - "$helper" #intel
echo 57bdb0: 00 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64

main='/Library/Application Support/Autodesk/AdskLicensing/13.3.0.9688/AdskLicensingAgent/AdskLicensingAgent.app/Contents/MacOS/AdskLicensingAgent'

cp "$main" /tmp/AdskLicensingAgent
sudo cp "$main" "$main.bak"

/usr/bin/codesign -f -s - /tmp/AdskLicensingAgent

sudo cp /tmp/AdskLicensingAgent "$main"
rm /tmp/AdskLicensingAgent

# 复制授权文件
cp license.dat /usr/local/flexnetserver/
cp adskflex /usr/local/flexnetserver/
chmod +x /usr/local/flexnetserver/adskflex

cd /usr/local/flexnetserver/
./lmgrd -c license.dat