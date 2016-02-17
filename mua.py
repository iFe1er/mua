# -*- coding:utf-8 -*-
from flask import *
from flask.ext.bootstrap import Bootstrap
from model2 import *
from model import *
from sendEmail import *
from joke import *
from coursebook import get_course_page
import hashlib
from check_message import check_message
from wechat_sdk import *
from wechat_sdk.exceptions import ParseError


app = Flask(__name__)
contents = []
# dont forget this
Bootstrap(app)
app.secret_key = 'key'


# db.create_all()创建表，表名为类名； 然后创建实例 a=User(), 用实例a进行各种操作，

# 接受微信公众号消息，并自动回复和数据库查询
@app.route('/wechat', methods=['POST', 'GET'])
def veri():
    f=open('/root/mua/token','r')
    token=f.readline().split('\n')[0]
    f.close()
    f=open('/root/mua/secret','r')
    secret=f.readline().split('\n')[0]
    f.close()

    L = [request.args.get('timestamp'), request.args.get('nonce'), token]
    L = sorted(L)
    try:
        s = L[0] + L[1] + L[2]
    except:
        return 'error1'
    if hashlib.sha1(s).hexdigest() != request.args.get('signature'):
        return 'error2'
    else:
        #公众号初始化配置
        conf = WechatConf(
            token=token,
            appid='wx9aa5de1ba97e5286',
            appsecret=secret,
            encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
            encoding_aes_key='dxrEyX2LugiPhSSMv8KpPNxq6ywAz74cODU9HQRZOlD'  # 如果传入此值则必须保证同时传入 token, appid
        )
        wechat = WechatBasic(conf=conf)
        body_text = request.get_data()
        # 解析接收到的数据
        wechat.parse_data(body_text.decode('utf-8'))
        # 仅处理文字型的数据
        content = wechat.message.content
        # 是否符合学号规范
        if check_message(content) == False:
            if content==u'猴年快乐':
                xml = wechat.response_text(content=u'小麦也祝你猴年快乐！\n----------------------\nMua网站首页：http://mua.cm，点击蓝色按钮进入课书。使用前务必阅读"Must-Read"。实时查询状态请直接向我回复学号\nPC端访问视觉体验更佳\n备用站:http://sysu.iego.cn')
            else:
                xml = wechat.response_text(content=u'学号不对呢，亲要不再试试？格式:直接输入14341234')
        else:
            # 修改为每次import
            import model3
            a=model3.Mua()
            # 查询是否有该学号用户
            result=a.query_by_number(content)
            if result==None:
                xml=wechat.response_text(content=u'学号没有记录哟，亲是不是没有用该服务呢？')
            # 存在该学号用户，对不同状态码进行自动回复
            elif result.status == '0':
                msg=u"""
【状态查询】
第%s个使用者
学号: %s
抢课: %s
抢前退课: %s
状态:未开始
-感谢使用mua-
                """ % (result.id,content,result.select,result.drop)
                xml=wechat.response_text(content=msg)
            elif result.status=='1':
                msg=u"""
【状态查询】
第%s个使用者
学号: %s
抢课: %s
抢前退课: %s
状态:正在刷课
-感谢使用mua-
                """ % (result.id,content,result.select,result.drop)
                xml=wechat.response_text(content=msg)
            elif result.status=='2':
                msg=u"""
【状态查询】
第%s个使用者
学号: %s
抢课: %s
抢前退课: %s
状态:抢课成功
-感谢使用mua-
                """ % (result.id,content,result.select,result.drop)
                xml=wechat.response_text(content=msg)

            elif result.status=='3':
                msg=u"""
【状态查询】
第%s个使用者
学号: %s
抢课: %s
抢前退课: %s
状态:抢课失败，请勿在抢课中登陆
-感谢使用mua-
                """ % (result.id,content,result.select,result.drop)
                xml=wechat.response_text(content=msg)
            else:
                msg=u"""
【状态查询】
第%s个使用者
学号: %s
抢课: %s
抢前退课: %s
状态:不明原因的失败，请联系作者
-感谢使用mua-
                """ % (result.id,content,result.select,result.drop)
                xml=wechat.response_text(content=msg)
        # 构造完成，返回消息
        return Response(xml, mimetype='text/xml')

