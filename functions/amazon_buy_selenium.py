# Selenium Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service


from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time

# Custom Package Imports
import amazon_sign_in_selenium

# Chrome Driver Options
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")

s = Service(ChromeDriverManager().install())

amazon_basket_url = '/gp/cart/view.html?ref_=nav_cart'
check_out_url_path = '/gp/buy/spc/handlers/display.html'
change_address_url = '/gp/buy/addressselect/handlers/display.html'
change_payment_url = '/gp/buy/payselect/handlers/display.html'


card_number = '1024204156346104' # random card number


def buy_amazon_product(prod_url, driver, order_details):
  parsed_prod_url = urlparse(prod_url) # parses product page
  driver.get(prod_url) # goes to product page
  if driver.current_url == prod_url: # checks if driver went to product page
    try:
      cookies_accept_button = driver.find_element(By.ID, 'sp-cc-accept') # looks for cookie accept button
      cookies_accept_button.submit() # submits cookie accept button
    except NoSuchElementException:
      pass
    except Exception as e:
      return [False, 'Failed Accepting Cookie: %s' % e]
    try:
      buy_now_button = driver.find_element(By.ID, 'buy-now-button') # looks for buy now button
      buy_now_button.click() # clicks buy now button

      # -- Checkout Page --
      if urlparse(driver.current_url).path == check_out_url_path: # check if on checkout page

        # -- Address --
        try:
          change_address_button = driver.find_element(By.ID, 'addressChangeLinkId')
          change_address_button.click()
          if urlparse(driver.current_url).path == change_address_url: # if current website is on change address webpage
            # change address
            pass
          else: # if current website not on change address webpage
            return [False, 'Not on Change Address URL']
        except NoSuchElementException: # no change address button
          return [False, 'No Change Address Button']
        except Exception as e:
          return [False, 'Failed To Change Address: %s' % e]

        # -- Payment Method --
        try:
          payment_last_4_digits = driver.find_element(By.XPATH, '//div[@data-field="tails"]')
          if payment_last_4_digits != card_number[-4:]: # if payment method same
            try:
              change_payment_button = driver.find_element(By.ID, '')
              change_payment_button.click()
              if urlparse(driver.current_url).path == change_payment_url: # if on change payment url
                pass
                # change payment details
              else:
                return [False, 'Not on Change Address URL']
            except NoSuchElementException:
              return [False, 'No Change Payment Button']
            except Exception as e:
              return [False, 'Failed To Click Payment Button: %s' % e]
        except NoSuchElementException:
          return [False, 'No Last 4 Digits of Payment Method']
        except Exception as e:
          return [False, 'Failed Searching for Payment Method: %s' % e]

      # -- Still On Product Page | Popout Order --
      elif driver.current_url == prod_url: # if still on product page
        try: # check for checkout popout check out
          pop_out_checkout = driver.find_element(By.ID, 'a-popover-1')
        except NoSuchElementException: # no popout checkout, so fail
          return [False, 'No Checkout Box']
        except Exception as e: # 
          return [False, 'Failed to Checkout: %s' % e]
    except NoSuchElementException:
      return [False, 'No Buy Now Button']
    except Exception as e:
      return [False, 'Failed Adding To Cart: %s' % e]


prod_urls = ['https://www.amazon.co.uk/dp/B009DL2TBA', 'https://www.amazon.co.uk/dp/B00NW479QO', 'https://www.amazon.co.uk/dp/B09GBY7632']
order_details = []
amazon_signed_in, amazon_sign_in_cookies = amazon_sign_in_selenium.sign_in_amazon()
if amazon_signed_in is True: # if signed in, then allow code to execute, wouldn't work if not signed in
  unique_tlds = []
  for prod_url in prod_urls:
    parsed_prod_url = urlparse(prod_url)
    tld = parsed_prod_url.netloc.split('.')[-1]
    if tld not in unique_tlds:
      unique_tlds.append(tld)

  print(unique_tlds)
  # edits cookie names depending on their amazon region using TLDs
  driver = webdriver.Chrome(service=s, options=chrome_options) # starts driver session
    
  driver.execute_cdp_cmd('Network.enable', {}) # allows cookies to be set without going to website
  for tld in unique_tlds:
    if parsed_prod_url.netloc != 'com':
      amazon_sign_in_cookies[0]['name'] = 'ubid-acb' + str(tld)
      amazon_sign_in_cookies[1]['name'] = 'x-acb' + str(tld)

    for cookie in amazon_sign_in_cookies: # loops through sign in cookies
      cookie['domain'] = str(parsed_prod_url.netloc) # changes domain of cookie to correct domain for the given product
      driver.execute_cdp_cmd('Network.setCookie', cookie) # sets cookie

  driver.execute_cdp_cmd('Network.disable', {}) # 
  for prod_url in prod_urls:

    status, error = buy_amazon_product(prod_url, driver, order_details)
    print(status)
    print(error)
else:
  print(amazon_sign_in_cookies)


# need to account for products that are subscriptions products, e.g. https://www.amazon.co.uk/dp/B00NW479QO