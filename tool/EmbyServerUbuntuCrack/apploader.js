var globalThis;
void 0 === globalThis && (globalThis = self),
  (function () {
    "use strict";
    globalThis.Emby = {};
    var docElem,
      appMode,
      supportsModules = "noModule" in document.createElement("script"),
      usesModules = !1;
    function loadScript(src) {
      return new Promise(function (resolve, reject) {
        var doc = document,
          script = doc.createElement("script");
        globalThis.urlCacheParam && (src += "?" + globalThis.urlCacheParam),
          usesModules && supportsModules && (script.type = "module"),
          (script.onload = resolve),
          (script.onerror = reject),
          (script.src = src),
          doc.head.appendChild(script);
      });
    }
    function catchAndResolve(err) {
      return (
        console.log("error registering service worker: " + err),
        Promise.resolve()
      );
    }
    function loadRequire() {
      return loadScript("./modules/alameda/alameda.js");
    }
    function loadApp() {
      var baseRoute,
        config = {
          urlArgs: globalThis.urlCacheParam,
          renameJsExtension: globalThis.Emby.jsExtension,
        };
      return (
        "android" !== globalThis.appMode &&
          ((baseRoute = (baseRoute = globalThis.location.href
            .split("?")[0]
            .replace("/index.html", "")).split("#")[0]).lastIndexOf("/") ===
            baseRoute.length - 1 &&
            (baseRoute = baseRoute.substring(0, baseRoute.length - 1)),
          console.log("Setting require baseUrl to " + baseRoute),
          (config.baseUrl = baseRoute)),
        require.config(config),
        loadScript("./app.js")
      );
    }
    function onPromiseLoaded() {
      !(function () {
        switch (globalThis.appMode) {
          case "ios":
          case "android":
          case "windows":
          case "winjs":
          case "tizen":
          case "webos":
          case "chromecast":
            return Promise.resolve();
        }
        return "undefined" != typeof caches && navigator.serviceWorker
          ? caches.open("embyappinfo").then(function (cache) {
              return cache
                .put(
                  "appversion",
                  new Response(globalThis.dashboardVersion || "")
                )
                .then(function () {
                  try {
                    var serviceWorkerOptions = {};
                    return (
                      usesModules &&
                        supportsModules &&
                        (serviceWorkerOptions.type = "module"),
                      navigator.serviceWorker
                        .register("serviceworker.js", serviceWorkerOptions)
                        .then(function () {
                          return navigator.serviceWorker.ready.then(
                            function () {
                              "standalone" === globalThis.appMode &&
                                (globalThis.urlCacheParam = null),
                                (Emby.serviceWorkerEnabled = !0);
                            }
                          );
                        }, catchAndResolve)
                        .then(function (reg) {
                          return reg && reg.sync
                            ? reg.sync.register("emby-sync")
                            : Promise.resolve();
                        })
                    );
                  } catch (err) {
                    console.log("Error registering serviceWorker: " + err);
                  }
                }, catchAndResolve);
            }, catchAndResolve)
          : Promise.resolve();
      })()
        .then(loadRequire, loadRequire)
        .then(loadApp, loadApp);
    }
    (globalThis.Emby.requiresClassesPolyfill = !!1),
      (docElem = document.documentElement),
      (appMode = docElem.getAttribute("data-appmode")) &&
        (globalThis.appMode = appMode),
      (docElem = docElem.getAttribute("data-appversion")) &&
        (globalThis.dashboardVersion = docElem),
      docElem
        ? (globalThis.urlCacheParam = "v=" + docElem)
        : appMode || (globalThis.urlCacheParam = "v=" + Date.now()),
      (function (onDone) {
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
                      SupporterKey: "1234",
                      IsMBSupporter: true,
                      // =======================
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
        var doc, script, src;
        globalThis.Promise && globalThis.Promise.all
          ? onDone()
          : ((script = (doc = document).createElement("script")),
            (src = "./modules/polyfills/native-promise-only.js"),
            globalThis.urlCacheParam && (src += "?" + globalThis.urlCacheParam),
            (script.onload = onDone),
            (script.src = src),
            doc.head.appendChild(script));
      })(onPromiseLoaded);
  })();
