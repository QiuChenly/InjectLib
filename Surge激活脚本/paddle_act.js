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

let MediaMate = () => {
  if (url.indexOf("https://api.gumroad.com/v2/licenses/verify") === -1) return;
  let body = JSON.stringify({
    success: true,
    uses: -999,
    purchase: {
      sellerId: "123",
      productId: "",
      productName: "",
      permalink: "https://www.baidu.com",
      productPermalink: "https://www.baidu.com",
      email: "qiuchenly@outlook.com",
      price: 100,
      gumroadFee: 0,
      currency: "usd",
      quantity: 1,
      discoverFeeCharged: false,
      canContact: false,
      referrer: "nmsl",
      orderNumber: 1234,
      saleId: "1",
      saleTimestamp: "2099-07-16T19:00:00Z",
      licenseKey: "我测你吗",
      refunded: false,
      disputed: false,
      disputeWon: false,
      id: "1234",
      createdAt: "2023-07-16T19:00:00Z",
    },
  });
  $done({
    response: {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
      body,
    },
  });
};

MediaMate();
