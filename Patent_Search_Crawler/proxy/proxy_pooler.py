import requests


class ProxyPooler:
    PROXY_POOL_URL = "http://127.0.0.1:5010/"

    @staticmethod
    def get_proxy():
        req = requests.get(f"{ProxyPooler.PROXY_POOL_URL}get/").json()
        proxy = req.get("proxy")
        is_https = req.get("https")

        return (
            {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            if is_https
            else {"http": f"http://{proxy}"}
        )

    @staticmethod
    def delete_proxy(proxy):
        requests.get(f"{ProxyPooler.PROXY_POOL_URL}delete/?proxy={proxy}")
