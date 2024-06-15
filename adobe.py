import os
import subprocess


subprocess.run(
    "sudo chmod -R 777 '/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js'",
    shell=True,
)
# 检查是否存在/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js
if os.path.isfile(
    "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js"
):
    # 替换文件中的key:"getEntitlementStatus",value:function(e){为key:"getEntitlementStatus",value:function(e){return "Entitled Installed"
    with open(
        "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js",
        "r",
        encoding="utf-8",
    ) as f:
        content = f.read()
    # 判断是否写过了
    if (
        'key:"getEntitlementStatus",value:function(e){return "Entitled Installed"'
        not in content
    ):
        # sed -i "s#key:\"getEntitlementStatus\",value:function(e){#key:\"getEntitlementStatus\",value:function(e){return \"Entitled Installed\"#g" /Applications/Utilities/Adobe\ Creative\ Cloud/Components/Apps/Apps1_0.js
        content = content.replace(
            'key:"getEntitlementStatus",value:function(e){',
            'key:"getEntitlementStatus",value:function(e){return "Entitled Installed";',
        )
        with open(
            "/Applications/Utilities/Adobe Creative Cloud/Components/Apps/Apps1_0.js",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(content)
