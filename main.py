import json
import os
import plistlib
import subprocess
import shutil
from pathlib import Path
import time


def read_input(prompt):
    return input(prompt).strip().lower()

def search_apps(app_list, install_apps, keyword):
    keyword = keyword.lower()
    installed_apps = {app['CFBundleIdentifier']: app['CFBundleName'].lower() for app in install_apps}
    def is_match(pn):
        return keyword in (pn.lower() if isinstance(pn, str) else any(keyword in p.lower() for p in pn))
    matched_apps = []
    for app in app_list:
        pn_list = app.get("packageName")
        if isinstance(pn_list, list):
            matched = [pn for pn in pn_list if is_match(pn) and any(pid == pn and keyword in name for pid, name in installed_apps.items())]
            matched_apps.extend({**app, "packageName": pn} for pn in matched)
        elif pn_list and is_match(pn_list):
            matched_apps.append({**app, "packageName": pn_list})
    return matched_apps

def parse_app_info(app_base_locate, app_info_file):
    with open(app_info_file, "rb") as f:
        app_info = plistlib.load(f)
    app_info = {
        "appBaseLocate": app_base_locate,
        "CFBundleIdentifier": app_info.get("CFBundleIdentifier"),
        "CFBundleVersion": app_info.get("CFBundleVersion", ""),
        "CFBundleShortVersionString": app_info.get("CFBundleShortVersionString", ""),
        "CFBundleName": app_info.get("CFBundleExecutable", ""),
        "CFBundleExecutable": app_info.get("CFBundleExecutable", ""),
    }
    return app_info


def scan_apps():
    appList = []
    base_dirs = ["/Applications", "/Applications/Setapp"]

    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
        lst = os.listdir(base_dir)
        for app in lst:
            app_info_file = os.path.join(base_dir, app, "Contents", "Info.plist")
            if not os.path.exists(app_info_file):
                continue
            try:
                appList.append(parse_app_info(base_dir + "/" + app, app_info_file))
                # print("检查本地App:", app_info_file)
            except Exception:
                continue

    return appList


def check_compatible(compatible_version_code, compatible_version_subcode, app_version_code, app_subversion_code):
    if compatible_version_code is None and compatible_version_subcode is None:
        return True

    if compatible_version_code:
        for code in compatible_version_code:
            if app_version_code == code:
                return True

    if compatible_version_subcode:
        for code in compatible_version_subcode:
            if app_subversion_code == code:
                return True

    return False

def handle_keygen(bundleIdentifier):
    # 取出用户名
    username = os.path.expanduser("~").split("/")[-1]
    subprocess.run("chmod +x ./tool/KeygenStarter", shell=True)
    subprocess.run(f"./tool/KeygenStarter '{bundleIdentifier}' '{username}'", shell=True)

def handle_helper(app_base, target_helper, component_apps, SMExtra, bridge_path, useOptool,helperNoInject):
    """增强Helper

    Args:
        app_base (dict): app信息
        target_helper (string): helper文件路径
    """
    subprocess.run("chmod +x ./tool/GenShineImpactStarter", shell=True)
    subprocess.run(f"./tool/GenShineImpactStarter '{target_helper}' {'' if SMExtra is None else SMExtra}", shell=True)
    if useOptool:
        sh = f"./tool/optool install -p '{bridge_path}91QiuChenly.dylib' -t '{target_helper}'"
    else:
        sh = f"./tool/insert_dylib '{bridge_path}91QiuChenly.dylib' '{target_helper}' '{target_helper}'"
    
    if helperNoInject:
        pass
    else:
        subprocess.run(sh, shell=True)
    helper_name = target_helper.split("/")[-1]

    # 检查是否存在
    target = f"/Library/LaunchDaemons/{helper_name}.plist"
    if os.path.exists(target):
        subprocess.run(f"sudo /bin/launchctl unload {target}", shell=True)
        subprocess.run(f"sudo /usr/bin/killall -u root -9 {helper_name}", shell=True)
        subprocess.run(f"sudo /bin/rm {target}", shell=True)
        subprocess.run(f"sudo /bin/rm /Library/PrivilegedHelperTools/{helper_name}", shell=True)
    subprocess.run(f"sudo xattr -c '{app_base}'", shell=True)

    src_info = [f"{app_base}/Contents/Info.plist"]
    if isinstance(component_apps, list):
        src_info.extend([f"{app_base}{i}/Contents/Info.plist" for i in component_apps])

    for i in src_info:
        command = ["/usr/libexec/PlistBuddy", "-c", f"Set :SMPrivilegedExecutables:{helper_name} 'identifier \\\"{helper_name}\\\"'", i]
        subprocess.run(command, text=True)
    subprocess.run(f'/usr/bin/codesign -f -s - --all-architectures --deep "{target_helper}"', shell=True)
    subprocess.run(f'/usr/bin/codesign -f -s - --all-architectures --deep "{app_base}"', shell=True)


