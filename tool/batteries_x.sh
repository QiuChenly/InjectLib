
sudo /usr/bin/killall -u root -9 io.fadel.Batteries-setapp.Helper

helper='/Applications/Setapp/Batteries.app/Contents/Library/LoginItems/io.fadel.Batteries-setapp.Helper.app/Contents/MacOS/io.fadel.Batteries-setapp.Helper'

xattr -cr '/Applications/Setapp/Batteries.app'

/usr/bin/codesign -f -s - --all-architectures --deep /Applications/Setapp/Batteries.app/Contents/Library/LoginItems/io.fadel.Batteries-setapp.Helper.app/Contents/MacOS/io.fadel.Batteries-setapp.Helper

/usr/bin/codesign -f -s - --all-architectures --deep /Applications/Setapp/Batteries.app