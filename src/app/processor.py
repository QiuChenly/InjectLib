import os
import subprocess
import sys
from pathlib import Path

from src.utils.common import getAppMainExecutable, getBundleID
from src.utils.ui_helper import read_input
from src.app.scanner import check_compatible, parse_app_info
from src.inject.helper import handle_helper
from src.inject.keygen import handle_keygen
from src.utils.color import Color


# 获取工具真实路径的辅助函数
def get_tool_path(tool_name):
    """获取工具的真实路径

    Args:
        tool_name: 工具名称

    Returns:
        str: 工具的绝对路径
    """
    # 获取项目根目录
    root_dir = Path(__file__).resolve().parent.parent.parent
    tool_path = os.path.join(root_dir, "tool", tool_name)

    # 检查工具是否存在
    if not os.path.exists(tool_path):
        print(Color.red(f"[错误] 工具 {tool_name} 不存在于路径: {tool_path}"))

    return tool_path


# 执行命令并检查结果的辅助函数
def run_command(command, shell=True, check_error=True):
    """运行命令并检查结果，如果出错则显示红色警告

    Args:
        command: 要执行的命令
        shell: 是否使用shell执行
        check_error: 是否检查错误

    Returns:
        bool: 命令执行成功返回True，否则返回False
    """
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)

        # 检查命令是否执行成功
        if check_error and result.returncode != 0:
            error_msg = result.stderr.strip() or f"命令执行失败: {command}"
            if "No such file or directory" in error_msg or "command not found" in error_msg:
                print(Color.red(f"[错误] {error_msg}"))
            return False
        return True
    except Exception as e:
        if check_error:
            print(Color.red(f"[错误] 执行命令时发生异常: {e}"))
        return False


