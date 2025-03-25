# excution/service/connection/restapi.py

import requests
import logging
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RestAPIClient:
    """
    通用的 REST API 客戶端骨架。
    如果你想在這裡做共用的錯誤處理，可以寫在 _handle_response。
    但 Binance/Bybit/OKX 各有不同錯誤碼邏輯時，
    可以選擇在子類別（binanceapi.py 等）裡覆寫 _handle_response()。
    """
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _handle_response(self, response):
        """
        預設(通用)的錯誤處理。若要針對不同交易所寫，更細的可在子類別 override。
        """
        try:
            response.raise_for_status()
            data = response.json()
            return data
        except HTTPError as http_err:
            logging.error(f"[HTTP Error] {http_err}")
        except RequestException as req_err:
            logging.error(f"[Request Error] {req_err}")
        except ValueError as val_err:
            logging.error(f"[Value Error] {val_err}")
        except Exception as err:
            logging.error(f"[Unexpected Error] {err}")
        return None

    def request(self, method: str, endpoint: str, params: dict = None, headers: dict = None, timeout: int = 10):
        """
        通用請求方法，可被子類別或外部直接呼叫
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        headers = headers or {"Content-Type": "application/json"}

        try:
            if method.upper() == "GET":
                resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            elif method.upper() == "POST":
                # 可以視交易所要求用 data= / json=
                resp = requests.post(url, json=params, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return self._handle_response(resp)

        except Timeout:
            logging.error("Request timeout")
        except ConnectionError:
            logging.error("Connection error")

        return None
