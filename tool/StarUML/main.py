import os

# 检查是否安装了 asar 命令
def check_asar_command():
    return os.system("command -v asar > /dev/null 2>&1") == 0

if not check_asar_command():
    print("草泥马，先安装asar。")
    exit(1)

# 获取用户输入的用户名
username = input("请输入用户名: ")
# 执行bash命令
bash_extract = """
cd /Applications/StarUML.app/Contents/Resources  && asar extract app.asar app
"""
os.system(bash_extract)

# 复制license-manager.js文件到目标位置
destination_path = "/Applications/StarUML.app/Contents/Resources/app/src/engine/"
os.system("cp -f license-manager.js {}".format(destination_path))


# 将字符串中的"BilZzard"替换为用户输入的文本
with open(destination_path + "license-manager.js", 'r') as file:
    js_content = file.read()
new_js_content = js_content.replace('QiuChenlyTeam', username)

# 将替换后的内容写回到js文件
with open(destination_path + "license-manager.js", 'w') as file:
    file.write(new_js_content)

# 执行bash命令
print("需要修复app,看到提示后输入root密码。")

bash_pack = """
cd /Applications/StarUML.app/Contents/Resources &&
asar pack app app.asar &&
rm -rf app && sudo xattr -r -d com.apple.quarantine /Applications/StarUML.app
"""
os.system(bash_pack)

print("脚本执行完成。请打开后从设置-隐私与安全中打开!之后随便输入激活码即可激活！")