def process_app(app, base_public_config, install_apps, current_dir=None, skip_confirmation=False):
    """处理单个应用的注入逻辑"""
    # 获取项目根目录
    root_dir = Path(__file__).resolve().parent.parent.parent

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
    forceSignMainExecute = app.get("forceSignMainExecute")
    dylibSelect = app.get("dylibSelect") # 选择注入的库

    if dylibSelect is None:
        dylibSelect = "91QiuChenly.dylib"

    # 构建工具路径
    insert_dylib_path = get_tool_path("insert_dylib")
    optool_path = get_tool_path("optool")
    dylib_path = get_tool_path(dylibSelect)

    # 查找匹配的应用，同时考虑包名和路径
    local_app = []
    for app_info in install_apps:
        # 检查包名是否匹配
        if app_info["CFBundleIdentifier"] == package_name:
            # 如果配置中指定了路径，则检查路径是否匹配
            if app_base_locate:
                if app_info["appBaseLocate"] == app_base_locate:
                    local_app.append(app_info)
            else:
                # 如果配置中没有指定路径，则只匹配包名
                local_app.append(app_info)

    if not local_app and (
        app_base_locate is None or not os.path.isdir(app_base_locate)
    ):
        print(Color.red(f"[错误] 未找到应用: {package_name}"))
        return False

    if not local_app:
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
        print(Color.yellow(f"[提示] [{local_app['CFBundleName']}] - [{local_app['CFBundleShortVersionString']}] - [{local_app['CFBundleIdentifier']}]不是受支持的版本，跳过注入。"))
        return False

    # 如果是受支持的版本，直接注入，不再询问
    print(Color.green(f"[✅] [{local_app['CFBundleName']}] - [{local_app['CFBundleShortVersionString']}] 是受支持的版本，开始注入..."))

    if onlysh:
        # 获取脚本路径
        shell_path = os.path.join(root_dir, "tool", extra_shell)
        if not run_command(f"sudo sh '{shell_path}'"):
            print(Color.red(f"[错误] 执行脚本 {shell_path} 失败"))
            return False
        return True

    print(f"开始注入App: {package_name}")

    # 设置权限
    success = True
    success &= run_command(["sudo", "chmod", "-R", "777", app_base_locate], shell=False)
    success &= run_command(["sudo", "xattr", "-cr", app_base_locate], shell=False)

    # 尝试终止进程，但忽略可能的错误
    run_command(["sudo", "pkill", "-f", getAppMainExecutable(app_base_locate)], shell=False, check_error=False)

    if keygen is not None:
        print("正在注册App...")
        handle_keygen(local_app["CFBundleIdentifier"])
        return True

    dest = rf"{app_base_locate}{bridge_file}{inject_file}"
    backup = rf"{dest}_backup"

    # 如果备份文件存在则直接使用，不再询问
    if os.path.exists(backup):
        print("备份的原始文件已经存在，将直接使用该备份文件进行注入")
    else:
        if not run_command(f"sudo cp '{dest}' '{backup}'"):
            print(Color.red(f"[错误] 创建备份文件失败: {backup}"))
            return False

    isDevHome = False # os.getenv("InjectLibDev")

    # 设置工具权限
    if not run_command(f"chmod +x '{insert_dylib_path}'"):
        print(Color.red(f"[错误] 无法设置 insert_dylib 为可执行文件，请检查文件是否存在: {insert_dylib_path}"))

    if not run_command(f"chmod +x '{optool_path}'"):
        print(Color.red(f"[错误] 无法设置 optool 为可执行文件，请检查文件是否存在: {optool_path}"))

    # 选择注入方式
    if useOptool:
        command = f"sudo '{optool_path}' install -p '{dylib_path}' -t '{dest}'"
    else:
        command = f"sudo '{insert_dylib_path}' '{dylib_path}' '{backup}' '{dest}'"

    # 执行注入命令
    if not run_command(command):
        print(Color.red(f"[错误] 执行注入命令失败: {command}"))
        return False

    if need_copy_to_app_dir:
        source_dylib = dylib_path
        destination_dylib = f"'{app_base_locate}{bridge_file}{dylibSelect}'"

        command = "ln -f -s" if isDevHome else "cp"
        if not run_command(f"{command} {source_dylib} {destination_dylib}"):
            print(Color.red(f"[错误] 复制动态库失败: {source_dylib} -> {destination_dylib}"))
            return False

        # codesign
        if not run_command(f"codesign -fs - --timestamp=none --all-architectures {destination_dylib}"):
            print(Color.yellow(f"[警告] 签名动态库失败: {destination_dylib}"))

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
                bsh = rf"sudo '{optool_path}' install -p {destination_dylib} -t '{it}'"
            else:
                bsh = rf"sudo '{insert_dylib_path}' {destination_dylib} '{backup}' '{it}'"
            sh.append(bsh)

        # 执行注入命令
        for command in sh:
            if not run_command(command):
                print(Color.red(f"[错误] 执行注入命令失败: {command}"))
                success = False

    sign_prefix = (
        "/usr/bin/codesign -f -s - --timestamp=none --all-architectures"
    )

    if no_deep is None:
        print("Need Deep Sign.")
        sign_prefix += " --deep"

    if entitlements is not None:
        # 获取entitlements文件路径
        entitlements_path = os.path.join(root_dir, "tool", entitlements)
        sign_prefix += f" --entitlements '{entitlements_path}'"

    if no_sign_target is None:
        print("开始签名...")
        if not run_command(f"{sign_prefix} '{dest}'"):
            print(Color.yellow(f"[警告] 签名失败: {dest}"))

        if not run_command(f"{sign_prefix} '{app_base_locate}'"):
            print(Color.yellow(f"[警告] 签名失败: {app_base_locate}"))

    if disable_library_validate is not None:
        run_command("sudo defaults write /Library/Preferences/com.apple.security.libraryvalidation.plist DisableLibraryValidation -bool true")

    if extra_shell is not None:
        # 获取额外脚本路径
        extra_shell_path = os.path.join(root_dir, "tool", extra_shell)
        if not run_command(f"sudo sh '{extra_shell_path}'"):
            print(Color.red(f"[错误] 执行额外脚本失败: {extra_shell_path}"))

    if deep_sign_app:
        if not run_command(f"{sign_prefix} '{app_base_locate}'"):
            print(Color.yellow(f"[警告] 深度签名失败: {app_base_locate}"))

    if forceSignMainExecute:
        if not run_command(f"cp '{dest}' /tmp/test && codesign -fs - /tmp/test && cp /tmp/test '{dest}'"):
            print(Color.yellow(f"[警告] 强制签名主执行文件失败: {dest}"))

    if not run_command(f"sudo xattr -cr '{dest}'"):
        print(Color.yellow(f"[警告] 清除扩展属性失败: {dest}"))

    if auto_handle_helper and helper_file:
        helpers = []

        if isinstance(helper_file, list):
            helpers = helper_file
        else:
            helpers.append(helper_file)

        for helper in helpers:
            try:
                handle_helper(
                    app_base_locate,
                    f"{app_base_locate}{helper}",
                    componentApp,
                    SMExtra,
                    f"{app_base_locate}{bridge_file}",
                    useOptool,
                    helperNoInject,
                    dylibSelect
                )
            except Exception as e:
                print(Color.red(f"[错误] 处理Helper失败: {e}"))
                success = False

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
                    run_command(f"tccutil reset {tccutil} {id}", check_error=False)
                else:
                    if isinstance(tccutil, list):
                        for i in tccutil:
                            run_command(f"tccutil reset {i} {id}", check_error=False)

    if success:
        print(Color.green("App处理完成。"))
    else:
        print(Color.yellow("App处理完成，但存在一些警告或错误。"))

    return success