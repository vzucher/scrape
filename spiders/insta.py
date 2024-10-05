import sys
import os

# Calculate the directory above your script's directory
current_script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import from the parent directory as if it was in your current directory
from imports import *
# defining variables

credentials = {
  'user': 'inkerscraper',
  'password': 'inkertattoo'
}

website = "https://www.instagram.com"

# instantiating webdriver options

def set_opts():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  # Optional: Use incognito mode which doesn't use cache
    chrome_options.add_argument("--disable-cache")  # Disable the cache
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--disable-gpu")  # Optional, recommended for compatibility
    chrome_options.add_argument("window-size=1024,768")  # Optional, set window size
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

def open_driver(website):
    
    chrome_options = set_opts()
    driver = webdriver.Chrome(options=chrome_options)
    print('[........opening website.....]')
    driver.get(website)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    return driver

# calling webdriver instatiating method


def login(credentials, driver):
  
    wait = WebDriverWait(driver, 10)
    login = wait.until(EC.element_to_be_clickable((By.NAME, "username"))).click()
    login = driver.find_element(By.NAME, 'username')
    login.send_keys(credentials['user'])
    driver.implicitly_wait(10)


    password = driver.find_element(By.NAME,"password")
    password.click()
    password.send_keys(credentials['password'])

    xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button"
    btn = driver.find_element(By.XPATH, xpath)
    btn.click()
    print('[........loging in instagram website.....]')
    return driver
  

def is_driver_active(driver):
    try:
        # Attempt to get the current URL. If the driver is not active, this will raise an exception.
        current_url = driver.current_url
        print("Driver is active!")
        return True
    except WebDriverException:
        print("Driver is not active!")
        return False
  
def js_element(driver, xpath):
    
    try:
        
        e = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        is_driver_active(driver)
        return driver, e
        
    except TimeoutException:
        
        try:
            e = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            
            return driver, e
            
        except TimeoutException:
            print(f"Element not found with {xpath}")
            return driver, None
  
def handling_popup(driver):
    
    xpath = "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div"
    btn = '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]' 
    driver, btn = js_element(driver, xpath)
    # btn = driver.find_element(By.XPATH, btn)
    print(btn)
    if btn != None:
      btn.click()
      print('[........pop up handled in instagram website.....]')  
    return driver

def search_tag(driver, tag):
    print('[........checkpoint.....]')
    u = f"{website}/explore/tags/{tag}"
    driver.get(u)
    print(f"successfully visited url of tag {u}")
    
    urls = []

    for xp in posts_xpaths:
      driver, e = js_element(driver, xp)
      print(f"Successfully located post {e} on grid")
      if e != None:    
        e.click()
        url = driver.current_url
        url = url.split('?img_index=')[0]
        print(url)
      
      print(f"Element is of type {type(e)}")
      driver.back()
      urls.append(url)
      
    return driver, urls

def save_csv(urls):
    print("..........saving csv function...........")

    try:
        df = pd.read_csv('data/urls.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['URL'])
    
    df_new = pd.DataFrame(urls, columns=['URL'])
    df_combined = pd.concat([df, df_new], ignore_index=True).drop_duplicates()
    
    # Only keep the 'URL' column and avoid saving the index
    df_combined = df_combined[['URL']]
    df_combined.to_csv('data/urls.csv', index=False)
    return df_combined

def post_to_user(df, driver):
    print("...........post to user function...........")
    df = post_or_user(df)
    df.to_csv('data/urls.csv', index=False)
    df_posts = df[df['Type'] == 'POST URL']
    for url in df_posts['URL']:
        driver.get(url)
        xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div/span/span/div/a/div/div/span"
        driver, username = js_element(driver, xpath)
        if username != None:
            username.click()
            user_url = driver.current_url
            print(f"User URL: {user_url}")
        with open('data/urls.csv', 'a') as f:
            user_url = driver.current_url
            f.write(user_url + '\n')
    df = post_or_user(df)
    return df

def user_info(df, driver):
    print("...........user info function...........")

    for url in df['URL']:
        
        if url:  # Check if the URL is not None or empty
            try:
                driver.get(url)
            # ... rest of your code
            except InvalidArgumentException:
                print(f"Invalid URL: {url}")
        # driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        username = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/section/main/div/header/section/div[1]/h2'
        name = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[1]/span'
        n_posts = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span'
        n_followers = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span'
        n_follow = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span'
        bio = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1'
        link = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[3]/a/span/span'
        
        driver, username = js_element(driver, username)
        print(f"ELEMENT USERNAME {username}, {type(username)}")
        # driver, name = driver.find_element(By.XPATH, name)
        # driver, n_posts = driver.find_element(By.XPATH, n_posts)
        # print(f"Retrieved # of Posts: {n_posts}, this var is of type {type(n_posts)}")
        # driver, n_followers = driver.find_element(By.XPATH, n_followers)
        # print(f"Retrieved # of Followers: {n_followers}, this var is of type {type(n_followers)}")        
        # driver, n_follow = driver.find_element(By.XPATH, n_follow)
        # print(f"Retrieved # of Following: {n_follow}, this var is of type {type(n_follow)}")        
        # driver, bio = driver.find_element(By.XPATH, bio)
        # driver, link = driver.find_element(By.XPATH, link)
        
        with open('data/users.csv', 'a') as f:
            f.write(f"{username},{url},{name},{n_posts},{n_followers},{n_follow},{bio},{link}"+'\n')
    return driver
            

def run_all():
  driver = open_driver(website)
  login(credentials, driver)
  handling_popup(driver)
  driver, urls =  search_tag(driver, 'tattoo')
  df = save_csv(urls)
  df, driver = post_to_user(df, driver)
  driver = user_info(df, driver)
  return 

run_all()