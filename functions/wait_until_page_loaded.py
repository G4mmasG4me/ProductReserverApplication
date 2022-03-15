# imports
import time

def wait_until_page_loaded(driver, max_attempts):
  attempts = 0
  page_state = driver.execute_script('return document.readyState;')
  while page_state != 'complete' or attempts >= max_attempts:
    page_state = driver.execute_script('return document.readyState;')
    attempts += 1
    print('Attempt')
    time.sleep(0.1)