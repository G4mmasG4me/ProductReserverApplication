from urllib.parse import urlparse

check_out_url = 'https://www.amazon.co.uk/gp/buy/spc/handlers/display.html?hasWorkingJavascript=1'

parsed_url = urlparse(check_out_url)
print(parsed_url)