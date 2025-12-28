# horus_client.py
"""
基础设施层 - 数据)
职责：只负责与 Horus 数据源的底层 API 通信。


来源参考： (Original horus_client3.py)
"""


import requests
from loguru import logger
from config import Config

class HorusClient:
    def __init__(self):
        if not Config.HORUS_API_KEY:
            raise ValueError("HORUS_API_KEY not set")
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": Config.HORUS_API_KEY,
            "Content-Type": "application/json"
        })

    def _request(self, endpoint, params=None):
        url = Config.HORUS_BASE_URL + endpoint
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            return data
        except Exception as e:
            logger.error(f"Horus API error: {e}")
            raise

    def get_market_price(self, asset="BTC", interval="1h", limit=None):
        params = {"asset": asset, "interval": interval, "format": "json"}
        if limit: params["limit"] = limit
        return self._request("/market/price", params)

    def get_latest_price(self, asset="BTC"):
        try:
            data = self.get_market_price(asset=asset, interval="1d")
            if isinstance(data, list) and len(data) > 0:
                return data[-1]["price"]
            return self._mock_price(asset)
        except Exception:
            return self._mock_price(asset)

    def _mock_price(self, asset):
        return {"BTC": 68000, "ETH": 3500}.get(asset, 100)