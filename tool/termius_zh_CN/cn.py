import os
import re
from os import path

choice = input("您是否使用 Termius Beta 版本？直接回车默认为n (y/n): ").strip().lower()

if choice == "y":
    baseApp = "/Applications/Termius Beta.app"
else:
    baseApp = "/Applications/Termius.app"

print(f"已选择的应用路径：{baseApp}")


def decompressAsar():
    cmd = f"asar extract '{baseApp}/Contents/Resources/app.asar' '{baseApp}/Contents/Resources/app'"
    os.system(cmd)


def pack2asar():
    cmd = f"asar p '{baseApp}/Contents/Resources/app' '{baseApp}/Contents/Resources/app.asar'"
    cmd += ' --unpack-dir "{node_modules/@termius,out}"'
    os.system(cmd)
    os.system(f"xattr -cr '{baseApp}'")


files_cache: dict[str:str] = {}


def main():
    if not os.path.exists(
        f"{baseApp}/Contents/Resources/app.asar_副本"
    ):
        os.system(
            f"cp '{baseApp}/Contents/Resources/app.asar' '{baseApp}/Contents/Resources/app.asar_副本'"
        )
    else:
        os.system(
            f"cp '{baseApp}/Contents/Resources/app.asar_副本' '{baseApp}/Contents/Resources/app.asar'"
        )

    os.system(f"rm -rf '{baseApp}/Contents/Resources/app'")
    # 防止自动更新
    os.system(
        f"rm -rf '{baseApp}/Contents/Resources/app-update.yml'"
    )

    if not path.exists(f"{baseApp}/Contents/Resources/app"):
        decompressAsar()

    with open("lang.txt") as lang:
        cnLang = [ll for ll in lang.read().splitlines() if len(ll) > 0]

    prefixLink = [
        f"{baseApp}/Contents/Resources/app/background-process/assets",
        f"{baseApp}/Contents/Resources/app/ui-process/assets",
        f"{baseApp}/Contents/Resources/app/main-process",
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
    os.system(f"xattr -cr '{baseApp}'")
    print("Done.")


# os.system("sudo xattr -cr '{baseApp}'")
# os.system("sudo codesign -f -s - '{baseApp}'")
os.system("npm i -g @electron/asar")

main()
