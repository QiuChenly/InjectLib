from src.utils.ui_helper import format_app_info, print_app_table_header, print_app_info, confirm_action, wait_for_enter
from src.app.processor import process_app
from src.app.search import get_installed_apps_info, search_apps
from src.utils.i18n import _, I18n

class AppManager:
    """管理应用的选择、显示和处理"""
    
    def __init__(self, config, installed_apps):
        """初始化应用管理器
        
        Args:
            config: 配置字典，包含basePublicConfig和AppList
            installed_apps: 已安装的应用列表
        """
        self.base_public_config = config.get("basePublicConfig", {})
        self.app_list = config.get("AppList", [])
        self.installed_apps = installed_apps
        self.selected_apps = []
        self.processed_count = 0
    
    def get_installed_supported_apps(self):
        """获取已安装且支持的应用列表"""
        return get_installed_apps_info(self.app_list, self.installed_apps)
    
    def search_by_keyword(self, keyword):
        """按关键字搜索应用
        
        Args:
            keyword: 搜索关键字
            
        Returns:
            list: 匹配的应用列表
        """
        return search_apps(self.app_list, self.installed_apps, keyword)
    
    def select_app_by_index(self, index):
        """通过索引选择应用
        
        Args:
            index: 应用索引
            
        Returns:
            dict: 应用信息字典，如果索引无效则返回None
        """
        all_installed_apps = self.get_installed_supported_apps()
        if 0 <= index < len(all_installed_apps):
            return all_installed_apps[index]
        return None
    
    def add_selected_app(self, app):
        """添加应用到已选择列表
        
        Args:
            app: 应用信息字典
        """
        if app not in self.selected_apps:
            self.selected_apps.append(app)
    
    def add_selected_apps(self, apps):
        """添加多个应用到已选择列表
        
        Args:
            apps: 应用列表
        """
        for app in apps:
            self.add_selected_app(app)
    
    def clear_selected_apps(self):
        """清空已选择的应用列表"""
        self.selected_apps.clear()
    
    def get_selected_count(self):
        """获取已选择的应用数量"""
        return len(self.selected_apps)
    
    def display_selected_app_info(self, app):
        """显示单个选择的应用信息
        
        Args:
            app: 应用信息字典
        """
        # 获取原始信息
        name = app.get("displayName", _("unknown", "未知"))
        package_name = app.get("packageName", _("unknown", "未知"))
        version = app.get("version", _("unknown", "未知"))
        build_version = app.get("buildVersion", _("unknown", "未知"))
        
        # 仅使用彩色，不添加宽度和填充
        from src.utils.color import Color
        name_colored = Color.green(name)
        package_colored = Color.cyan(package_name)
        version_colored = Color.yellow(version)
        build_colored = Color.yellow(build_version)
        
        print(f"\n{_('selected_app', '已选择应用')}: {name_colored} ({package_colored}) - {_('version', '版本')}: {version_colored} {_('build_version', '构建版本')}: {build_colored}")
    
    def display_selected_apps(self):
        """显示所有已选择的应用"""
        if not self.selected_apps:
            print(_("no_apps_selected", "未选择任何应用"))
            return False
        
        print(f"\n{_('ready_to_process_apps', '准备处理 {0} 个应用').format(len(self.selected_apps))}:")
        print_app_table_header()
        
        for i, app in enumerate(self.selected_apps, 1):
            print_app_info(i, app)
        
        return True
    
    def process_selected_app(self, app, skip_confirmation=False):
        """处理单个应用
        
        Args:
            app: 应用信息字典
            skip_confirmation: 是否跳过确认
            
        Returns:
            bool: 处理成功返回True，否则返回False
        """
        success = process_app(app, self.base_public_config, self.installed_apps, skip_confirmation)
        if success:
            self.processed_count += 1
        return success
    
    def process_selected_apps(self, skip_confirmation=False):
        """处理所有选择的应用
        
        Args:
            skip_confirmation: 是否跳过确认
            
        Returns:
            tuple: (成功数量, 总数量)
        """
        if not self.selected_apps:
            return 0, 0
        
        if not skip_confirmation and not confirm_action(f"\n{_('confirm_start_processing', '确认开始处理? (y/n)')}:"):
            return 0, 0
        
        success_count = 0
        for app in self.selected_apps:
            if self.process_selected_app(app, skip_confirmation=True):
                success_count += 1
        
        return success_count, len(self.selected_apps)
    
    def get_processed_count(self):
        """获取总共已成功处理的应用数量"""
        return self.processed_count
    
    def handle_app_selection(self, app_index):
        """处理应用选择操作
        
        Args:
            app_index: 应用索引
            
        Returns:
            bool: 操作成功返回True，否则返回False
        """
        # 获取所有已安装且支持的应用列表
        all_apps = self.get_installed_supported_apps()
        
        # 验证索引是否有效
        if not 0 <= app_index < len(all_apps):
            print(_("invalid_app_index", "应用索引超出范围"))
            wait_for_enter()
            return False
            
        selected_app = all_apps[app_index]
        if not selected_app:
            print(_("invalid_app_selection", "无效的应用选择"))
            wait_for_enter()
            return False
        
        self.display_selected_app_info(selected_app)
        
        # 直接处理应用，不需要确认
        print(_("start_processing_app", "开始处理应用..."))
        success = self.process_selected_app(selected_app, skip_confirmation=True)
        if success:
            print(_("app_processing_complete", "应用处理完成 (累计成功: {0})").format(self.processed_count))
        else:
            print(_("app_processing_failed", "应用处理失败"))
        wait_for_enter()
        
        return True 