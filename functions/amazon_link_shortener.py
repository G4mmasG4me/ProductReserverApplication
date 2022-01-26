from urllib.parse import urlparse

unshortened_link = 'https://www.amazon.com/PlayStation-5-DualSense-Wireless-Controller/dp/B08H99BPJN/ref=sr_1_3?crid=88LLA78MLLT9&keywords=ps5+controller&qid=1641843550&sprefix=ps5+controll%2Caps%2C147&sr=8-3'

parsed_url = urlparse(unshortened_link)

tld_list = parsed_url.netloc.split('.')[2:]
tld_string = '.'.join(tld_list)

url_path_components = parsed_url.path.split('/')
dp_pos = url_path_components.index('dp')
url_shortened_path = url_path_components[dp_pos+1]

shortened_link = parsed_url.scheme + '://' + parsed_url.netloc + '/dp/' + url_shortened_path