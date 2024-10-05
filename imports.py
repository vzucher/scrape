import re
import os 
import sys
import requests
import pandas as pd
from vars_data.proxies import *
from vars_data.useragent import *
from vars_data.posts_xpaths import *
from bs4 import BeautifulSoup
from selenium import webdriver
from processing.tagging import post_or_user
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from processing.tagging import post_or_user

