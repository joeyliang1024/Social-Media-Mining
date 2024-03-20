import requests
import random
from smm.utils.constant import PROXY_URL
def load_proxy_list(url):
    try:
        # Fetch proxy list from the URL
        response = requests.get(url)
        if response.status_code == 200:
            proxy_list = response.json()
            # Filter out entries without IP address or port specified
            proxy_list = [proxy for proxy in proxy_list if 'ip' in proxy and 'port' in proxy]
            return proxy_list
        else:
            print(f"Failed to fetch proxy list. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching proxy list: {e}")
        return None


def request_with_proxy(url, proxy_list_url):
    proxy_list = load_proxy_list(proxy_list_url)

    if proxy_list:
        while proxy_list:
            # Select a random proxy from the list
            proxy = random.choice(proxy_list)

            # Get the proxy address
            proxy_address = proxy.get('ip')
            port = proxy.get('port', None)  # Get port with default value None if not provided

            # Check if the proxy address is available
            if proxy_address:
                # Append port to proxy address if provided
                if port:
                    proxy_address = f"{proxy_address}:{port}"

                try:
                    # Configure proxy settings for requests
                    proxies = {
                        "http": f"socks4://{proxy_address}",
                        "https": f"socks4://{proxy_address}"
                    }

                    # Send GET request to the URL with proxy settings
                    response = requests.get(url, proxies=proxies)

                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        print("Request successful")
                        # Process the response content here if needed
                        return response
                    else:
                        print(f"Error: Failed to load URL (Status Code: {response.status_code})")

                except requests.RequestException as e:
                    # Handle any request exceptions
                    print(f"Error: {e}")

                # Remove the problematic proxy from the list
                proxy_list.remove(proxy)
                print("Proxy removed due to failure. Trying another proxy...")
            else:
                print("Proxy address not available. Trying another proxy...")

        print("All proxies failed. Unable to make the request.")
        return None
    else:
        print("Failed to load proxy list. Unable to make the request.")
        return None
