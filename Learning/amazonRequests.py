import requests
import bs4 as BeautifulSoup

site = 'https://www.amazon.com/gp/sign-in.html'

session = requests.Session()

session.headers = {
}

'''get login page'''
resp = session.get(site)
html = resp.text
 
'''get BeautifulSoup object of the html of the login page'''
soup = BeautifulSoup(html , 'lxml')

data = {}
form = soup.find('form', {'name': 'signIn'})
for field in form.find_all('input'):
	try:
 		data[field['name']] = field['value']
	except:
		pass

USERNAME = 'TEST123@TEST123.COM'
PASSOWRD = 'TEST123'

data[u'email'] = USERNAME
data[u'password'] = PASSWORD

post_resp = session.post('https://www.amazon.com/ap/signin', data = data)

post_soup = BeautifulSoup(post_resp.content , 'lxml')
 
if post_soup.find_all('title')[0].text == 'Your Account':
	print('Login Successfull')
else:
	print('Login Failed')