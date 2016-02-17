# coding ='utf-8'
from flask import Flask
from flask.ext.sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2519766@localhost/words'
app.config['SQLALCHEMY_POOL_RECYCLE']=172800
db = SQLAlchemy(app)


class Spages3(db.Model):
    # define column
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(255))
    pages = db.Column(db.Text)
    cookies=db.Column(db.String(255))
    number=db.Column(db.String(255))
    status=db.Column(db.String(255))
    select=db.Column(db.String(255))
    drop=db.Column(db.String(255))
    def __init__(self, s=' ', p=' ',c=' ',n=' ',st=' ',se=' ',dr=' '):
        # define our class
        self.sid = s
        self.pages = p
        self.cookies=c
        self.number=n
        self.status=st
        self.select=se
        self.drop=dr

    def add(self):
        # try:
        db.session.add(self)
        db.session.commit()
        return 1
        '''
		except Exception,e:
			print e
			db.session.rollback()
			return 0
		'''

    def query_by_sid(self, s):
        result = self.query.order_by('id desc').filter_by(sid=s).first()
        if result != None:
            return result
        else:
            return None

    def query_by_number(self,n):
        result=self.query.order_by('id desc').filter_by(number=n).first()
        if result !=  None:
            return result
        else:
            return None

db.create_all()
