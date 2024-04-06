BASE_PATH=$(pwd)

chmod +x $BASE_PATH/insert_dylib

main='/Applications/Autodesk/maya2024/Maya.app/Contents/MacOS/Maya'

# 如果.bak不存在则复制
if [ ! -f "$main.bak" ]; then
  sudo cp "$main" "$main.bak"
fi
# 把.bak覆盖原文件
sudo cp "$main.bak" "$main"

inject="$BASE_PATH/91QiuChenly.dylib"
inject="/Users/qiuchenly/Library/Developer/Xcode/DerivedData/InjectLib-fyoxoytblilggjegbdnyoruvteuz/Build/Products/Debug/91QiuChenly.dylib"

# 签名主程序
sudo "$BASE_PATH/insert_dylib" "$inject" "$main.bak" "$main"
echo "$BASE_PATH/insert_dylib" "$inject" "$main.bak" "$main"

sudo /usr/bin/codesign -f -s - "$main"

# 修改通过服务器认证文件
helper='/Library/Application Support/Autodesk/AdskLicensing/13.3.1.9694/AdskLicensingAgent/AdskLicensingAgent.app/Contents/PlugIns/libadlmint.dylib'

# 如果.bak不存在则复制
if [ ! -f "$helper.bak" ]; then
  sudo cp "$helper" "$helper.bak"
fi

echo CB010: 6A 00 58 C3 |sudo xxd -r - "$helper" #intel
echo 58bdb0: 00 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64

# 准备签名主程序
main='/Library/Application Support/Autodesk/AdskLicensing/13.3.1.9694/AdskLicensingAgent/AdskLicensingAgent.app/Contents/MacOS/AdskLicensingAgent'

# 先备份主程序 如果有备份则不执行备份
if [ ! -f "$main.bak" ]; then
  sudo cp "$main" "$main.bak"
fi

sudo cp "$main.bak" "$main"
cp "$main" /tmp/AdskLicensingAgent

/usr/bin/codesign -f -s - /tmp/AdskLicensingAgent

sudo cp /tmp/AdskLicensingAgent "$main"
rm /tmp/AdskLicensingAgent

# 复制授权文件
# 检查md5是否为我修改后的文件 如果md5不一样就复制
if [ "$(md5 "$BASE_PATH/license.dat")" != "ea6ac1abbea63a20881ea810b923a33b" ]; then
  sudo cp "$BASE_PATH/license.dat" /usr/local/flexnetserver/license.dat
fi

# 复制授权文件同样检查md5
if [ "$(md5 "$BASE_PATH/adskflex")" != "d95e3fc2ac6c4f4164aa0745365692d1" ]; then
  sudo cp "$BASE_PATH/adskflex" /usr/local/flexnetserver/adskflex
  chmod +x /usr/local/flexnetserver/adskflex
  xattr -cr /usr/local/flexnetserver/adskflex
fi

cd /usr/local/flexnetserver/
./lmgrd -c license.dat