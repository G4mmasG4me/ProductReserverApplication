from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(executable_path=os.getcwd() + r"\chromedriver.exe", options=chrome_options)

amazon_sign_in_url_goto = '/gp/sign-in.html'
amazon_sign_in_url = '/ap/signin'
amazon_account_fix_up_url = '/ap/accountfixup'

sign_in_email = 'productreservertest@gmail.com'
sign_in_password = 'ProdReserve2022'

def sign_in_amazon():
  driver.get(amazon_sign_in_url)
  if urlparse(driver.current_url).path == amazon_sign_in_url: # if currently on sign in page
    try: # try signing in
      email_input = driver.find_element_by_id('ap_email')
      email_input.send_keys(sign_in_email)
      email_input.submit()
      if urlparse(driver.current_url).path == amazon_sign_in_url: # if currently on sign in page
        try: # tries to find if there is an error message, i.e. wrong email
          driver.find_element_by_id('auth-error-message-box')
          return [False, 'Wrong Email']
        except NoSuchElementException as e: # if no error message box
          try: # tries to input password and submit
            password_input = driver.find_element_by_id('ap_password')
            password_input.send_keys(sign_in_password)
            password_input.submit()
            if urlparse(driver.current_url).path == '':
              pass
            
            # --- Phone Add Form --- #
            elif urlparse(driver.current_url).path == amazon_account_fix_up_url:
              try:
                add_phone_form = driver.find_element(By.ID, 'auth-account-fixup-phone-form')
                try:
                  skip_phone_button = driver.find_element(By.ID, 'ap-account-fixup-phone-skip-link')
                except NoSuchElementException as e:
                  return [False, 'Error Finding Skip Phone Button']
              except NoSuchElementException as e:
                return [False, 'Error Finding Add Phone Box']

            # --- Still On Login Page --- #
            elif urlparse(driver.current_url).path == : # tries to find if there is an error message, i.e. wrong passwrod
              driver.find_element_by_id('auth-warning-message-box')
              return [False, 'Wrong Password']
            except NoSuchElementException as e: # no error box
              cookies = driver.get_cookies()
              return [True, cookies]
              # check if logged in
              # may have mobile number popup
          except NoSuchElementException as e: # if no password input box
            return [False, 'No Password Input'] 
      else: # not on sign in page
        return [False, 'Not On Sign In Page']
    except NoSuchElementException as e: # if email input box not found
      return [False, 'No Email Input']



output = sign_in_amazon()
print(output)

# cookies required to keep login
# ubid-acbuk
# x-acbuk
# session-token
# if you delete these cookies, then you get logged out