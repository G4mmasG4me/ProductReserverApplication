import requests

def buy_product(item_order, order_queue, product_link, amazon_sign_in_cookies):
  pass
  # start requests session
  session = requests.Session()
  # laod cookies into session
  for cookie in amazon_sign_in_cookies:
    session.amazon_sign_in_cookies.set(cookie['name'], cookie['value'])

  # load website in requests session
  # check if 
  # unfilled_order_item_id = item_order[0]
  # return [unfilled_order_item_id, status]

def buy_basket():
  pass