# 根地址，匿名树洞
@app.route('/')
def main():
    # 判断有无消息，大于10要分页
    contents = get_all()
    if contents:
        if len(contents) <= 10:
            return render_template("main.html", contents=contents, pagenumber=1)
        else:
            return render_template("main.html", contents=contents[0:9], pagenumber=1)
    else:
        mywords = [{'id': '1', 'content': u'你好，我是小麦，来这里畅所欲言吧！是完全匿名的哦~', 'nickname': u'管理员 小麦'}]
        return render_template("main.html", contents=mywords, pagenumber=1)

# 介绍页
@app.route('/intro')
def index():
    return render_template("index.html")

# 匿名主页，同根域名
@app.route('/annoy', methods=['POST', 'GET'])
def annoy():
    contents = get_all()
    if contents:
        if len(contents) <= 10:
            return render_template("main.html", contents=contents, pagenumber=1)
        else:
            return render_template("main.html", contents=contents[0:9], pagenumber=1)
    else:
        mywords = [{'id': '1', 'content': u'你好，我是小麦，来这里畅所欲言吧！是完全匿名的哦~', 'nickname': u'管理员 小麦'}]
        return render_template("main.html", contents=mywords, pagenumber=1)

# 发表匿名消息
@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        contents = get_all()
        nickname = request.form['nickname']
        message = request.form['message']
        if not nickname:
            flash(u'啥 你居然懒得连名字都懒得编？')
            return redirect(url_for("annoy"))
        if not message:
            flash(u'你说什么，我！听！不！见！')
            return redirect(url_for("annoy"))
        temp_class = Message(nickname, message)
        status = temp_class.add()
        if status == 1:
            flash(u'匿名消息已发送')
            contents = get_all()
            return redirect(url_for("annoy"))
        else:
            flash(u'啊，刚才分神了，你再说一次呗')
            return redirect(url_for("annoy"))


# 树洞翻页
@app.route('/page/<page>', methods=['POST', 'GET'])
def turnpage(page):
    contents = get_all()
    if contents:
        if len(contents) <= 10:
            return render_template("main.html", contents=contents, pagenumber=eval(page))
        else:
            return render_template("main.html", contents=contents[10 * page:10 * page + 9], pagenumber=eval(page))
    else:
        mywords = [{'id': '1', 'content': u'你好，我是小麦，来这里畅所欲言吧！是完全匿名的哦~', 'nickname': u'管理员 小麦'}]
        return render_template("main.html", contents=mywords, pagenumber=eval(page))

# 联系页面
@app.route('/contact')
def contact():
    return render_template("contact.html")

# 笑话页面
@app.route('/jokes')
def jokes():
    # 取得随机笑话
    contents = get_jokes_lists()
    # 发布笑话
    return render_template("jokes.html", contents=contents)

# 课书主页
@app.route('/course')
def course():
    return render_template("course.html")

