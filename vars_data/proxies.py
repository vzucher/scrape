import json
import random

def get_random_proxy():
    with open('proxies.json', 'r') as f:
        proxies = json.load(f)
    
#         chosen_proxy = random.choice(proxies)
#         ip = chosen_proxy['ip']
#         port = chosen_proxy['port']
#         protocol = chosen_proxy['protocols'][0]  # Assuming you want the first protocol in the list

#         return f"{protocol}://{ip}:{port}"
    proxy = random.choice(proxies)
    port = proxy['port']
    ip = proxy['ip']

    # print(f"Setting a random proxy: {proxy}")
    # print(f"Your proxy PORT is {port}")
    print(f"Your proxy is IP:{ip} and your PORT:{port}")
    
    return proxy, ip, port

# get_random_proxy()

def get_current_ip(driver):
    # Navigate to httpbin's IP check service
    driver.get("http://httpbin.org/ip")
    
    # Extract the IP address from the page content
    ip_info = driver.find_element_by_tag_name("pre").text
    ip_address = ip_info.split(":")[1].strip().replace('"', '').replace('}', '').strip()
    
    print(f"Your current IP address is {ip_address}")
    
    return ip_address
