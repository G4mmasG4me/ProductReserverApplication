import smtplib
port = 587
smtp_server = 'smtp.gmail.com'
sender_email = 'productreservertest@gmail.com'
password = 'byumamkhzzgazkgx'

def email_on_order_completion(receiver_email, order_details):

  receiver_email = 'domhough@hotmail.co.uk'


  message = 'Hello how are?'

  try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    server.close()
    print('Success')
  except Exception as e:
    print(e)
    print('Fail')