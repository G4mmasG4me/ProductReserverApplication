# imports
import mysql.connector
import multiprocessing
import time
import requests

# custom functions imports
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
  while running is True:
    
    start = time.time()
    # select a list of product_ids and their country where they were ordered from
    mycursor.execute('SELECT DISTINCT order_item.product_id, product_link.id, product_link.link, address.country FROM unfilled_order_item INNER JOIN order_item ON unfilled_order_item.order_item_id = order_item.id INNER JOIN address ON order_item.address_id = address.id INNER JOIN product_link WHERE (product_link.product_id = order_item.product_id AND product_link.region = address.country)')

    # fetches all results from mysql server
    unique_order_items = mycursor.fetchall()
    
    # seperates the different components of unique orders
    product_ids, link_ids, product_links, order_regions = map(list, zip(*unique_order_items))

    check_availability_processes = []
    # :
    order_items_queue = multiprocessing.Queue()
    for order_item_position, unique_order in enumerate(unique_order_items):
      p = multiprocessing.Process(target=amazon_check_stock_requests.check_stock_amazon, args=(unique_order[2], order_items_queue, order_item_position,)) # stock_checker.check_stock
      check_availability_processes.append(p)
      p.start()
    for p in check_availability_processes:
      p.join()

    availability_output = []
    for p in check_availability_processes:
      availability_output.append(order_items_queue.get())
    print(availability_output)

    # runs a for loop through the list of availability outputs

      # create order queue

    email_processes = []
    for availability_position, availability in enumerate(availability_output):
      # if the product is available to order
      if availability is True:
        order_item = unique_order_items[availability_position]
        product_id = order_item[0]
        product_link = order_item[2]
        product_region = order_item[3]

        # get a list of all emails based on their product and region
        sql = 'SELECT DISTINCT user.email FROM availability_mailing_list INNER JOIN user ON availability_mailing_list.user_id = user.id INNER JOIN address ON user.id = address.user_id WHERE (availability_mailing_list.product_id = %s AND user.country = %s)'
        mycursor.execute(sql, (product_id, product_region)) # parameters are product id and link region
        emails = mycursor.fetchall()

        for email in emails:
          pass
            


# process
# user buys service
# check availability on chosen product
# if available then buy product
# if bought then change details in db, and email user