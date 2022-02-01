# imports
import mysql.connector
import multiprocessing
import time
import requests

import amazon_check_stock_requests
import amazon_sign_in_selenium
import amazon_buy_requests
import email_customer

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

    chekck_availability_processes = []
    # :
    order_items_queue = multiprocessing.Queue()
    for order_item_position, unique_order in enumerate(unique_order_items):
      p = multiprocessing.Process(target=amazon_check_stock_requests.check_stock_amazon, args=(unique_order, order_items_queue, order_item_position,)) # stock_checker.check_stock
      chekck_availability_processes.append(p)
      p.start()
    for p in chekck_availability_processes:
      p.join()

    availability_output = []
    for p in chekck_availability_processes:
      availability_output.append(order_items_queue.get())
    print(availability_output)

    # runs a for loop through the list of availability outputs

    # create a sign in loop, so incase it fails it retires.
    amazon_signed_in = False
    sign_in_attempts = 0
    while amazon_signed_in is False and sign_in_attempts < 5:
      sign_in_attempts += 1
      amazon_signed_in, amazon_sign_in_cookies = amazon_sign_in_selenium.sign_in_amazon()


    if amazon_signed_in:
      # start requests session
      amazon_session = requests.Session()
      # laod cookies into session
      for cookie in amazon_sign_in_cookies:
        amazon_session.amazon_sign_in_cookies.set(cookie['name'], cookie['value'])

      item_available = False

      # create order queue
      order_queue = multiprocessing.Queue()

      buy_item_processes = []
      for availability_position, availability in enumerate(availability_output):
        # if the product is available to order
        if availability[1] == True:
          item_available = True
          order_item = unique_order_items[availability_position]
          product_link = order_item[2]
          product_region = order_item[3]

          sql = ('SELECT unfilled_order_item.id, unfilled_order_item.order_item_id, address.line_1, address.line_2, address.postcode, address.city, address.county FROM unfilled_order_item INNER JOIN order_item ON unfilled_order_item.order_item_id = order_item.id INNER JOIN address ON order_item.address_id = address.id WHERE order_item.product_id = %s AND address.country = %s  ')
          mycursor.execute(sql, (order_item[0], order_item[3])) # parameters are product id and link region
          item_orders = mycursor.fetchall()

          
          
          for item_order_position, item_order in enumerate(item_orders):
            # item order = [unfilled_order_item_id, order_item_id, address_line_1, address_line_2, address_postcode, address_city, address_county]
            p = multiprocessing.Process(target=amazon_buy_requests.buy_product, args=(item_order, order_queue, product_link, amazon_session))
            buy_item_processes.append(p)
      
      if item_available:
        
        for p in buy_item_processes:
          p.start()
        for p in buy_item_processes:
          p.join()
          
        order_output = []
        for p in buy_item_processes:
          order_output.append(order_items_queue.get())

        email_processes = []
        email_queue = multiprocessing.Queue()
        # each item in order_output should look like [unfilled_order_item_id, order_placed, status, details]
        for unfilled_order_item_id, order_item_id, order_placed, status, details in order_output:
          if order_placed: # if order successfully placed
            # move unfilled_order_item to filled_order_item
            sql = ('BEGIN TRANSACTION; INSERT INTO filled_order_item (order_item_id) SELECT (order_item_id) FROM unfilled_order_item WHERE unfilled_order_item.id = %s; DELETE FROM unfilled_order_item WHERE unfilled_order_item.id = %s; COMMIT;')
            mycursor.execute(sql, (unfilled_order_item_id, unfilled_order_item_id)) # parameters are product id and link region

            # things to insert into db
            amazon_order_code = 0
            sql = ('INSERT INTO order_item (order_site, order_code) VALUES (%s, %s) WHERE id = %s')
            mycursor.execute(sql, ('Amazon', amazon_order_code, order_item_id))
            

            # email user
            # create a process of emailing customers
            p = multiprocessing.Process(target=email_customer.email_on_order_completition, args=(email_queue))
            email_processes.append(p)
        
        for p in email_processes:
          p.start()
        for p in email_processes:
          p.join()
        
        email_output = []
        for p in email_processes:
          email_output.append(email_queue.get())