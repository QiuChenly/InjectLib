const hostname = ['v3.paddleapi.com','api.elpass.app','api.gumroad.com',
  'amazonaws.com'
  // '/.*?\.execute-api.*\.amazonaws\.com/'
  ]
const url = $request.url;
const domain = url.split('/')[2];
const path = url.split(domain)[1]?.split('?')[0];

const handleRequest = () => {
  if (domain === hostname[0]) {
    // /3.2/license/
    if (path.endsWith('activate')) {
      paddleActivate();
    } else if (path.endsWith('verify')) {
      paddleVerify();
    }
  } else if (domain === hostname[1]) {
    // /device/
    if (path.endsWith('init')) {
      elpassInit();
    } else if (path.endsWith('activate-with-key')) {
      elpassActiveWithKey();
    } else if (path.endsWith('management')) {
      elpassManagement();
    }
  } else if (domain === hostname[2]) {
    // /v2/licenses/
    if (path.endsWith('verify')) {
      MediaMate();
    }
  } else if (domain.endsWith(hostname[3])) { // hostname[3].test(domain)
    // /default/
    if (['meddle-activate','meddle-authenticate','meddle-deactivate'].some(end => path.endsWith(end))) {
      MacUpdater();
    }
  }

  $done({});
}

// paddle
const paddleActivate = () => {
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

const paddleVerify = () => {
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

// elpass
const elpassInit = () => {
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

const elpassActiveWithKey = () => {
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

const elpassManagement = () => {
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
// MediaMate
const MediaMate = () => {
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

// MacUpdater
const MacUpdater = () => {
  let body = "success";
  $done({
    response: {
      body,
    },
  });
};

handleRequest();
