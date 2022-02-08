# use requests, look for div with 'availability' id
# then check the span for it
# depending on that text, will tell you if its available or not
# ' Currently unavailable. ' - out of stock
# ' In stock. ' - in stock

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
    while captcha_form and captcha_attempts < 5: # if availability is not found, and captcha form is found, captcha attempts is less than 5
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




# form values
# amzn: get from form
# amzn-r: refer website / product url e.g. /dp/B08H95Y452
# field-keywords: captcha answer


# current problem
# only works on english speaking websites
# to work on all language website
# I need to check if it shows the price of the product or not
# If it shows the price, it means it's in stock
# If it doesn't show the price, it means it's out of stock+

# some amazon websites have product price with id="priceblock_ourprice"
# eg | <span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">€17.99</span>

# others have higher elements with id="corePriceDisplay_desktop_feature_div"

# if i rely on availability message, then it's not going to work across different languages
# could create a list of all unavailable message across different languages

