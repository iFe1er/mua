# coding ='utf-8'
from flask import Flask 
from flask.ext.sqlalchemy import *

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:2519766@localhost/words'
app.config['SQLALCHEMY_POOL_RECYCLE']=172800
db=SQLAlchemy(app)


# Upper db.Model and db.String
class Message(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	nickname=db.Column(db.String(255))
	content=db.Column(db.Text)
	#__tablename__='test1' 
	def __init__(self,nn,ct):
		self.nickname=nn
		self.content=ct

	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return 1
		except Exception,e:
			print e
			db.session.rollback()
			return 0

def get_all():
	msg=Message.query.order_by('id desc').all()
	return msg



db.create_all()
