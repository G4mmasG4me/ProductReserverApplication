import requests

def buy_product(item_order, order_queue, product_link, amazon_signed_in_session):
  # load product url into amazon session
  amazon_signed_in_session.get(product_link)

  # do inital check to see if it is available

  # unfilled_order_item_id = item_order[0]
  # return [unfilled_order_item_id, status]

  # get all other parameters
  # then insert these into the payload

  # quantity: 1
  # submit.buy-now: Submit




def buy_basket():
  pass