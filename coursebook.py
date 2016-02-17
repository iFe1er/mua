#coding:utf-8

import requests,re,hashlib
from PIL import Image
from main import *
from Tool import Tool
from lxml import etree

class get_course_page:
    def __init__(self,un,pw):
        self.username=un
        self.password=pw
        xpath_gb='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[2]/a/@href'
        xpath_gx='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td[2]/a/@href'
        xpath_zb='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td[2]/a/@href'
        xpath_zx='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[4]/td[2]/a/@href'
        self.semester='3'

        # 用户的登陆主界面
        url1='http://uems.sysu.edu.cn/elect'
        # 验证码界面
        url2='http://uems.sysu.edu.cn/elect/login/code'
        # 登陆请求url
        url3='http://uems.sysu.edu.cn/elect/login'

        # 访问注界面，取得cookies：r1.cookies
        self.r1=requests.get(url1)

        # 在这里v的值可以随机给一个
        p={'v':'0.7235605481546372'}
        # 用主界面也就是url1的cookies访问验证码网站url2
        r2=requests.get(url2,params=p,cookies=self.r1.cookies)

        # 用二进制读入方式写验证码文件
        output=open(r'/root/mua/ocr/ve.jpg','wb')
        #验证码文件写入（r2.content）
        output.write(r2.content)
        # 记得此处要保存！
        output.close()

        #raw_input输入默认为string
        #username=raw_input(u'请输入帐号，按回车键结束\n')
        #password=raw_input(u'请输入密码，按回车键结束\n')

        # 对密码进行md5加密
        passwordEncoded=hashlib.md5(self.password).hexdigest().upper()

        # 识别验证码！
        veriObj = verifyFunction('/root/mua/ocr/ve.jpg')
        vericode=veriObj.getverify1()


        # 设置登陆url3所需要的头（注意这里已缺省cookies，到后面的cookie参数时再调用r1.cookies）
        headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'104',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'uems.sysu.edu.cn',
        'Origin':'http://uems.sysu.edu.cn',
        'Referer':'http://uems.sysu.edu.cn/elect/index.html?_t=1445313601933',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'}
        #设置登陆表单信息
        #在这里，username是输入的账户，passwordEncoded是输入密码的md5加密，j_code是识别出来的验证码vericode
        data={'username':self.username,
        'password':passwordEncoded,
        'j_code': vericode,
        'lt':'',
        '_eventId':'submit',
        'gateway':'true'}

        # 模拟登陆的头，同样没有Cookies项
        headers_Login={
        'Accept':'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'uems.sysu.edu.cn',
        'Referer':'http://uems.sysu.edu.cn/elect/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        }

        # 进行模拟登陆！  post命令默认参数： data=None，然后加上headers 和 r1请求得到重复利用的cookies项
        r3=requests.post(url3,data=data,headers=headers_Login,cookies=self.r1.cookies)
        pattern=re.search(r'<a href="(.*)" class="btn">',r3.text)
        patternSid=re.search(r'&sid=(.*)',pattern.group(1))
        # SID是正则搜索结果
        self.sid=patternSid.group(1)

        selector=etree.HTML( r3.content)
        self.gb_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_gb)[0]
        self.gx_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_gx)[0]
        self.zb_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_zb)[0]
        self.zx_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_zx)[0]
    #gb,gx,zb,zx=0~3
    def get_course(self,mode):
        sites_list=[self.gb_sites,self.gx_sites,self.zb_sites,self.zx_sites]
        site=sites_list[mode]
        zx_r=requests.get(site,cookies=self.r1.cookies)
        #actually all course_number here
        all_course_number=re.findall(r'courseDet\(\'(\d+)\'',zx_r.content)
        print all_course_number
        #actually all course_name here
        all_course_name=re.findall(r'\">(.*?)</a></td>',zx_r.content)


        patt_string='\''+self.semester+'\'\)\">(.*?)</a></td>'
        patt=re.compile(patt_string)
        selected_quantities=len(re.findall(patt,zx_r.content))
        print 'selected_quantities',selected_quantities
        unselected_course_number=all_course_number[selected_quantities:]
        unselected_course_name=all_course_name[selected_quantities:]
        unselected_quantities=len(unselected_course_number)
        print unselected_quantities+selected_quantities
        #real
        selected_course_number=all_course_number[0:selected_quantities]
        selected_course_name=all_course_name[0:selected_quantities]
        self.selected_course_number=selected_course_number
        self.selected_course_name=selected_course_name
        page_list=zx_r.content.split("<tbody>")

        output0=page_list[0].split('</title>')[0]+"</title>"+"""
        <link rel="stylesheet" type="text/css" href="http://uems.sysu.edu.cn/elect/static/css/site.css" media="all">
	    <link rel="stylesheet" type="text/css" href="http://uems.sysu.edu.cn/elect/static/css/jquery.loadmask.css" media="all">
        """+page_list[0].split('</title>')[1]

        output1=page_list[1]
        # 替换已选的
        for i in range(0,selected_quantities):
            strr1='href=/course/drop/'+selected_course_number[i]+'>'+selected_course_name[i]
            output1=re.sub(r'href=(.*) onclick="courseDet\(\'(\d+)(.*)</a>',strr1,output1,count=1)

        i=0
        output2=page_list[2]

        while i<unselected_quantities:
            strr2='href=/course/select/'+unselected_course_number[i]+'>'+unselected_course_name[i]
            output2=re.sub(r'href=(.*) onclick="courseDet\(\'(\d+)\'\)\"(.*)</a>',strr2,output2,count=1)
            i+=1
        fullpage=output0+"<tbody>"+output1+"<tbody>"+output2
        print 'SUCCESS'
        return fullpage

#####################################################################################
#进入选课结果界面的头
'''
headers_xkjg={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'uems.sysu.edu.cn',
'Referer':'http://uems.sysu.edu.cn/elect/s/types?sid='+sid,
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'}
'''



#输入想要查看的年份和学期
#year=raw_input(u'请输入学年 eg.2014-2015 \n')
#term = raw_input(u'请输入学期 eg.2 \n')

#p1是表单信息,对应的学年和学期，sid值是上面用正则表达式获取的
#p1={'xnd':year,
#'xq':term,
#'sid':sid}

#url4是选课结果页面
#url4='http://uems.sysu.edu.cn/elect/s/courseAll'

#get请求选课结果页面，用headers和一开始进入登陆主界面的cookies
#r4=requests.get(url4,params=p1,headers=headers_xkjg,cookies=r1.cookies)

#实例化清洁工具
#tool=Tool()
#清洁工具清理充满标签的r4.text
#Course_content=tool.replace(r4.text.encode('utf-8'))

#打开文件，写入已清理的内容
#outfile=open(r'C:\ppy\hhhhhhhhh.txt','w')
#outfile.write(Course_content)
#outfile.close()
#print u'目标达成，您的选课结果已经储存'