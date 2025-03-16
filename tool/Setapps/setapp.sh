cp /Applications/Setapp.app/Contents/Library/LaunchServices/Setapp.app/Contents/MacOS/SetappAgent /Applications/Setapp.app/Contents/Library/LaunchServices/Setapp.app/Contents/MacOS/SetappAgent_backup
tool/insert_dylib /Applications/Setapp.app/Contents/Frameworks/CoreInject.dylib /Applications/Setapp.app/Contents/Library/LaunchServices/Setapp.app/Contents/MacOS/SetappAgent_backup /Applications/Setapp.app/Contents/Library/LaunchServices/Setapp.app/Contents/MacOS/SetappAgent
codesign -fs - /Applications/Setapp.app/Contents/Library/LaunchServices/Setapp.app
