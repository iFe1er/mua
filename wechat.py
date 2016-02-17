# -*- coding:utf-8 -*-
from flask import *
from flask.ext.bootstrap import Bootstrap
from model import *
from sendEmail import *
from joke import *
import hashlib
from wechat_sdk import *
from wechat_sdk.exceptions import ParseError

app=Flask(__name__)
contents=[]
#dont forget this
Bootstrap(app)
app.secret_key='key'
#db.create_all()创建表，表名为类名； 然后创建实例 a=User(), 用实例a进行各种操作，

@app.route('/wechat',methods=['POST','GET'])
def veri():
	token='love455389351s'
	L=[request.args.get('timestamp'),request.args.get('nonce'),token]
	L=sorted(L)
	try:
		s=L[0]+L[1]+L[2]
	except:
		return 'error1'
	if hashlib.sha1(s).hexdigest() != request.args.get('signature'):
		return hashlib.sha1(s).hexdigest()
	else:
		
		conf = WechatConf(
   		token='love455389351s', 
		appid='wx9aa5de1ba97e5286', 
		appsecret='530cd7acc4a40fab89968de9c232b3dc', 
		encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
		encoding_aes_key='dxrEyX2LugiPhSSMv8KpPNxq6ywAz74cODU9HQRZOlD'  # 如果传入此值则必须保证同时传入 token, appid
)
		wechat = WechatBasic(conf=conf)
		body_text=request.get_data()
   		
		wechat.parse_data(body_text)	
		
		content = wechat.message.content			
		send(content)
		xml=wechat.response_text(content='I got it')
		return Response(xml, mimetype='text/xml')

@app.route('/',methods=['POST','GET'])
def mainpage():
	contents=get_all()
	if contents:
		if len(contents)<=10:
			return render_template("main.html",contents=contents,pagenumber=1)
		else:
			return render_template("main.html",contents=contents[0:9],pagenumber=1)
	else:
		mywords=[{'id':'1','content':u'你好，我是小麦，来这里畅所欲言吧！是完全匿名的哦~','nickname':u'管理员 小麦'}]
		return render_template("main.html",contents=mywords,pagenumber=1)


@app.route('/post',methods=['POST'])
def post():
	if request.method=='POST':
		contents=get_all()
		nickname=request.form['nickname']
		message=request.form['message']
		if not nickname:
			flash(u'啥 你居然懒得连名字都懒得编？')
			return redirect('/')
		if not message:
			flash(u'你说什么，我！听！不！见！')
			return redirect('/')
		temp_class=Message(nickname,message)
		status=temp_class.add()
		if status==1:
			flash(u'匿名消息已发送')
			contents=get_all()
			return redirect('/')
		else:
			flash(u'啊，刚才分神了，你再说一次呗')
			return redirect('/')

@app.route('/page/<page>',methods=['POST','GET'])
def turnpage(page):
	contents=get_all()
	if contents:
		if len(contents)<=10:
			return render_template("main.html",contents=contents,pagenumber=eval(page))
		else:
			return render_template("main.html",contents=contents[10*page:10*page+9],pagenumber=eval(page))
	else:
		mywords=[{'id':'1','content':u'你好，我是小麦，来这里畅所欲言吧！是完全匿名的哦~','nickname':u'管理员 小麦'}]
		return render_template("main.html",contents=mywords,pagenumber=eval(page))


@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/jokes')
def jokes():
	contents=get_jokes_lists()
	return render_template("jokes.html",contents=contents)

@app.route('/course')
def course():
	return render_template("course.html")

@app.route('/submit_contact',methods=['POST','GET'])
def submit_contact():
	if request.method=='POST':
		name=request.form['name']
		email=request.form['email']
		subject=request.form['subject']
		message=request.form['message']
		string="""
		Contact-Information:
		From: %s ;
		Email: %s ;
		subject: %s;
		message: %s ;

		""" % (name,email,subject,message)
		status=send(string)
		if status==1:
			flash(u'成功，您的邮件已发送到我的邮箱，我会尽快与您联系')
		else:
			flash(u'咦，没发送成功呢，请直接加小麦的微信吧~手机号在旁边哦！')
		return render_template("contact.html")
	return render_template("contact.html")

if __name__=="__main__":
	app.run(debug=True,	port=8080)
