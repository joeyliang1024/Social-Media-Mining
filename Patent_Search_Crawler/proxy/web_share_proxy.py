import requests
import random
import config


class ProxyPoolFromWebShare:
    def __init__(self, start_index=0):
        self.PROXY_POOL_URL = config.PROXY_POOL_URL
        self.proxies = ProxyPoolFromWebShare.fetch_proxy(self.PROXY_POOL_URL)
        self.index = start_index

    def get_proxy(self):
        key = list(self.proxies.keys())
        return self.proxies.get(key[self.index])

    def delete_proxy(self, ip):
        self.index += 1 
        self.index %= len(self.proxies)

    @staticmethod
    def fetch_proxy(proxy_pool_url):
        req = requests.get(proxy_pool_url).text
        proxies = {}
        for line in req.split("\n"):
            if line:
                ip, port, username, password = line.split(":")
                proxies.update(
                    {
                        ip: {
                            "ip": ip,
                            "port": port,
                            "username": username,
                            "password": password,
                        }
                    }
                )
        return proxies


if __name__ == "__main__":
    proxy_pool = ProxyPoolFromWebShare()
    from pprint import pprint

    px = proxy_pool.get_proxy()
    pprint(px)
    proxy_pool.delete_proxy(px["ip"])
    pprint(proxy_pool.proxies)
