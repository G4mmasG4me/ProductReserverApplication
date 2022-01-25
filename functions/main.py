# imports
import mysql.connector
import multiprocessing
import time

import amazon_check_stock_requests
import amazon_sign_in_selenium
import amazon_buy_requests

# connect to database

mydb = mysql.connector.connect(
  host="localhost",
  username="root",
  password="",
  database="productreserver"
)

mycursor = mydb.cursor()

running = True


if __name__ == '__main__':
  print('test')
  manager = multiprocessing.Manager()
  while running:
    
    start = time.time()
    # select a list of product_ids and their country where they were ordered from
    mycursor.execute('SELECT DISTINCT order_item.product_id, product_link.id, product_link.link, address.country  FROM unfilled_order_item INNER JOIN order_item ON unfilled_order_item.order_item_id = order_item.id INNER JOIN address ON order_item.address_id = address.id INNER JOIN product_link ON (product_link.product_id = order_item.product_id AND product_link.region = address.country)')

    # fetches all results from mysql server
    unique_order_items = mycursor.fetchall()

    # creates an output list filled with 0s of the amount of unique orders
    # output = manager.list([0]*len(unique_orders))
    
    # seperates the different components of unique orders
    product_ids, link_ids, product_links, order_regions = map(list, zip(*unique_order_items))

    processes = []
    # :
    order_items_queue = multiprocessing.Queue()
    for order_item_position, unique_order in enumerate(unique_order_items):
      p = multiprocessing.Process(target=amazon_check_stock_requests.check_stock_amazon, args=(unique_order, order_items_queue, order_item_position,)) # stock_checker.check_stock
      processes.append(p)
      p.start()
    for p in processes:
      p.join()

    availability_output = []
    for p in processes:
      availability_output.append(order_items_queue.get())
    print(availability_output)

    # runs a for loop through the list of availability outputs

    # need to sign in with selenium
    # and then transfer cookies to requests

    # create a sign in loop, so incase it fails it retires.
    amazon_sign_in_cookies = amazon_sign_in_selenium.sign_in_amazon()

    # create requests session here and then load cookies into it and pass it to each order
    # or create a new session for each order, and then load cookies into it.
    # 2nd option is expensive as you repeat creating a session and loading cookies. But less conflict

    order_queue = multiprocessing.Queue()

    processes = []
    item_available = True
    if item_available:
      for availability_position, availability in enumerate(availability_output):
        # if the product is available to order
        if availability[1] == True:
          order_item = unique_order_items[availability_position]
          product_link = order_item[2]
          product_region = order_item[3]
          # next need to get all orders items on unfilled orders and then get the corresponding order details
          # things i need to select
          # order_item_id, address_line_1, address_line_2, address_postcode, address_city, address_county, address_country.
          sql = ('SELECT unfilled_order_item.id, address.line_1, address.line_2, address.postcode, address.city, address.county FROM unfilled_order_item INNER JOIN order_item ON unfilled_order_item.order_item_id = order_item.id INNER JOIN address ON order_item.address_id = address.id WHERE order_item.product_id = %s AND address.country = %s  ')
          mycursor.execute(sql, (order_item[0], order_item[3])) # parameters are product id and link region
          item_orders = mycursor.fetchall()

          
          
          for item_order_position, item_order in enumerate(item_orders):
            # item order = [unfilled_order_item_id, address_line_1, address_line_2, address_postcode, address_city, address_county]
            p = multiprocessing.Process(target=amazon_buy_requests.buy_product, args=(item_order, order_queue, product_link, amazon_sign_in_cookies))
            processes.append(p)
      for p in processes:
        p.start()
      for p in processes:
        p.join()
      
      order_output = []
      for p in processes:
        order_output.append(order_items_queue.get())
      print(order_output)
      # each item in order_output should look like [unfilled_order_item_id, status]
      # to get specific order
      # order = unique_order_items[positon]