def getAppMainExecutable(app_base):
    # 读取Contents/Info.plist中的CFBundleExecutable
    with open(f"{app_base}/Contents/Info.plist", "rb") as f:
        app_info = plistlib.load(f)
        return app_info["CFBundleExecutable"]


# 获取BundleID
def getBundleID(app_base):
    with open(f"{app_base}/Contents/Info.plist", "rb") as f:
        app_info = plistlib.load(f)
        return app_info["CFBundleIdentifier"]


def main():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)

        base_public_config = config["basePublicConfig"]
        app_list = config["AppList"]
        proc_version = config["Version"]

        print()
        print("  ██████╗ ██╗██╗   ██╗ ██████╗██╗  ██╗███████╗███╗   ██╗██╗  ██╗   ██╗ ")
        print(" ██╔═══██╗██║██║   ██║██╔════╝██║  ██║██╔════╝████╗  ██║██║  ╚██╗ ██╔╝ ")
        print(" ██║   ██║██║██║   ██║██║     ███████║█████╗  ██╔██╗ ██║██║   ╚████╔╝  ")
        print(" ██║▄▄ ██║██║██║   ██║██║     ██╔══██║██╔══╝  ██║╚██╗██║██║    ╚██╔╝   ")
        print(" ╚██████╔╝██║╚██████╔╝╚██████╗██║  ██║███████╗██║ ╚████║███████╗██║    ")
        print("  ╚══▀▀═╝ ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝    ")
        print()
        print("Original Design By QiuChenly(github.com/qiuchenly), Py ver. by X1a0He")
        print(f"自动注入版本号: {proc_version}")
        print("注入时请根据提示输入'y' 或者按下回车键跳过这一项。")

        # QiuChenlyTeam 特殊变量
        isDevHome = False #os.getenv("InjectLibDev")

#         start_time = time.time()
        install_apps = scan_apps()
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         print("扫描本地App耗时: {:.2f}s".format(elapsed_time))
        app_Lst = []
        keyword = input("请输入应用名称或包名的关键字进行搜索,或直接按回车键遍历所有支持的应用: ").strip()

        if keyword:
            matched_apps = search_apps(app_list, install_apps, keyword)
            if not matched_apps:
                print("未找到匹配的应用程序。")
            else:
                app_Lst = []
                selected = set()
                while len(selected) < len(matched_apps):
                    print("找到以下匹配的应用程序:")
                    for i, app in enumerate(matched_apps, 1):
                        status = " ✅[已选中]" if i-1 in selected else ""
                        print(f"{i}. {app.get('packageName')}{status}")
                    if len(selected) == len(matched_apps):
                        print("所有应用已选中，即将开始处理...")
                        break
                    choice = input("请输入要注入的应用程序编号，输入0退出，或按回车继续: ").strip()
                    if choice == '0':
                        print("已退出程序。")
                        exit(0)
                    elif choice.isdigit() and 0 < int(choice) <= len(matched_apps):
                        index = int(choice) - 1
                        if index not in selected:
                            app_Lst.append(matched_apps[index])
                            selected.add(index)
                            if len(selected) == len(matched_apps): print("所有应用已选中，即将开始处理...")
                        else: print(f"应用 {matched_apps[index].get('packageName')} 已经被选择，请选择其他应用。")
                    elif choice == '':
                        if not app_Lst: print("未选择任何应用，请至少选择一个应用。")
                        else: break
                    else: print("无效的输入，请重新选择。")
        else:
            app_Lst = [app.copy() | {"packageName": name} for app in app_list
               if not (app.get("forQiuChenly") and not os.path.exists("/Users/qiuchenly"))
               for name in (app["packageName"] if isinstance(app["packageName"], list) else [app["packageName"]])]

        for app in app_Lst:
            package_name = app.get("packageName")
            app_base_locate = app.get("appBaseLocate")
            bridge_file = app.get("bridgeFile")
            inject_file = app.get("injectFile")
            support_version = app.get("supportVersion")
            support_subversion = app.get("supportSubVersion")
            extra_shell = app.get("extraShell")
            need_copy_to_app_dir = app.get("needCopyToAppDir")
            deep_sign_app = app.get("deepSignApp")
            disable_library_validate = app.get("disableLibraryValidate")
            entitlements = app.get("entitlements")
            no_sign_target = app.get("noSignTarget")
            no_deep = app.get("noDeep")
            tccutil = app.get("tccutil")
            auto_handle_setapp = app.get("autoHandleSetapp")
            auto_handle_helper = app.get("autoHandleHelper")
            helper_file = app.get("helperFile")
            componentApp = app.get("componentApp")
            onlysh = app.get("onlysh")
            SMExtra = app.get("SMExtra")
            keygen = app.get("keygen")
            useOptool = app.get("useOptool")
            helperNoInject = app.get("helperNoInject") 
            # forceSignMainExecute
            forceSignMainExecute = app.get("forceSignMainExecute")
            dylibSelect = app.get("dylibSelect") # 选择注入的库
            
            if dylibSelect is None:
                dylibSelect = "91QiuChenly.dylib"

            local_app = [
                local_app
                for local_app in install_apps
                if local_app["CFBundleIdentifier"] == package_name
            ]

            if not local_app and (
                app_base_locate is None or not os.path.isdir(app_base_locate)
            ):
                continue

            if not local_app:
                # print("[🔔] 此App包不是常见类型结构，请注意当前App注入的路径是 {appBaseLocate}".format(appBaseLocate=app_base_locate))
                # print("读取的是 {appBaseLocate}/Contents/Info.plist".format(appBaseLocate=app_base_locate))
                local_app.append(
                    parse_app_info(
                        app_base_locate,
                        os.path.join(app_base_locate, "Contents", "Info.plist"),
                    )
                )

            local_app = local_app[0]
            if app_base_locate is None:
                app_base_locate = local_app["appBaseLocate"]

            if bridge_file is None:
                bridge_file = base_public_config.get("bridgeFile", bridge_file)

            if auto_handle_setapp is not None:
                bridge_file = "/Contents/MacOS/"
                executableAppName = local_app["CFBundleExecutable"]
                inject_file = os.path.basename(app_base_locate + bridge_file + executableAppName)
                print(f"======== Setapp下一个App的处理结果如下 [{app_base_locate}] [{bridge_file}] [{inject_file}]")

            if not check_compatible(support_version, support_subversion, local_app["CFBundleShortVersionString"], local_app["CFBundleVersion"],):
                print(f"[😅] [{local_app['CFBundleName']}] - [{local_app['CFBundleShortVersionString']}] - [{local_app['CFBundleIdentifier']}]不是受支持的版本，跳过注入😋。")
                continue

            print(f"[🤔] [{local_app['CFBundleName']}] - [{local_app['CFBundleShortVersionString']}] 是受支持的版本，是否需要注入？y/n(默认n)")
            action = read_input("").strip().lower()
            if action != "y":
                continue

            if onlysh:
                subprocess.run(f"sudo sh tool/{extra_shell}", shell=True)
                continue

            # 检查是否为com.adobe开头
