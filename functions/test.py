product_details = [[0,1], [3,4]]
product_link = [2,5]
product_details = tuple(zip(*zip(*product_details), product_link))
print(product_details)