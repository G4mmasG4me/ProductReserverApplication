import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://www.amazon.com/gp/sign-in.html'

headers = {
	'User-Agent':  UserAgent().chrome, #'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
	'Accept-Language': 'en-us, en:q=0.5'
}

s = requests.Session()
webpage = s.get(url, headers=headers)

soup = BeautifulSoup(webpage.content, 'html.parser')
print(soup.prettify())



# so payload for amazon sign in
# appActionToken
# appAction
# metadata1 | only loaded if javascript is rendered
# openid.return_to
# prevRID
# workflowState
# email
# encryptedPwd | encrypted upon post, so the payload is encrypted unlike when you are idle on the sign in page
# encryptedPasswordExpected | blank


# may be able to login with selenium, and then switch to requests, by getting all of the cookies and setting them on the current requests session

'''
s = requests.session()
s.headers.update(headers)

for cookie in driver.get_cookies():
	c = {cookie['name']: cookie['value']}
	s.cookies.update(c)
'''