import amazon_check_stock_requests
#import amazon_check_stock_selenium
from datetime import datetime
import time

while True:
  availability_requests = amazon_check_stock_requests.check_stock('https://www.amazon.com/dp/B08H99BPJN')
  #availability_selenium = amazon_check_stock_selenium.check_stock('https://www.amazon.co.uk/dp/B08H95Y452')

  time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(time + ' : ' + str(availability_requests))