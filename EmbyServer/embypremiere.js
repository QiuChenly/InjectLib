define([
  "exports",
  "./../modules/viewmanager/baseview.js",
  "./../modules/emby-elements/emby-input/emby-input.js",
  "./../modules/emby-elements/emby-button/emby-button.js",
  "./../modules/emby-elements/emby-collapse/emby-collapse.js",
  "./../modules/common/globalize.js",
  "./../modules/loading/loading.js",
  "./../modules/registrationservices/registrationservices.js",
  "./../modules/common/dialogs/confirm.js",
  "./../modules/emby-apiclient/connectionmanager.js",
], function (
  _exports,
  _baseview,
  _embyInput,
  _embyButton,
  _embyCollapse,
  _globalize,
  _loading,
  _registrationservices,
  _confirm,
  _connectionmanager
) {
  function load(page) {
    var apiClient;
    _loading.default.show(),
      (apiClient = ApiClient)
        .getJSON(apiClient.getUrl("Plugins/SecurityInfo"))
        .then(function (info) {
          info.IsMBSupporter = true;
          (page.querySelector(".txtSupporterKey").value =
            info.SupporterKey || ""),
            info.SupporterKey && !info.IsMBSupporter
              ? (page
                  .querySelector(".txtSupporterKey")
                  .classList.add("invalidEntry"),
                page.querySelector(".notSupporter").classList.remove("hide"))
              : (page
                  .querySelector(".txtSupporterKey")
                  .classList.remove("invalidEntry"),
                page.querySelector(".notSupporter").classList.add("hide")),
            info.IsMBSupporter
              ? (page
                  .querySelector(".supporterContainer")
                  .classList.add("hide"),
                (function (key) {
                  key = "key=" + key + "&serverId=" + ApiClient.serverId();
                  return new Promise((resolve) =>
                    resolve({
                      deviceStatus: 0,
                      planType: "超级会员",
                      subscriptions: [
                        {
                          autoRenew: true,
                          store: "秋城落叶",
                          feature: "all",
                          planType: "超级会员",
                          expDate: "且会员资格永远不会失效",
                        },
                      ],
                    })
                  );
                })(info.SupporterKey).then(function (statusInfo) {
                  if (statusInfo) {
                    var statusLine,
                      indicator = page.querySelector(
                        ".status-indicator .listItemIcon"
                      ),
                      extendedPlans = page.querySelector(".extended-plans");
                    switch (
                      ((extendedPlans.innerHTML = _globalize.default.translate(
                        "MessagePremiereExtendedPlans",
                        '<a is="emby-linkbutton" class="button-link" href="https://emby.media/premiere-ext.html" target="_blank">',
                        "</a>"
                      )),
                      statusInfo.deviceStatus)
                    ) {
                      case 2:
                        (statusLine = _globalize.default.translate(
                          "MessagePremiereStatusOver",
                          statusInfo.planType
                        )),
                          indicator.classList.add("expiredBackground"),
                          indicator.classList.remove("nearExpiredBackground"),
                          (indicator.innerHTML = "&#xE000;"),
                          indicator.classList.add("autortl"),
                          extendedPlans.classList.remove("hide");
                        break;
                      case 1:
                        (statusLine = _globalize.default.translate(
                          "MessagePremiereStatusClose",
                          statusInfo.planType
                        )),
                          indicator.classList.remove("expiredBackground"),
                          indicator.classList.add("nearExpiredBackground"),
                          (indicator.innerHTML = "&#xE000;"),
                          indicator.classList.add("autortl"),
                          extendedPlans.classList.remove("hide");
                        break;
                      default:
                        (statusLine = _globalize.default.translate(
                          "MessagePremiereStatusGood",
                          statusInfo.planType
                        )),
                          indicator.classList.remove("expiredBackground"),
                          indicator.classList.remove("nearExpiredBackground"),
                          (indicator.innerHTML = "&#xE5CA;"),
                          indicator.classList.remove("autortl"),
                          extendedPlans.classList.add("hide");
                    }
                    page.querySelector(".premiere-status").innerHTML =
                      statusLine;
                    var subsElement = page.querySelector(".premiere-subs");
                    statusInfo.subscriptions &&
                    0 < statusInfo.subscriptions.length
                      ? ((page.querySelector(
                          ".premiere-subs-content"
                        ).innerHTML =
                          ((subs = statusInfo.subscriptions),
                          (key = info.SupporterKey),
                          subs.map(function (item) {
                            var itemHtml = "",
                              makeLink =
                                item.autoRenew && "Stripe" === item.store,
                              tagName = makeLink ? "button" : "div";
                            return (
                              itemHtml +
                              (("button" == tagName
                                ? '<button type="button"'
                                : "<div") +
                                ' class="listItem listItem-button listItem-border' +
                                (makeLink ? " lnkSubscription" : "") +
                                '" data-feature="' +
                                item.feature +
                                '" data-key="' +
                                key +
                                '">') +
                              '<i class="listItemIcon md-icon autortl">&#xe1b2;</i>' +
                              '<div class="listItemBody two-line">' +
                              '<div class="listItemBodyText">' +
                              _globalize.default.translate(
                                "ListItemPremiereSub",
                                item.planType,
                                item.expDate,
                                item.store
                              ) +
                              "</div>" +
                              '<div class="listItemBodyText listItemBodyText-secondary">' +
                              _globalize.default.translate(
                                "Stripe" === item.store
                                  ? item.autoRenew
                                    ? "LabelClickToCancel"
                                    : "LabelAlreadyCancelled"
                                  : "LabelCancelInfo",
                                item.store
                              ) +
                              "</div>" +
                              "</div>" +
                              ("</" + tagName + ">")
                            );
                          }))),
                        (subs = page.querySelector(".lnkSubscription")) &&
                          subs.addEventListener("click", cancelSub),
                        subsElement.classList.remove("hide"))
                      : subsElement.classList.add("hide"),
                      page
                        .querySelector(".isSupporter")
                        .classList.remove("hide");
                  }
                  var subs, key;
                }))
              : (page
                  .querySelector(".supporterContainer")
                  .classList.remove("hide"),
                page.querySelector(".isSupporter").classList.add("hide")),
            _loading.default.hide();
        });
  }
  function cancelSub(e) {
    console.log("Cancel ");
    var feature = this.getAttribute("data-feature"),
      key = this.getAttribute("data-key");
    (0, _confirm.default)({
      title: _globalize.default.translate("HeaderCancelSub"),
      text: _globalize.default.translate("MessageConfirmSubCancel"),
      confirmText: _globalize.default.translate("ButtonCancelSub"),
      cancelText: _globalize.default.translate("ButtonDontCancelSub"),
      primary: "cancel",
    }).then(function () {
      console.log("after confirm"),
        fetch("http://127.0.0.1:3000/admin/service/stripe/requestSubCancel", {
          method: "POST",
          body: "key=" + key + "&feature=" + feature,
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }).then(
          function (response) {
            alertText({
              text: _globalize.default.translate("MessageSubCancelReqSent"),
              title: _globalize.default.translate("HeaderConfirmation"),
            });
          },
          function (response) {
            alertText({
              text: _globalize.default.translate(
                "MessageSubCancelError",
                "cancel@emby.media"
              ),
            });
          }
        );
    });
  }
  function retrieveSupporterKey(e) {
    _loading.default.show();
    var email = this.querySelector(".txtEmail").value,
      url =
        "http://127.0.0.1:3000/admin/service/supporter/retrievekey?email=" +
        email;
    return (
      console.log(url),
      fetch(url, { method: "POST" })
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          _loading.default.hide(),
            result.Success
              ? require(["toast"], function (toast) {
                  toast(
                    _globalize.default
                      .translate("MessageKeyEmailedTo")
                      .replace("{0}", email)
                  );
                })
              : require(["toast"], function (toast) {
                  toast(result.ErrorMessage);
                }),
            console.log(result);
        }),
      e.preventDefault(),
      !1
    );
  }
  function alertText(options) {
    require(["alert"], function (alert) {
      alert(options);
    });
  }
  function updateSupporterKey(e) {
    _loading.default.show();
    var form = this,
      key = form.querySelector(".txtSupporterKey").value;
    return (
      ApiClient.updatePluginSecurityInfo({ SupporterKey: key }).then(
        function () {
          _loading.default.hide(),
            alertText(
              key
                ? {
                    text: _globalize.default.translate("MessageKeyUpdated"),
                    title: _globalize.default.translate("HeaderConfirmation"),
                  }
                : {
                    text: _globalize.default.translate("MessageKeyRemoved"),
                    title: _globalize.default.translate("HeaderConfirmation"),
                  }
            ),
            _connectionmanager.default.resetRegistrationInfo(ApiClient),
            load(form.closest(".page"));
        },
        function () {
          _loading.default.hide(),
            _connectionmanager.default.resetRegistrationInfo(ApiClient),
            load(form.closest(".page"));
        }
      ),
      e.preventDefault(),
      !1
    );
  }
  function onSupporterLinkClick(e) {
    _registrationservices.default.showPremiereInfo(),
      e.preventDefault(),
      e.stopPropagation();
  }
  function View(view, params) {
    _baseview.default.apply(this, arguments),
      view
        .querySelector(".supporterKeyForm")
        .addEventListener("submit", updateSupporterKey),
      view
        .querySelector(".lostKeyForm")
        .addEventListener("submit", retrieveSupporterKey),
      (view.querySelector(".benefits").innerHTML = _globalize.default.translate(
        "HeaderSupporterBenefit",
        '<a is="emby-linkbutton" class="lnkPremiere button-link" href="https://emby.media/premiere" target="_blank">',
        "</a>"
      )),
      view
        .querySelector(".lnkPremiere")
        .addEventListener("click", onSupporterLinkClick);
  }
  Object.defineProperty(_exports, "__esModule", { value: !0 }),
    (_exports.default = void 0),
    require(["listViewStyle"]),
    Object.assign(View.prototype, _baseview.default.prototype),
    (View.prototype.onResume = function (options) {
      _baseview.default.prototype.onResume.apply(this, arguments),
        load(this.view);
    }),
    (_exports.default = View);
});
