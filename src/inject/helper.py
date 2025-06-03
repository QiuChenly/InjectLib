import os
import subprocess
from pathlib import Path
from src.utils.color import Color
from src.utils.i18n import _, I18n

# 初始化国际化支持
I18n.init()

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
            error_msg = result.stderr.strip() or _("command_failed").format(command)
            if "No such file or directory" in error_msg or "command not found" in error_msg:
                print(Color.red(f"[{_('error')}] {error_msg}"))
            return False
        return True
    except Exception as e:
        if check_error:
            print(Color.red(f"[{_('error')}] {_('exception_occurred').format(e)}"))
        return False


def handle_helper(app_base, target_helper, component_apps, SMExtra, bridge_path, useOptool, helperNoInject, dylibSelect):
    """增强Helper

    Args:
        app_base (dict): app信息
        target_helper (string): helper文件路径
    """
    # 获取项目根目录
    root_dir = Path(__file__).resolve().parent.parent.parent
    
    # 构建工具路径
    starter_path = os.path.join(root_dir, "tool", "GenShineImpactStarter")
    optool_path = os.path.join(root_dir, "tool", "optool")
    insert_dylib_path = os.path.join(root_dir, "tool", "insert_dylib")
    
    # 设置权限
    if not run_command(f"chmod +x '{starter_path}'"):
        print(Color.red(f"[{_('error')}] {_('cannot_set_executable').format(starter_path)}"))
    
    # 运行工具
    if not run_command(f"'{starter_path}' '{target_helper}' {'' if SMExtra is None else SMExtra}"):
        print(Color.red(f"[{_('error')}] {_('tool_failed')}"))
    
    # 设置注入命令
    if useOptool:
        command = f"'{optool_path}' install -p '{bridge_path}{dylibSelect}' -t '{target_helper}'"
    else:
        command = f"'{insert_dylib_path}' '{bridge_path}{dylibSelect}' '{target_helper}' '{target_helper}'"
    
    if not helperNoInject:
        if not run_command(command):
            print(Color.red(f"[{_('error')}] {_('injection_failed').format(command)}"))
    
    helper_name = target_helper.split("/")[-1]

    # 检查是否存在
    target = f"/Library/LaunchDaemons/{helper_name}.plist"
    if os.path.exists(target):
        run_command(f"sudo /bin/launchctl unload {target}")
        run_command(f"sudo /usr/bin/killall -u root -9 {helper_name}")
        run_command(f"sudo /bin/rm {target}")
        run_command(f"sudo /bin/rm /Library/PrivilegedHelperTools/{helper_name}")
    
    run_command(f"sudo xattr -c '{app_base}'")

    src_info = [f"{app_base}/Contents/Info.plist"]
    
    if isinstance(component_apps, list):
        src_info.extend([f"{app_base}{i}/Contents/Info.plist" for i in component_apps])

    for i in src_info:
        command = ["/usr/libexec/PlistBuddy", "-c", f"Set :SMPrivilegedExecutables:{helper_name} 'identifier \\\"{helper_name}\\\"'", i]
        run_command(command, shell=False)
    
    run_command(f'/usr/bin/codesign -f -s - --all-architectures --deep "{target_helper}"')
    run_command(f'/usr/bin/codesign -f -s - --all-architectures --deep "{app_base}"') 