#             if local_app["CFBundleIdentifier"].startswith("com.adobe"):
#                 subprocess.run(
#                     "sudo chmod -R 777 /Applications/Utilities/Adobe Creative Cloud/Components/Apps/*",
#                     shell=True,
#                 )
#                 # 检查是否存在/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js
#                 if not os.path.exists(
#                     "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js"
#                 ):
#                     # 替换文件中的key:"getEntitlementStatus",value:function(e){为key:"getEntitlementStatus",value:function(e){return "Entitled Installed"
#                     with open(
#                         "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js",
#                         "r",
#                         encoding="utf-8",
#                     ) as f:
#                         content = f.read()
#                     # 判断是否写过了
#                     if (
#                         'key:"getEntitlementStatus",value:function(e){return "Entitled Installed"'
#                         not in content
#                     ):
#                         # sed -i "s#key:\"getEntitlementStatus\",value:function(e){#key:\"getEntitlementStatus\",value:function(e){return \"Entitled Installed\"#g" /Applications/Utilities/Adobe\ Creative\ Cloud/Components/Apps/Apps1_0.js
#                         content = content.replace(
#                             'key:"getEntitlementStatus",value:function(e){',
#                             'key:"getEntitlementStatus",value:function(e){return "Entitled Installed";',
#                         )
#                         with open(
#                             "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js",
#                             "w",
#                             encoding="utf-8",
#                         ) as f:
#                             f.write(content)

            print(f"开始注入App: {package_name}")

            subprocess.run(["sudo", "chmod", "-R", "777", app_base_locate])
            subprocess.run(["sudo", "xattr", "-cr", app_base_locate])

            subprocess.run(
                ["sudo", "pkill", "-f", getAppMainExecutable(app_base_locate)]
            )

            if keygen is not None:
                print("正在注册App...")
                handle_keygen(local_app["CFBundleIdentifier"])
                continue

            # dest = os.path.join(app_base_locate, bridge_file, inject_file)
            dest = rf"{app_base_locate}{bridge_file}{inject_file}"
            backup = rf"{dest}_backup"

            if os.path.exists(backup):
                print("备份的原始文件已经存在,需要直接用这个文件注入吗？y/n(默认y)")
                action = read_input("").strip().lower()
                if action == "n":
                    os.remove(backup)
                    subprocess.run(f"sudo cp '{dest}' '{backup}'", shell=True)
            else:
                subprocess.run(f"sudo cp '{dest}' '{backup}'", shell=True)

            current = Path(__file__).resolve()

            sh = f"chmod +x {current.parent}/tool/insert_dylib"
            sh = f"chmod +x {current.parent}/tool/optool"
            subprocess.run(sh, shell=True)

            if useOptool:
                sh = f"sudo {current.parent}/tool/optool install -p '{current.parent}/tool/{dylibSelect}' -t '{dest}'"
            else:
                sh = f"sudo {current.parent}/tool/insert_dylib '{current.parent}/tool/{dylibSelect}' '{backup}' '{dest}'"

            if need_copy_to_app_dir:
                source_dylib = f"{current.parent}/tool/{dylibSelect}"
                if isDevHome:
                    # 开发者自己的prebuild库路径 直接在.zshrc设置环境变量这里就可以读取到。
                    # export InjectLibDev="自己的路径/91QiuChenly.dylib"
                    # 要设置全路径哦 并且不要用sudo python3 main.py 启动 否则读不到你的环境变量
                    source_dylib = isDevHome
                destination_dylib = f"'{app_base_locate}{bridge_file}{dylibSelect}'"

                command = "ln -f -s" if isDevHome else "cp"
                subprocess.run(
                    f"{command} {source_dylib} {destination_dylib}",
                    shell=True,
                )

                sh = []
                desireApp = [dest]
                if componentApp:
                    desireApp.extend(
                        [
                            f"{app_base_locate}{i}/Contents/MacOS/{getAppMainExecutable(app_base_locate+i)}"
                            for i in componentApp
                        ]
                    )
                for it in desireApp:
                    if useOptool:
                        bsh = rf"sudo {current.parent}/tool/optool install -p {destination_dylib} -t '{it}'"
                    else:
                        bsh = rf"sudo {current.parent}/tool/insert_dylib {destination_dylib} '{backup}' '{it}'"
                    sh.append(bsh)

            if isinstance(sh, list):
                [subprocess.run(command, shell=True) for command in sh]
            else:
                subprocess.run(sh, shell=True)

            sign_prefix = (
                "/usr/bin/codesign -f -s - --timestamp=none --all-architectures"
            )

            if no_deep is None:
                print("Need Deep Sign.")
                sign_prefix += " --deep"

            if entitlements is not None:
                sign_prefix += f" --entitlements {current.parent}/tool/{entitlements}"

            if no_sign_target is None:
                print("开始签名...")
                subprocess.run(f"{sign_prefix} '{dest}'", shell=True)

            if disable_library_validate is not None:
                subprocess.run(
                    "sudo defaults write /Library/Preferences/com.apple.security.libraryvalidation.plist DisableLibraryValidation -bool true",
                    shell=True,
                )

            if extra_shell is not None:
                subprocess.run(
                    f"sudo sh {current.parent}/tool/{extra_shell}", shell=True
                )

            if deep_sign_app:
                subprocess.run(f"{sign_prefix} '{app_base_locate}'", shell=True)

            if forceSignMainExecute:
                subprocess.run(f"cp '{dest}' /tmp/test && codesign -fs - /tmp/test && cp /tmp/test '{dest}'", shell=True)

            subprocess.run(f"sudo xattr -cr '{dest}'", shell=True)
            if auto_handle_helper and helper_file:
                helpers = []

                if isinstance(helper_file, list):
                    helpers = helper_file
                else:
                    helpers.append(helper_file)

                for helper in helpers:
                    handle_helper(
                        app_base_locate,
                        f"{app_base_locate}{helper}",
                        componentApp,
                        SMExtra,
                        f"{app_base_locate}{bridge_file}",
                        useOptool,
                        helperNoInject
                    )
            if tccutil is not None:
                if tccutil := tccutil:
                    # 如果componentApp不为空，则创建一个数组
                    ids = [local_app["CFBundleIdentifier"]]
                    if isinstance(componentApp, list):
                        ids.extend(
                            [getBundleID(app_base_locate + i) for i in componentApp]
                        )

                    for id in ids:
                        if isinstance(tccutil, str):
                            subprocess.run(f"tccutil reset {tccutil} {id}", shell=True)
                        else:
                            if isinstance(tccutil, list):
                                for i in tccutil:
                                    subprocess.run(
                                        f"tccutil reset {i} {id}", shell=True
                                    )

            print("App处理完成。")
    except KeyboardInterrupt:
        print("\n用户手动退出程序,祝你使用愉快,再见.")


if __name__ == "__main__":
    main()