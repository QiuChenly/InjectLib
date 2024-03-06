sudo /bin/launchctl unload /Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist
#sudo /usr/bin/killall -u root -9 com.nssurge.surge-mac.helper
sudo /bin/rm /Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.proxyman.NSProxy.HelperTool
helper='/Applications/Setapp/Proxyman.app/Contents/Library/LaunchServices/com.proxyman.NSProxy.HelperTool'
echo {{==intel==}}: 6A 01 58 C3 |sudo xxd -r - "$helper" #intel
echo {{==arm64==}}: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #arm64
xattr -c '/Applications/Setapp/Proxyman.app'
src_info='/Applications/Setapp/Proxyman.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.proxyman.NSProxy.HelperTool \"identifier \\\"com.proxyman.NSProxy.HelperTool\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/Setapp/Proxyman.app/Contents/Library/LaunchServices/com.proxyman.NSProxy.HelperTool