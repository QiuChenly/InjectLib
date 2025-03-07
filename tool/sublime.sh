/usr/bin/codesign -f -s - --timestamp=none --all-architectures --deep "tool/CoreInject.dylib"
sudo cp "tool/CoreInject.dylib" /usr/local/lib/qcly
cp '/Applications/Sublime Text.app/Contents/MacOS/sublime_text' '/Applications/Sublime Text.app/Contents/MacOS/sublime_text_backup'
sudo tool/insert_dylib qcly '/Applications/Sublime Text.app/Contents/MacOS/sublime_text_backup' '/Applications/Sublime Text.app/Contents/MacOS/sublime_text'
sudo xattr -cr "/Applications/Sublime Text.app"
echo "注册码:\n----- BEGIN LICENSE -----
秋城落叶@outlook.com
Unlimited User License
EA7E-8888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
88888888888888888888888888888888
------ END LICENSE ------"