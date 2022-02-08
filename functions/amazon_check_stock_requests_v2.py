import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from amazoncaptcha import AmazonCaptcha
from urllib.parse import urlparse

def check_stock_amazon(product_url, q, position): # unique order is a list of unique ordered products with unique locations. q is the output, position is so that we which process is which.
  parsed_url = urlparse(product_url)
  captcha_url = 'https://' + str(parsed_url.netloc) + '/errors/validateCaptcha'

  headers = {
    'User-Agent':  UserAgent().chrome, #'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    'Accept-Language': 'en-us, en:q=0.5'
  }
  session = requests.Session()
  webpage = session.get(product_url, headers=headers)
  captcha_attempts = 0
  if webpage.url == product_url and webpage.status_code == 200: # if webpage is equal to target url, and webpage is connected
    soup = BeautifulSoup(webpage.content, 'html.parser')
    captcha_form = soup.find('form', {'action': '/errors/validateCaptcha'})
    while captcha_form and captcha_attempts < 5: # checks if captcha form is showing, and makes sure it doesn't exceed the captcha attempts
      captcha_attempts += 1
      captcha_id = soup.find('input', {'name': 'amzn'})['value'] # attempts to find the captcha id
      captcha_image_url = soup.find('img')['src'] # gets the source link of the captcha image
      captcha_solution = AmazonCaptcha.fromlink(captcha_image_url).solve() # solves captcha
      payload = {
        'amzn': captcha_id,
        'amzn-r': parsed_url.path,
        'field-keywords': captcha_solution
      }
      webpage = session.post(captcha_url, headers=headers, params=payload)
      soup = BeautifulSoup(webpage.content, 'html.parser')
      captcha_form = soup.find('form', {'action': '/errors/validateCaptcha'})
      
    if captcha_form == None:
      price_container = soup.find('div', {'id': 'apex_desktop'})
      if price_container:
        price_a_offscreen = price_container.find('span', {'class': 'a-offscreen'})
      else:
        price_a_offscreen = None
      priceblock_ourprice = soup.find('span', {'id': 'priceblock_ourprice'})
      buy_options = soup.find('span', {'id': 'buybox-see-all-buying-choices'})
      if price_a_offscreen or priceblock_ourprice:
        q.put([position, False]) # In Stock
      elif buy_options:
        print('Other Options')
      else:
        q.put([position, True]) # Out of Stock
        
    else:
      q.put([position, str('Captcha Fail')])
  else:
    q.put([position, 'Error: ' +  webpage.url + ' - ' + webpage.status_code])


links = ['https://www.amazon.co.uk/dp/B009DL2TBA', 'https://www.amazon.co.uk/dp/B07HBW5HVL', 'https://www.amazon.co.uk/dp/B08S3FMVV7', 'https://www.amazon.co.uk/dp/B09MT54XQZ', 'https://www.amazon.co.uk/dp/B08H95Y452']
for link in links:
  check_stock_amazon(link)