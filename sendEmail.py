import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender='sysu_public@163.com'
receiver='sysu_public@163.com'
subject='from ECS'
smtpserver='smpt.163.com'
username='sysu_public@163.com'
password='laqyjovmtuozeznq'



def send(string):
	try:
		msg=MIMEText(string,_subtype='plain')
		msg['Subject']=Header(subject)

		smtp=smtplib.SMTP()
		smtp.connect('smtp.163.com')
		smtp.login(username,password)
		smtp.sendmail(sender,receiver,msg.as_string())
		smtp.quit()
		return 1
	except:
		return 0
