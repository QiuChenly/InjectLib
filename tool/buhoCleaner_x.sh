sudo /bin/launchctl unload /Library/LaunchDaemons/com.drbuho.BuhoCleaner.PrivilegedHelperTool.plist
sudo /bin/rm /Library/LaunchDaemons/com.drbuho.BuhoCleaner.PrivilegedHelperTool.plist
sudo /bin/rm /Library/PrivilegedHelperTools/com.drbuho.BuhoCleaner.PrivilegedHelperTool
helper='/Applications/BuhoCleaner.app/Contents/Library/LaunchServices/com.drbuho.BuhoCleaner.PrivilegedHelperTool'
echo {{==intel==}}: 6A 01 58 C3 |sudo xxd -r - "$helper" #Intel
echo {{==arm64==}}: 20 00 80 D2 C0 03 5F D6 |sudo xxd -r - "$helper" #ARM
xattr -c '/Applications/BuhoCleaner.app'
src_info='/Applications/BuhoCleaner.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c "Set :SMPrivilegedExecutables:com.drbuho.BuhoCleaner.PrivilegedHelperTool \"identifier \\\"com.drbuho.BuhoCleaner.PrivilegedHelperTool\\\"\"" "$src_info"
codesign -f -s - --all-architectures --deep /Applications/BuhoCleaner.app/Contents/Library/LaunchServices/com.drbuho.BuhoCleaner.PrivilegedHelperTool
codesign -f -s - --all-architectures --deep /Applications/BuhoCleaner.app