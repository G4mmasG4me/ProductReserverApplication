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
import os

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--start-maximized)
# chrome_options.add_argument('--incognito)
# chrome_options.add_argument('--disable-popup-blocking)
# chrome_options.add_argument('--disable-infobars)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)

amazon_sign_in_url = 'https://www.amazon.com/gp/sign-in.html'
amazon_sign_in_check_url = '/ap/sigin'

sign_in_email = 'productreservertest@gmail.com'
sign_in_password = 'ProdReserve2022'

def sign_in_amazon():
  driver.get(amazon_sign_in_url)
  if urlparse(driver.current_url).path == amazon_sign_in_check_url: # if currently on sign in page
    try: # try signing in
      email_input = driver.find_element(By.ID, 'ap_email')
      email_input.send_keys(sign_in_email)
      email_input.submit()
      if urlparse(driver.current_url).path == amazon_sign_in_check_url: # if currently on sign in page
        try: # tries to find if there is an error message, i.e. wrong email
          driver.find_element(By.ID, 'auth-error-message-box')
          return [False, 'Wrong Email']
        except NoSuchElementException as e: # if no error message box
          try: # tries to input password and submit
            password_input = driver.find_element(By.ID, 'ap_password')
            password_input.send_keys(sign_in_password)
            password_input.submit()
            try: # tries to find if there is an error message, i.e. wrong passwrod
              driver.find_element(By.ID, 'auth-warning-message-box')
              return [False, 'Wrong Password']
            except NoSuchElementException as e: # no error box |
              try:
                # find captcha box
                captcha_box = driver.find_element(By.ID, '')
                return [False, 'Captcha'] # cant currently solve captcha, develop ML to solve amazon captcha
                # upon solving captcha
                if urlparse(driver.current_url).netloc == 'www.amazon.com':
                  ubid_cookie = driver.get_cookie('ubid-main')
                  x_cookie = driver.get_cookie('x-main')
                  session_token_cookie = driver.get_cookie('session-token')
                  return [True, [ubid_cookie, x_cookie, session_token_cookie]]
                else:
                  return [False, 'Error Signing In']
              except NoSuchElementException: # successfull login
                if urlparse(driver.current_url).netloc == 'www.amazon.com':
                  ubid_cookie = driver.get_cookie('ubid-main')
                  x_cookie = driver.get_cookie('x-main')
                  session_token_cookie = driver.get_cookie('session-token')
                  return [True, [ubid_cookie, x_cookie, session_token_cookie]]
                else:
                  return [False, 'Error Signing In']
              except Exception as e:
                return [False, 'Error Solving Captcha: %s' % e]
          except NoSuchElementException as e: # if no password input box
            return [False, 'No Password Input'] 
          except Exception as e:
            return [False, 'Unable to Input Password: %s' % e]
      else: # not on sign in page
        return [False, 'Not On Sign In Page']
    except NoSuchElementException as e: # if email input box not found
      return [False, 'No Email Input']
    except Exception as e:
      return [False, 'Unable to Input Email: %s' % e]

# cookies required to keep login | .co.uk
# ubid-acbuk
# x-acbuk
# session-token
# if you delete these cookies, then you get logged out

# cookies required to keep login | .com
# ubid-main
# x-main
# session-token

# cookies required to keep login | .fr
# ubid-abcfr
# x-acbfr
# session-token