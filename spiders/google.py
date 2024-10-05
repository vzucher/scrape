import os
import time
from imports import *
from selenium.common.exceptions import StaleElementReferenceException

# from insta import set_opts

query = {
  'target': 'instagram.com',
  'tag': 'tattoo',
  'mail': 'gmail.com',
  'mail2': 'hotmail.com',
  'page': ''
  
}

google = f"https://google.com/search?q=site%3A{query['target']}+{query['tag']}+%22%40{query['mail']}'%22+OR+%22%40{query['mail2']}%22&sca_esv=569753216&sxsrf=AM9HkKnuDy_gxzACkJpPeRfz35kLs8xCtg%3A1696103888760&ei=0H0YZYCMLoTZ5OUPiKOfKA&ved=0ahUKEwiAtKquj9OBAxWELLkGHYjRBwUQ4dUDCBE&uact=5&oq=site%3A{query['target']}+{query['tag']}+%22%40{query['mail']}%22+OR+%22%40{query['mail2']}%22&gs_lp=Egxnd3Mtd2l6LXNlcnAiOHNpdGU6aW5zdGFncmFtLmNvbSB0YXR0b28gIkBnbWFpbC5jb20iIE9SICJAaG90bWFpbC5jb20iSI0OUOoEWIUMcAJ4AJABAJgBjAGgAesIqgEDMC45uAEDyAEA-AEB4gMEGAEgQYgGAQ&sclient=gws-wiz-serp#ip=1"

def set_opts():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  # Optional: Use incognito mode which doesn't use cache
    chrome_options.add_argument("--disable-cache")  # Disable the cache
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(gen_ua(browsers, os, min_per))
    
    # proxy_, ip, port = get_random_proxy()
    
    # proxy_settings = {
    #     "proxyType": "manual",
    #     "sslProxy": f"{ip}:{port}"
    # }

    # chrome_options.add_argument(f"--proxy-server={ip}:{port}")  # Directly set the proxy in chrome_options
    
    return chrome_options

def open(google):
    chrome_options = set_opts()
    driver = webdriver.Chrome(options=chrome_options)
    print('[........opening website.....]')
    driver.get(google)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    return driver



def get_urls(driver):
    profile_urls = []
    url = driver.current_url
    response = requests.get(url)
    html_doc = response.text

    # instantiate the soup object

    soup = BeautifulSoup(html_doc, 'html.parser')
    a = soup.find_all('a')
    h3 = soup.find_all('h3')
    
    r = range(16, len(a))

    # def format_link(link):
    #     # Remove the prefix '/url?q=' from the link
    #     link = link.replace('/url?q=', '')
    #     link = link.replace('&sa=U&ved=', '')
    #     link = link.split('2ahUKE')[0]
    #     # Pattern to match user profiles or post profiles
    #     pattern = r"https:\/\/www\.instagram\.com\/([^\/]+\/(?:p\/)?[^\/]+\/?)"
    #     match = re.search(pattern, link)

    #     if match:
    #         formatted_link = match.group()
    #         return formatted_link[:70]

    #     return link
    
    def format_link(link):
    # Pattern to extract the desired URL
        pattern = r"/url\?q=(https:\/\/www\.instagram\.com\/[^\/]+\/(?:p\/)?[^\/]+\/?)(?:&sa=U&ved=|2ahUKE)?.*"
        match = re.match(pattern, link)
        
        if match:
            formatted_link = match.group(1)
            formatted_link = formatted_link.split('&sa=U&ved=')[0]
            
            return formatted_link[:70]
        else:
            return None

    
        
    for i in a[16:]:
        print(i)
        for n in r:
            
            link = a[n]['href']
            link = format_link(link)
            if link != None:
                print(f"Appending {link}")
                profile_urls.append(link)
                
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
    return driver, profile_urls

# Save the URLs to urls.csv
def save_db(urls):
    try:
        df = pd.read_csv('data/urls.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['URL'])
    
    df_new = pd.DataFrame(urls, columns=['URL'])
    df_combined = pd.concat([df, df_new], ignore_index=True).drop_duplicates()
    
    # Only keep the 'URL' column and avoid saving the index
    df_combined = df_combined[['URL']]
    df_combined.to_csv('data/urls.csv', index=False)


# def run(google):
          
#     driver = open(google)
#     driver, urls = get_urls(driver)
#     df = save_db(urls)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     driver, urls = get_urls(driver)
#     df = save_db(urls)


#     return driver


def run(google):
    driver = open(google)
    
    # Initial fetch of URLs
    _, urls = get_urls(driver)
    save_db(urls)
    
    # Number of scrolls you want to attempt
    max_scrolls = 15  # You can adjust this number based on your needs
    
    for _ in range(max_scrolls):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the page to load
        time.sleep(3)  # Adjust this sleep time if needed
        
        # Fetch URLs after scrolling
        _, new_urls = get_urls(driver)
        
        # If no new URLs are found, break out of the loop
        if not new_urls:
            break
        
        # Save the new URLs
        save_db(new_urls)
    
    return driver

run(google)