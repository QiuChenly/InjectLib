# QiuChenly 计算数据差值做特征码算法
# 部分网友提供了原始版本 虽然是用的Chatgpt写给我的 但是还是略表谢意
# 提供不定长度的多个十六进制汇编代码段 自动求出差值特征码

data = """
55 48 89 E5 53 50 48 89 FB 48 8D 35 DC D6 0A 03 E8 C7 45 29 01 85 C0 0F 84 96 00 00 00 48 8D 35 D8 D6 0A 03 48 89 DF E8 B0 45 29 01 85 C0 0F 84 86 00 00 00 48 8D 35 D5 D6 0A 03 48 89 DF E8 99 45 29 01 85 C0 74 7A 48 8D 35 D1 D6 0A 03 48 89 DF E8 86 45 29 01 85 C0 74 6E 48 8D 35 D4 D6 0A 03 48 89 DF E8 73 45 29 01 85 C0 74 62 48 8D 35 D3 D6 0A 03 48 89 DF E8 60 45 29 01 85 C0 74 53 48 8D 35 DB D6 0A 03 48 89 DF E8 4D 45 29 01 85 C0 74 47 48 8D 35 D7 D6 0A 03 48 89 DF E8 3A 45 29 01 85 C0

4C 89 A5 28 FD FF FF 48 C7 45 C0 00 00 00 00 48 8B B5 ?? FD FF FF 80 BE B0 00 00 00 00 74 0F
"""

data1 = []

for i in data.split("\n"):
    if i == "":
        continue
    else:
        data1.append(i)
        if len(data1) > 1:
            res = " ".join(
                [
                    d1 if d1 == d2 else "??"
                    for d1, d2 in zip(data1[0].split(), data1[1].split())
                ]
            )
            data1 = [res]

print(data1[0])
