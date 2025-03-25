# excution/service/exchange/api/binanceapi.py

import time
import hmac
import hashlib
import logging
from ...connection.restapi import RestAPIClient  # 注意引用路徑

logger = logging.getLogger(__name__)

class BinanceAPIClient(RestAPIClient):
    """
    專門給 Binance 用的 API 客戶端。
    - 若需要簽名時，就 override _sign_request()
    - 若要 Binance 特定錯誤處理，就 override _handle_response()
    """

    def __init__(self, base_url: str, api_key: str = None, api_secret: str = None):
        super().__init__(base_url)
        self.api_key = api_key
        self.api_secret = api_secret

    def _sign_request(self, params: dict) -> dict:
        """
        Binance 簽名機制：HMAC-SHA256
        """
        if not self.api_secret:
            return params
        
        # 加timestamp
        params["timestamp"] = int(time.time() * 1000)
        # 排序後串 query string
        query_str = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
        # 產生簽名
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        params["signature"] = signature
        return params

    def _handle_response(self, response):
        """
        依 Binance 的錯誤格式做特化處理。例如：
        {
          "code": -1121,
          "msg": "Invalid symbol."
        }
        """
        try:
            response.raise_for_status()
            data = response.json()

            # 如果回傳有 'code' 且 != 200 (或 > 0 / < 0)，代表錯誤
            if isinstance(data, dict) and "code" in data and data["code"] != 200:
                # 可能 code = -1121 ...
                logger.error(f"[Binance Error] code={data['code']}, msg={data['msg']}")
                raise ValueError(f"[Binance] {data['msg']}")

            return data

        except Exception as e:
            logger.error(f"[Binance] Unexpected error: {e}")
            return None

    def request(self, method: str, endpoint: str, params: dict = None, auth: bool = False):
        """
        改寫 request() 以整合 Binance 特定 header & 簽名
        """
        # 預設 headers
        headers = {"Content-Type": "application/json"}

        # 如果要簽名 (例如需要下單, 取得私有資訊...):
        if auth and self.api_key:
            headers["X-MBX-APIKEY"] = self.api_key
            if params:
                params = self._sign_request(params)
            else:
                params = self._sign_request({})

        # 呼叫父類別 (RestAPIClient) 的 request
        return super().request(method, endpoint, params=params, headers=headers)
