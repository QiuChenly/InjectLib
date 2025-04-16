import os
import sys
from src.utils.ui_helper import read_input, ensure_black_background, format_app_info, print_app_table_header, print_app_info, wait_for_enter, BLACK_BG, WHITE_FG
from src.utils.color import Color, truncate_text, get_visible_length
from src.utils.i18n import I18n, _

# 使用ui_helper中的函数替代重复代码
def search_apps(app_list, install_apps, keyword):
    """根据关键字搜索应用"""
    # 将关键字转为小写以便不区分大小写地搜索
    keyword = keyword.lower()
    
    # 构建已安装应用的字典，包含包名和应用名称（参考原始实现）
    installed_apps = {}
    for app in install_apps:
        # 确保CFBundleName存在
        app_name = app.get('CFBundleName', '')
        if not app_name:
            app_name = app.get('CFBundleExecutable', '')
        installed_apps[app['CFBundleIdentifier']] = {
            'name': app_name.lower(),
            'app_info': app
        }
    
    # 辅助函数：判断文本是否匹配关键字
    def is_match(text):
        if not text:
            return False
            
        if isinstance(text, str):
            # 检查文本是否包含关键字
            return keyword in text.lower()
        elif isinstance(text, list):
            # 如果是列表，检查任何元素是否匹配
            return any(keyword in item.lower() for item in text if isinstance(item, str))
        return False
    
    matched_apps = []
    
    # 遍历配置中的所有应用
    for app in app_list:
        pn_list = app.get("packageName")
        
        # 如果包名是列表，处理每个包名
        if isinstance(pn_list, list):
            matched = []
            for pn in pn_list:
                # 检查是否在已安装应用中
                if pn in installed_apps:
                    # 获取已安装的应用信息
                    installed_app_data = installed_apps[pn]
                    installed_app = installed_app_data['app_info']
                    app_name = installed_app_data['name']
                    
                    # 参考原始实现的匹配逻辑：检查包名或者应用名匹配关键字
                    if is_match(pn) or is_match(app_name):
                        matched.append({
                            **app, 
                            "packageName": pn,
                            "displayName": installed_app["CFBundleName"],
                            "version": installed_app["CFBundleShortVersionString"],
                            "buildVersion": installed_app["CFBundleVersion"],
                            "appPath": installed_app["appBaseLocate"]
                        })
            matched_apps.extend(matched)
        # 如果包名是单个字符串
        elif pn_list and pn_list in installed_apps:
            installed_app_data = installed_apps[pn_list]
            installed_app = installed_app_data['app_info']
            app_name = installed_app_data['name']
            
            # 检查包名或者应用名匹配关键字
            if is_match(pn_list) or is_match(app_name):
                matched_apps.append({
                    **app, 
                    "packageName": pn_list,
                    "displayName": installed_app["CFBundleName"],
                    "version": installed_app["CFBundleShortVersionString"],
                    "buildVersion": installed_app["CFBundleVersion"],
                    "appPath": installed_app["appBaseLocate"]
                })
    
    return matched_apps


def get_installed_apps_info(app_list, install_apps):
    """获取所有已安装且受支持的应用信息"""
    installed_supported_apps = []
    
    # 检查所有app是否在本地已安装，提前展开列表
    all_config_apps = []
    for app in app_list:
        if app.get("forQiuChenly") and not os.path.exists("/Users/qiuchenly"):
            continue
            
        pn_list = app.get("packageName")
        if isinstance(pn_list, list):
            for pn in pn_list:
                all_config_apps.append({**app, "packageName": pn})
        else:
            all_config_apps.append(app)
    
    # 检查是否已安装
    installed_app_ids = {app["CFBundleIdentifier"] for app in install_apps}
    
    # 匹配已安装的应用
    for app in all_config_apps:
        package_name = app.get("packageName")
        if package_name in installed_app_ids:
            # 找到对应的安装应用信息
            for installed_app in install_apps:
                if installed_app["CFBundleIdentifier"] == package_name:
                    # 合并信息
                    app_info = {
                        **app,
                        "displayName": installed_app["CFBundleName"],
                        "version": installed_app["CFBundleShortVersionString"],
                        "buildVersion": installed_app["CFBundleVersion"],
                        "appPath": installed_app["appBaseLocate"]
                    }
                    installed_supported_apps.append(app_info)
                    break
    
    return installed_supported_apps


def select_apps_by_keyword(app_list, install_apps):
    """通过关键字搜索选择应用"""
    keyword = input(_("enter_keyword", "请输入应用名称或包名的关键字进行搜索: ")).strip()
    
    if not keyword:
        print(_("no_keyword", "未输入关键字，返回主菜单..."))
        return []
    
    matched_apps = search_apps(app_list, install_apps, keyword)
    
    if not matched_apps:
        print(_("no_matching_apps", "未找到匹配的应用程序。"))
        return []
    
    # 显示匹配的应用并允许选择
    app_Lst = []
    selected = set()
    
    while len(selected) < len(matched_apps):
        print("\n" + _("found_matching_apps", "找到以下匹配的应用程序:"))
        
        # 打印表头
        print_app_table_header(include_status=True)
        
        for i, app in enumerate(matched_apps, 1):
            status = "✅ " if i-1 in selected else ""
            app_with_status = {**app, "status": status}
            print_app_info(i, app_with_status, include_status=True)
        
        print(f"\n{_('selected_apps_count', '已选择 {0}/{1} 个应用').format(len(selected), len(matched_apps))}")
        print(_("return_previous", "0. 返回上一级"))
        print(_("confirm_selection", "Enter. 确认当前选择并继续"))
        
        if len(selected) == len(matched_apps):
            print(_("all_apps_selected", "所有应用已选中..."))
            break
        
        choice = input(_("enter_app_number", "请输入要选择的应用编号: ")).strip()
        
        if choice == '0':
            if not app_Lst:
                return []
            break
        elif choice.isdigit() and 0 < int(choice) <= len(matched_apps):
            index = int(choice) - 1
            if index not in selected:
                app_Lst.append(matched_apps[index])
                selected.add(index)
                if len(selected) == len(matched_apps): 
                    print(_("all_apps_selected", "所有应用已选中..."))
            else:
                print(_("app_already_selected", "应用 {0} 已经被选择，请选择其他应用。").format(matched_apps[index].get('displayName')))
        elif choice == '':
            if not app_Lst:
                print(_("no_app_selected", "未选择任何应用，请至少选择一个应用。"))
            else:
                break
        else:
            print(_("invalid_input", "无效的输入，请重新选择。"))
    
    return app_Lst


