# coding ='utf-8'
from flask import Flask
from flask.ext.sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2519766@localhost/words'
app.config['SQLALCHEMY_POOL_RECYCLE']=172800

db = SQLAlchemy(app)


class Mua(db.Model):
    # define column
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(255))
    pages = db.Column(db.Text)
    cookies=db.Column(db.String(255))
    number=db.Column(db.String(255))
    select=db.Column(db.String(255))
    drop=db.Column(db.String(255))
    status=db.Column(db.String(255))
    errorcount=db.Column(db.Integer)
    mode=db.Column(db.String(255))
    #0~3 GB GX ZB ZX
    def __init__(self, s=' ', p=' ',c=' ',n=' ',st=' ',se=' ',dr=' ',ec=0,md=' s'):
        # define our class
        self.sid = s
        self.pages = p
        self.cookies=c
        self.number=n
        self.status=st
        self.select=se
        self.drop=dr
        self.errorcount=ec
        self.mode=md
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

    def modify_status_with_id(self,s,status):
        try:
            self.query.filter_by(id=s).update({"status":status})
            return 1
        except:
            return 0

    def modify_status_with_sid(self,s,status):
        self.query.filter_by(sid=s).update({"status":status})

    def modify_errorcount_with_sid_add_one(self,s):
        result=self.query.order_by('id desc').filter_by(sid=s).first().errorcount
        res=result+1
        self.query.filter_by(sid=s).update({"errorcount":res})

db.create_all()
