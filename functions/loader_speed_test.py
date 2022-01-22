import requests_html
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

import time
from fake_useragent import UserAgent

url = 'https://www.amazon.com/gp/sign-in.html'

headers = {
		'User-Agent':  UserAgent().chrome, #'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
		'Accept-Language': 'en-us, en:q=0.5'
	}



chrome_options = Options()
chrome_options.add_argument("--headless")

selenium_driver = webdriver.Chrome(options=chrome_options)

start = time.time()
requests_session = requests.Session()
requests_response = requests_session.get(url, headers=headers)
print(time.time() - start)

start = time.time()
requests_html_session = requests_html.HTMLSession()
requests_html_response = requests_html_session.get(url)
requests_html_response.html.render()
print(time.time() - start)

start = time.time()
selenium_driver.get(url)
print(time.time() - start)