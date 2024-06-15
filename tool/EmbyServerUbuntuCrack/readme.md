# 自用EmbyServer破解

## 使用
1. 修改映射目录
2. docker compose up -d

## 对应版本
emby/embyserver:4.9.0.23

## 注意事项
1. emby config自动存在于一个独立的镜像。如果需要docker compose down的时候也删掉这个配置保存内容，带上-v。
2. 如果不带-v，那么docker compose down是不会删除配置信息的，包括你的数据缓存。下次更新只需要docker compose down && docker compose up -d即可。

## 破解原理
1. 硬件解码
    找到Security类，修改一个字节: 
    ```c#
    bool Emby.Server.Implementations.Security.RegRecord::get_registered()
    return true;
    ```
2. 服务器验证
    拦截hook http页面请求。这里涉及到前端js层hook，技术理解比较深入，不建议新手研究。

## 备注

破解个毫无安全意识的app，把网上不少贵物小学生得瑟的那样，发个版本到处装大神，你装你吗呢？菜鸟。