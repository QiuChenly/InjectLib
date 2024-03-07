# 本教程旨在破解Emby Server for macOS
## 支持版本: 4.7.14.0 
下载地址: https://github.com/MediaBrowser/Emby.Releases/releases/download/4.7.14.0/embyserver-osx-x64-4.7.14.0.zip

## 使用方法
Emby.Web.dll 替换到 /Applications/EmbyServer.app/Contents/MacOS/Emby.Web.dll

embypremiere.js 替换到 /Applications/EmbyServer.app/Contents/Resources/dashboard-ui/embypremiere/embypremiere.js

## 最后
我再说一遍：网上那些破解Emby Linux/Windows Server版本要替换四五个文件的人都是傻狗。

不就是修改个b前端js和改一下.Net资源文件的事情被你们搞这么复杂，老子一直以为这东西很难都懒得弄，没想到就他妈这么点b大点难度。一群饭桶！

## 利用全局hook来伪造激活信息

```js

2024.03.08 全平台通杀代码无需反编译 by QiuChenly
就你们这b水平还搞Emby的破解？纯纯的一群饭桶。一个个只会盲目替换修改dll资源文件，一知半解在这装破解大神，问点问题没一个人回，真他妈的纯纯的饭桶。

/Applications/EmbyServer.app/Contents/Resources/dashboard-ui/apploader.js   
function onDone():

 // 重写全局的 fetch 函数
        //powered by QiuChenly use node module hook 
        (window.fetch1 = window.fetch),
          (window.fetch = (url, options) => {
            console.log("加载的URL是:", url);
            //如果url 包含 https://mb3admin.com/admin/service/registration/validateDevice 则直接返回
            /**
           * {
            status: 200,
            headers: $response.headers,
            body: '{"cacheExpirationDays":999,"resultCode":"GOOD","message":"Device Valid"}'
        }
           */
            if (
              url ===
                "https://mb3admin.com/admin/service/registration/getStatus" ||
              url.includes(
                "https://mb3admin.com/admin/service/registration/validateDevice"
              )
            ) {
              return new Promise((resolve, reject) => {
                resolve({
                  status: 200,
                  headers: {
                    get: () => "application/json",
                  },
                  json: () => {
                    return {
                      cacheExpirationDays: 999,
                      resultCode: "GOOD",
                      message: "Device Valid",
                      // 上半部分是分开的
                      deviceStatus: 0,
                      planType: "超级会员",
                      subscriptions: [
                        {
                          autoRenew: true,
                          store: "秋城落叶",
                          feature: "all",
                          planType: "超级会员",
                          expDate: "直到2099年12月31日以后",
                        },
                      ],
                    };
                  },
                });
              });
            }

            return window.fetch1(url, options);
          });
```