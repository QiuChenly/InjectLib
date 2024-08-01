#!/bin/bash

# 定义文件路径
ASAR_FILE="/Applications/Obsidian.app/Contents/Resources/obsidian.asar"
EXTRACT_DIR="obsidian_extracted"
APP_JS_PATH="$EXTRACT_DIR/app.js"
TEMP_JS_PATH="$EXTRACT_DIR/app_temp.js"

# 检查是否安装了 asar 工具
if ! command -v asar &> /dev/null; then
  echo "asar 工具未安装。请按照以下步骤安装 asar："
  echo "1. 确保已安装 Node.js"
  echo "2. 运行命令：npm install -g asar"
  exit 1
fi

# 解包 ASAR 文件
asar extract "$ASAR_FILE" "$EXTRACT_DIR"

# 检查解包是否成功
if [ ! -f "$APP_JS_PATH" ]; then
  echo "解包失败，未找到 app.js 文件"
  exit 1
fi

# 修改 app.js 文件
sed 's/var iY=new(function(){function e(){this.keyValidation="",this.company="",this.expiry=0,this.seats=0;try{var e=JSON.parse(localStorage.getItem(zK));this.email=e.email,this.name=e.name,this.token=e.token,this.license=e.license,this.key=e.key}catch(e){}}return e.prototype.save=function(){var e={email:this.email,name:this.name,token:this.token,license:this.license,key:this.key};localStorage.setItem(zK,JSON.stringify(e))},e.prototype.setKey=function(e){this.key=e,this.save()},e}());/var iY=new(function(){function e(){this.keyValidation="valid",this.company="QiuChenly",this.expiry= Date.now()+120,this.seats=99999; this.email = "QiuChenly@outlook.com", this.name = "QiuChenly", this.token = "e.token", this.license = "vip", this.key = "NMSL";}return e.prototype.save=function(){this.keyValidation="valid",this.company="QiuChenly",this.expiry= Date.now()+120,this.seats=99999; this.email = "QiuChenly@outlook.com", this.name = "QiuChenly", this.token = "e.token", this.license = "vip", this.key = "NMSL";var e={email:this.email,name:this.name,token:this.token,license:this.license,key:this.key};localStorage.setItem(zK,JSON.stringify(e))},e.prototype.setKey=function(e){this.key=e,this.save()},e}());/' "$APP_JS_PATH" > "$TEMP_JS_PATH"

# 替换原始 app.js 文件
mv "$TEMP_JS_PATH" "$APP_JS_PATH"

# 重新打包 ASAR 文件
asar pack "$EXTRACT_DIR" "$ASAR_FILE"

# 清理解包目录
rm -rf "$EXTRACT_DIR"

echo "obsidian操作完成"
