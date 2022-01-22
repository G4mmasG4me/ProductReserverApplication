import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from amazoncaptcha import AmazonCaptcha
from urllib.parse import urlparse

def solve_captcha(product_url):
  headers = {
        'User-Agent':  UserAgent().chrome, #'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        'Accept-Language': 'en-us, en:q=0.5'
  }
  session = requests.Session()
  webpage = session.get('https://www.amazon.co.uk/errors/validateCaptcha', headers=headers)
  soup = BeautifulSoup(webpage.content, 'html.parser')
  captcha_id = soup.find('input', {'name': 'amzn'})['value']
  captcha_image_url = soup.find('img')['src']
  captcha_solution = AmazonCaptcha.fromlink(captcha_image_url).solve()
  payload = {
    'amzn': captcha_id,
    'amzn-r': urlparse(product_url).path,
    'field-keywords': captcha_solution
  }
  webpage = session.post('https://www.amazon.co.uk/errors/validateCaptcha', headers=headers, params=payload)
  soup = BeautifulSoup(webpage.content, 'html.parser')
  print(webpage.url)



solve_captcha('https://www.amazon.co.uk/dp/B08H95Y452')
# form values
# amzn: get from form
# amzn-r: refer website / product url e.g. /dp/B08H95Y452
# field-keywords: captcha answer