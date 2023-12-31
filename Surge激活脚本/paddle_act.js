let url = $request.url;

let paddleActivate = () => {
  if (url !== "https://v3.paddleapi.com/3.2/license/activate") return;
  let body = $request.body.split("&");
  let product_id = "";
  for (let k of body) {
    if (k.indexOf("product_id") != -1) {
      product_id = k.split("=")[1];
    }
  }

  $done({
    response: {
      body: JSON.stringify({
        success: true,
        response: {
          product_id: product_id,
          activation_id: "QiuChenly",
          type: "personal",
          expires: 1,
          expiry_date: 1999999999999,
        },
      }),
    },
  });
};

let paddleVerify = () => {
  if (url !== "https://v3.paddleapi.com/3.2/license/verify") return;
  let body = JSON.stringify({
    success: true,
    response: {
      type: "personal",
      expires: 1,
      expiry_date: 1999999999999,
    },
  });
  $done({
    response: {
      body,
    },
  });
};

let elpassManagement = () => {
  if (url !== "https://api.elpass.app/device/management") return;
  let body = JSON.stringify({
    email: "QiuChenly@52pojie.com",
    subscriptionBillingPeriod: null,
    subscriptionEndDate: 99999502400,
    subscriptionSource: null,
    autoRenew: true,
    trial: false,
  });
  $done({
    response: {
      body,
    },
  });
};

let elpassInit = () => {
  if (url !== "https://api.elpass.app/device/init") return;
  let body = JSON.stringify({
    code: 0,
    subscriptionBillingPeriod: null,
    subscriptionEndDate: 99999502400, //5100年授权
    subscriptionSource: null,
    autoRenew: true,
    trial: false,
  });
  $done({
    response: {
      body,
    },
  });
};

let elpassActiveWithKey = () => {
  if (url !== "https://api.elpass.app/device/activate-with-key") return;
  let body = JSON.stringify({
    code: 0,
    license: "没有密钥 这个注入伪造信息是没有用的",
  });
  $done({
    response: {
      body,
    },
  });
};

paddleActivate();
paddleVerify();

//这里可以用通用有效授权信息伪造下发即可伪造出真实激活状态
elpassManagement();
elpassInit();
elpassActiveWithKey();

let MacUpdater = () => {
  if (
    url.indexOf(
      "execute-api.eu-central-1.amazonaws.com/default/meddle-activate"
    ) === -1 &&
    url.indexOf(
      "execute-api.eu-central-1.amazonaws.com/default/meddle-deactivate"
    ) === -1 &&
    url.indexOf(
      "execute-api.eu-central-1.amazonaws.com/default/meddle-authenticate"
    ) === -1
  )
    return;
  let body = "success";
  $done({
    response: {
      body,
    },
  });
};

MacUpdater();
