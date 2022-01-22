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

amazon_sign_in_url = 'https://www.amazon.com/gp/sign-in.html'

sign_in_email = 'productreservertest@gmail.com'
sign_in_password = 'ProdReserve2022'

def sign_in_amazon():
  print('start')
  driver.get(amazon_sign_in_url)
  print(driver.current_url)
  print(amazon_sign_in_url)
  if driver.current_url.split('?')[0] == 'https://www.amazon.com/ap/signin'.split('?')[0]: # if currently on sign in page
    print('is on sign in page')
    try: # try signing in
      print('attempting email input')
      email_input = driver.find_element_by_id('ap_email')
      email_input.send_keys(sign_in_email)
      email_input.submit()
      if driver.current_url.split('?')[0] == 'https://www.amazon.com/ap/signin'.split('?')[0]: # if currently on sign in page
        try: # tries to find if there is an error message, i.e. wrong email
          driver.find_element_by_id('auth-error-message-box')
          print('Wrong Email')
          return 'Wrong Email'
        except NoSuchElementException as e: # if no error message box
          try: # tries to input password and submit
            password_input = driver.find_element_by_id('ap_password')
            password_input.send_keys(sign_in_password)
            password_input.submit()
            try: # tries to find if there is an error message, i.e. wrong passwrod
              driver.find_element_by_id('auth-warning-message-box')
              print('Wrong Password')
              return 'Wrong Password'
            except NoSuchElementException as e: # no error box
              print('Logged In')
              cookies = driver.get_cookies()
              return cookies
              # check if logged in
              # may have mobile number popup
          except NoSuchElementException as e: # if no password input box
            print('No Passowrd Input')
            return 'No Password Input'
      else: # not on sign in page
        print('Not On Sign In Page')
        return 'Not On Sign In Page'
    except NoSuchElementException as e: # if email input box not found
      print('No Email Output')
      return 'No Email Input'



output = sign_in_amazon()
print(output)

# cookies required to keep login
# ubid-acbuk
# x-acbuk
# session-token
# if you delete these cookies, then you get logged out