# 提交建议和意见
@app.route('/submit_contact', methods=['POST', 'GET'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        string = """
        Contact-Information:
        From: %s ;
        Email: %s ;
        subject: %s;
        message: %s ;

        """ % (name, email, subject, message)
        # 自定制发送邮件
        status = send(string)
        if status == 1:
            flash(u'成功，您的邮件已发送到我的邮箱，我会尽快与您联系')
        else:
            flash(u'咦，没发送成功呢，请直接加小麦的微信吧~手机号在旁边哦！')
        return render_template("contact.html")
    return render_template("contact.html")

# 存储密码
@app.route('/course/option', methods=['POST', 'GET'])
def menu():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    session['password'] = password
    return render_template('menu.html')

# 选择课程类型后，显示要抢选的课程页面
@app.route('/login/<option>')
def login(option):
    try:
        instance = get_course_page(session['username'], session['password'])
    except:
        try:
            instance = get_course_page(session['username'], session['password'])
        except:
            return redirect(url_for("course"))
    page = instance.get_course(eval(option))
    session['mode']=option
    session['ck'] = instance.r1.cookies['JSESSIONID']
    session['sid'] = instance.sid
    # session['aabb']=jsonpickle.encode(instance)
    # select_page=page.split('<tbody>')[0]+'<tbody>'+page.split('<tbody>')[2]
    select_page = page.split('<body>')[0] + '<body><h1>请单击课程名称，选择你要【抢选】的课程</h1>' + page.split('<body>')[1]
    sp2=select_page.split("<h3 style='margin-top:1em'>")[0]+"<h3 style='margin-top:1em'>"+select_page.split("<h3 style='margin-top:1em'>")[2]
    #try:
    orm = Spages3(instance.sid, page,session['ck'],session['username'],'0','0','0')
    orm.add()
    #except:
    #    return 'Oop！'
    return sp2

# 显示要退选的课程页面(可以跳过)
@app.route('/course/select/<jxbh>')
def select_course(jxbh):
    # instance=course_manip(session.get('sid'),jsonpickle.decode(session.get('ck')))
    # instance.select_course(jxbh)

    session['select'] = jxbh
    a = Spages3()
    key = session['sid']
    ##fuck you! use ".page" to query a column of result
    pages = a.query_by_sid(key).pages
    drop_pages = pages.split('<body>')[0] + u'''
    <body><h1>请单击课程名称，选择你要【退选】的课程</h1>
    <h1>如果【只抢不退】，请<a href='/course/drop/omit'>点击此处<a>跳过该步骤</h1>
    ''' + pages.split('<body>')[1]
    dp2=drop_pages.split("<h3 style='margin-top:1em'>")[0]+"<h3 style='margin-top:1em'>"+drop_pages.split("<h3 style='margin-top:1em'>")[1]
    return dp2

# 退选那门课
@app.route('/course/drop/<jxbh>')
def drop_course(jxbh):
    # instance=course_manip(session.get('sid'),jsonpickle.decode(session.get('ck')))
    # instance.drop_course(jxbh):
    session['drop'] = jxbh
    return redirect(url_for("confirm"))

# 确认
@app.route('/course/confirm')
def confirm():
    if session.get('drop') == 'omit':
        return render_template("confirm.html", select_course=session.get('select'))
    else:
        return render_template("confirm.html", select_course=session.get('select'), drop_course=session.get('drop'))

# 确认成功 把信息全部存入数据库Mua中
@app.route("/course/confirm_yes")
def confirm_yes():
    #try:
    temp = Spages3()
    pages = temp.query_by_sid(session['sid']).pages
    import model3
    orm = model3.Mua(session['sid'], pages, session['ck'], session['username'], '0', session['select'], session['drop'], 0, session['mode'])
    orm.add()
    model3.db.session.commit()
    return render_template("confirm_success.html", select_course=session.get('select'), drop_course=session.get('drop'))

    #except:
    #    return 'Oop！'

    '''USEFUL MESSAGE IN BUILDING OVER-WATCHING SOFTWARE AND QUERYING SOFTWARE
    instance = course_manip(session.get('sid'), session.get('ck'))
    if session.get('drop') != 'omit':
        status1 = instance.drop_course(session['drop'])
    else:
        status1=1
    status2 = instance.select_course(session['select'])
    if status1 and status2:
        return render_template("confirm_success.html", select_course=session.get('select'),
                               drop_course=session.get('drop'))
    else:
        return '错了啦再选一次啊'
    '''

if __name__ == "__main__":
    app.run(debug=True, port=8080)
