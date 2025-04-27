import os
import plistlib
import subprocess
from pathlib import Path


def parse_app_info(app_base_locate, app_info_file):
    """解析应用信息"""
    with open(app_info_file, "rb") as f:
        app_info = plistlib.load(f)
    app_info = {
        "appBaseLocate": app_base_locate,
        "CFBundleIdentifier": app_info.get("CFBundleIdentifier"),
        "CFBundleVersion": app_info.get("CFBundleVersion", ""),
        "CFBundleShortVersionString": app_info.get("CFBundleShortVersionString", ""),
        "CFBundleName": app_info.get("CFBundleName", app_info.get("CFBundleDisplayName", app_info.get("CFBundleExecutable", ""))),
        "CFBundleExecutable": app_info.get("CFBundleExecutable", ""),
    }
    return app_info


def find_applications():
    """查找系统中所有可能的应用安装位置"""
    # 默认位置
    base_dirs = [
        "/Applications", 
        "/Applications/Setapp",
        "/Applications/Utilities",
        os.path.expanduser("~/Applications")
    ]
    
    # 添加常见的Adobe应用目录（直接添加而不是扫描，避免耗时）
    adobe_dirs = [
        "/Applications/Adobe",
        "/Applications/Adobe Acrobat DC",
        "/Applications/Adobe Lightroom Classic",
        "/Applications/Adobe Lightroom CC",
        "/Applications/Adobe Photoshop 2025",
        "/Applications/Adobe After Effects 2025",
        "/Applications/Adobe Premiere Pro 2025",
        "/Applications/Adobe Illustrator 2025"
    ]

    autodesk_dirs = [
        "/Applications/Autodesk",
        "/Applications/Autodesk/Autodesk Desktop App",
        "/Applications/Autodesk/Autodesk Fusion 360",
        "/Applications/Autodesk/AutoCAD 2025",
        "/Applications/Autodesk/Maya 2025"
    ]

    # 添加存在的Adobe目录
    for adobe_dir in adobe_dirs:
        if os.path.exists(adobe_dir):
            base_dirs.append(adobe_dir)

    for autodesk_dirs in autodesk_dirs:
        if os.path.exists(autodesk_dirs):
            base_dirs.append(autodesk_dirs)
    
    # 去重
    return list(set(base_dirs))


def scan_apps():
    """扫描系统中安装的应用"""
    appList = []
    base_dirs = find_applications()

    # 只显示简单提示，不显示详细目录
    print("正在扫描本地应用...")

    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
            
        # 扫描直接位于base_dir下的.app文件
        try:
            lst = os.listdir(base_dir)
            for app in lst:
                if app.endswith(".app"):
                    app_path = os.path.join(base_dir, app)
                    app_info_file = os.path.join(app_path, "Contents", "Info.plist")
                    if os.path.exists(app_info_file):
                        try:
                            appList.append(parse_app_info(app_path, app_info_file))
                        except Exception:
                            continue
        except Exception:
            continue
            
        # 扫描子目录中的.app文件，但限制只扫描一级子目录以避免过深递归
        try:
            for item in os.listdir(base_dir):
                sub_dir = os.path.join(base_dir, item)
                if os.path.isdir(sub_dir) and not item.endswith(".app"):
                    try:
                        for sub_item in os.listdir(sub_dir):
                            if sub_item.endswith(".app"):
                                app_path = os.path.join(sub_dir, sub_item)
                                app_info_file = os.path.join(app_path, "Contents", "Info.plist")
                                if os.path.exists(app_info_file):
                                    try:
                                        appList.append(parse_app_info(app_path, app_info_file))
                                    except Exception:
                                        continue
                    except Exception:
                        continue
        except Exception:
            pass

    return appList


def check_compatible(compatible_version_code, compatible_version_subcode, app_version_code, app_subversion_code):
    """检查应用版本是否兼容"""
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