def display_supported_apps(app_list, install_apps, page=0, page_size=20):
    """分页显示已安装且支持的应用程序"""
    installed_supported_apps = get_installed_apps_info(app_list, install_apps)
    total_apps = len(installed_supported_apps)
    
    if total_apps == 0:
        print("\n" + _("no_installed_supported_apps", "未找到已安装且受支持的应用程序"))
        return [], 0, 0
    
    total_pages = (total_apps + page_size - 1) // page_size
    page = max(0, min(page, total_pages - 1))  # 确保页码有效
    
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_apps)
    
    page_info = _("installed_supported_apps_list", "已安装且支持的应用列表 (第 {0}/{1} 页, 共 {2} 个应用)").format(page+1, total_pages, total_apps)
    print(f"\n{page_info}")
    
    # 打印表头
    print_app_table_header()
    
    for i, app in enumerate(installed_supported_apps[start_idx:end_idx], start_idx+1):
        print_app_info(i, app)
    
    return installed_supported_apps[start_idx:end_idx], page, total_pages


def show_all_supported_apps(app_list, install_apps):
    """显示所有支持的应用"""
    # 获取所有配置的应用，展开列表类型的包名
    all_apps = []
    for app in app_list:
        # 跳过特定用户专用的应用
        if app.get("forQiuChenly") and not os.path.exists("/Users/qiuchenly"):
            continue
            
        pn_list = app.get("packageName")
        if isinstance(pn_list, list):
            for pn in pn_list:
                all_apps.append({**app, "packageName": pn})
        else:
            all_apps.append(app)
    
    # 尝试匹配安装信息
    installed_apps_map = {app["CFBundleIdentifier"]: app for app in install_apps}
    for app in all_apps:
        package_name = app.get("packageName")
        if package_name in installed_apps_map:
            installed_app = installed_apps_map[package_name]
            app["displayName"] = installed_app["CFBundleName"]
            app["version"] = installed_app["CFBundleShortVersionString"]
            app["buildVersion"] = installed_app["CFBundleVersion"]
            app["appPath"] = installed_app["appBaseLocate"]
            app["isInstalled"] = True
        else:
            app["displayName"] = package_name
            app["isInstalled"] = False
    
    print("\n" + _("total_supported_apps", "支持的应用总数: {0}").format(len(all_apps)))
    
    page_size = 10
    page = 0
    total_pages = (len(all_apps) + page_size - 1) // page_size
    
    selected_apps = []
    
    while True:
        start_idx = page * page_size
        end_idx = min(start_idx + page_size, len(all_apps))
        
        print("\n" + _("showing_page", "显示第 {0}/{1} 页 (应用 {2}-{3}/{4})").format(page+1, total_pages, start_idx+1, end_idx, len(all_apps)))
        
        # 打印表头
        print_app_table_header(include_status=True)
        
        for i, app in enumerate(all_apps[start_idx:end_idx], start_idx+1):
            print_app_info(i, app, include_status=True)
        
        print("\n" + _("operation_options", "操作选项:"))
        print(f"{Color.cyan('n')}. {_('next_page', '下一页')} | {Color.cyan('p')}. {_('prev_page', '上一页')} | {Color.cyan(_('number', '数字'))}. {_('select_app', '选择应用')} | {Color.cyan('0')}. {_('confirm_and_return', '确认并返回')}")
        
        choice = read_input("\n" + _("select_operation", "请选择操作: "))
        
        if choice == 'n':
            if page < total_pages - 1:
                page += 1
            else:
                print(_("last_page", "已经是最后一页"))
                wait_for_enter()
        elif choice == 'p':
            if page > 0:
                page -= 1
            else:
                print(_("first_page", "已经是第一页"))
                wait_for_enter()
        elif choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(all_apps[start_idx:end_idx]):
            idx = start_idx + int(choice) - 1
            app = all_apps[idx]
            if app.get("isInstalled", False):
                if app not in selected_apps:
                    selected_apps.append(app)
                    print(_("app_selected", "已选择应用: {0}").format(app.get('displayName')))
                else:
                    selected_apps.remove(app)
                    print(_("app_deselected", "已取消选择: {0}").format(app.get('displayName')))
            else:
                print(_("app_not_installed", "该应用未安装，无法选择：{0}").format(app.get('displayName')))
            wait_for_enter()
        else:
            print(_("invalid_choice", "无效的选择，请重新选择"))
            wait_for_enter()
    
    return selected_apps 