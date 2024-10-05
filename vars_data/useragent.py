import random
from fake_useragent import UserAgent


browsers = ["random", "chrome", "edge", "google", "google chrome", "firefox", "ff", "safari"]

os = ["windows", "macos", "linux"]

min_per = [0.5, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.5]

def gen_ua(browsers, os, min_per):
#     b = random.choice(browsers)
    os = random.choice(os)
    min_per = random.choice(min_per)
    ua = UserAgent(browsers=browsers, os=os, min_percentage=min_per)
    ua = ua.random
    ua = 'user-agent='+ua
    return ua


ua_list = []

for i in range(0,1000):
    ua = gen_ua(browsers, os, min_per)
    ua_list.append(ua)
    
print(gen_ua(browsers, os, min_per))