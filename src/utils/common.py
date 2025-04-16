import os
import plistlib

def getAppMainExecutable(app_base):
    """读取Contents/Info.plist中的CFBundleExecutable"""
    with open(f"{app_base}/Contents/Info.plist", "rb") as f:
        app_info = plistlib.load(f)
        return app_info["CFBundleExecutable"]


def getBundleID(app_base):
    """获取BundleID"""
    with open(f"{app_base}/Contents/Info.plist", "rb") as f:
        app_info = plistlib.load(f)
        return app_info["CFBundleIdentifier"]
