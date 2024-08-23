import os, datetime, shutil

def extract(base):
    os.system(f"cd {base} && asar extract obsidian.asar obsidian")

def pack(base):
    os.system(f"cd {base} && asar pack obsidian obsidian.asar")

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"「{now}」 {msg}")

def is_obsidian_running():
    if os.system("pgrep -x Obsidian > /dev/null 2>&1") == 0:
        log("检测到 Obsidian 进程正在运行，请先关闭 Obsidian 进程")
        # os.system("killall -9 Obsidian")
        exit(0)

def crack_app(base):
    destination_path = f"{base}/obsidian"

    app_js_file_path = os.path.join(destination_path, "app.js")

    with open(app_js_file_path, "r", encoding="utf-8") as file:
        old_content = """var iY=new(function(){function e(){this.keyValidation="",this.company="",this.expiry=0,this.seats=0;try{var e=JSON.parse(localStorage.getItem(zK));this.email=e.email,this.name=e.name,this.token=e.token,this.license=e.license,this.key=e.key}catch(e){}}return e.prototype.save=function(){var e={email:this.email,name:this.name,token:this.token,license:this.license,key:this.key};localStorage.setItem(zK,JSON.stringify(e))},e.prototype.setKey=function(e){this.key=e,this.save()},e}());"""
        new_content = """
        var iY = new ((function () {
            function e() {
                (this.keyValidation = "valid"),
                (this.company = "QiuChenlyTeam"),
                (this.expiry = 8640000000000),
                (this.seats = Infinity);
                (this.email = "QiuChenlyTeam@Cracked.com"),
                (this.name = "Cracked by QiuChenlyTeam"),
                (this.token = "e.token"),
                (this.license = "vip"),
                (this.key = "Cracked by QiuChenlyTeam");
            }
            return (
                (e.prototype.save = function () {
                (this.keyValidation = "valid"),
                (this.company = "QiuChenlyTeam"),
                (this.expiry = 8640000000000),
                (this.seats = Infinity);
                (this.email = "QiuChenlyTeam@Cracked.com"),
                (this.name = "Cracked by QiuChenlyTeam"),
                (this.token = "e.token"),
                (this.license = "vip"),
                (this.key = "Cracked by QiuChenlyTeam");
                var e = {
                  email: this.email,
                  name: this.name,
                  token: this.token,
                  license: this.license,
                  key: this.key,
                };
                localStorage.setItem(zK, JSON.stringify(e));
              }), (e.prototype.setKey = function (e) { (this.key = e), this.save(); }), e
            );
        })())();"""
        app_content = file.read()
        if old_content in app_content:
            log("激活信息写入中...")
            new_app_content = app_content.replace(old_content, new_content)

            with open(app_js_file_path, "w", encoding="utf-8") as file2:
                file2.write(new_app_content)
                log("激活信息写入完毕")
        else:
            log("Obsidian文件已被修改过，请重新下载")

def crack_asar(base):
    if not os.path.exists(f"{base}/obsidian_backup.asar"):
        log("备份 obsidian.asar -> obsidian_backup.asar")
        shutil.copyfile(f"{base}/obsidian.asar", f"{base}/obsidian_backup.asar")

    log("解包 obsidian.asar")
    extract(base)
    crack_app(base)

    log("打包 obsidian.asar")
    pack(base)
    log("删除 obsidian 文件夹")
    shutil.rmtree(f"{base}/obsidian")

    log("正在修复已损坏")
    os.system("sudo xattr -cr /Applications/Obsidian.app")
    log("修复完毕")

def crack(base):
    log("正在进行 Obsidian 破解操作...")

    if os.system("command -v asar > /dev/null 2>&1") == 1:
        log("未检测到asar，请先安装asar")
        exit(0)

    # 如果存在obsidian_backup，证明已经用脚本处理过，那就用obsidian_backup重新破解，免得有傻逼瞎几把搞
    if os.path.exists(rf"{base}/obsidian_backup.asar"):
        log("obsidian_backup.asar 已存在，将使用 obsidian_backup 重新激活")
        os.remove(f"{base}/obsidian.asar")
        shutil.copyfile(f"{base}/obsidian_backup.asar", f"{base}/obsidian.asar")
        os.remove(f"{base}/obsidian_backup.asar")

    if os.path.exists(rf"{base}/obsidian.asar"):
        crack_asar(base)

    log("Obsidian 破解处理完毕")

def main():
    try:
        print("  ___  _        ____ _                _      _____")
        print(" / _ \\(_)_   _ / ___| |__   ___ _ __ | |_   |_   _|__  __ _ _ __ ___")
        print("| | | | | | | | |   | '_ \\ / _ \\ '_ \\| | | | || |/ _ \\/ _` | '_ ` _ \\")
        print("| |_| | | |_| | |___| | | |  __/ | | | | |_| || |  __/ (_| | | | | | |")
        print(" \\__\\_\\_|\\__,_|\\____|_| |_|\\___|_| |_|_|\\__, ||_|\\___|\\__,_|_| |_| |_|")
        print("                                        |___/")
        print("\nQiuChenlyTeam Obsidian「Mac」一键破解脚本 By X1a0He\n")

        is_obsidian_running()

        # 你他妈的，要修改文件都是要权限的，不用 sudo ，你修改nm呢？
        if not os.geteuid() == 0:
            log("请以「sudo」运行此脚本")
            exit(0)

        if not os.path.exists("/Applications/Obsidian.app"):
            log("未检测到 Obsidian.app，结束执行")
            exit(0)

        base = "/Applications/Obsidian.app/Contents/Resources"
        crack(base)
        os.system("open -a Obsidian")

    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == '__main__':
    main()