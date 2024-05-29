import os
import re
from os import path


def decompressAsar():
    cmd = "asar extract /Applications/Termius\\ Beta.app/Contents/Resources/app.asar /Applications/Termius\\ Beta.app/Contents/Resources/app"
    os.system(cmd)


def pack2asar():
    cmd = 'asar p /Applications/Termius\\ Beta.app/Contents/Resources/app /Applications/Termius\\ Beta.app/Contents/Resources/app.asar --unpack-dir "{node_modules/@termius,out}"'
    os.system(cmd)
    os.system("xattr -cr /Applications/Termius\\ Beta.app")


files_cache: dict[str:str] = {}


def main():
    if not os.path.exists(
        "/Applications/Termius\\ Beta.app/Contents/Resources/app.asar_副本"
    ):
        os.system(
            "cp /Applications/Termius\\ Beta.app/Contents/Resources/app.asar /Applications/Termius\\ Beta.app/Contents/Resources/app.asar_副本"
        )
    else:
        os.system(
            "cp /Applications/Termius\\ Beta.app/Contents/Resources/app.asar_副本 /Applications/Termius\\ Beta.app/Contents/Resources/app.asar"
        )

    os.system("rm -rf /Applications/Termius\\ Beta.app/Contents/Resources/app")
    # 防止自动更新
    os.system(
        "rm -rf /Applications/Termius\\ Beta.app/Contents/Resources/app-update.yml"
    )

    if not path.exists("/Applications/Termius Beta.app/Contents/Resources/app"):
        decompressAsar()

    with open("lang.txt") as lang:
        cnLang = [ll for ll in lang.read().splitlines() if len(ll) > 0]

    prefixLink = [
        "/Applications/Termius Beta.app/Contents/Resources/app/background-process/assets",
        "/Applications/Termius Beta.app/Contents/Resources/app/ui-process/assets",
        "/Applications/Termius Beta.app/Contents/Resources/app/main-process",
    ]

    lstFile = []
    for li in prefixLink:
        lstFile1 = [li + "/" + ls for ls in os.listdir(li) if ls.endswith(".js")]
        lstFile.extend(lstFile1)

    for file in lstFile:
        if path.exists(file):
            with open(file) as lang:
                files_cache[file] = lang.read()
    for cache in files_cache:
        print(f"你好像很急，我知道你很急，但是你先别急, {cache}")
        file_content = files_cache[cache]
        for lang in cnLang:
            old_value, new_value = lang.split("|")
            if old_value.startswith("regex:"):
                regex = re.compile(old_value[6:])
                file_content = regex.sub(new_value, file_content)
            else:
                file_content = file_content.replace(old_value, new_value)
        files_cache[cache] = file_content

    for fileOut in files_cache:
        with open(fileOut, "w", encoding="utf-8") as u:
            u.write(files_cache[fileOut])
    pack2asar()
    os.system("xattr -cr /Applications/Termius\ Beta.app")
    print("Done.")


# os.system("sudo xattr -cr '/Applications/Termius Beta.app'")
# os.system("sudo codesign -f -s - '/Applications/Termius Beta.app'")

main()
