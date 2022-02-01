import requests

def buy_product(item_order, order_queue, product_link, amazon_signed_in_session):
  # item_order = [unfilled_order_item_id, order_item_id, address_line_1, address_line_2, address_postcode, address_city, address_county]
  address_line_1 = item_order[2]
  address_line_2 = item_order[3]
  address_postcode = item_order[4]
  address_city = item_order[5]
  address_county = item_order[6]
  # load product url into amazon session
  amazon_signed_in_session.get(product_link)

  # do inital check to see if it is available

  # unfilled_order_item_id = item_order[0]
  # return [unfilled_order_item_id, order_item_id, order_placed, status, details]

  # get all other parameters
  # then insert these into the payload

  # check for price, and see if it above the max limit

  # quantity: 1
  # submit.buy-now: Submit
  

def buy_basket():
  pass


def add_to_bakset():
  pass