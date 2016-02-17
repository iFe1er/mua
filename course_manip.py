#coding:utf-8
import requests
from lxml import etree
import re
class course_manip:
    def __init__(self,sid,cookies):
        self.drop_url='http://uems.sysu.edu.cn/elect/s/unelect'
        self.select_url='http://uems.sysu.edu.cn/elect/s/elect'
        self.sid=sid
        self.cookies=cookies
        self.univerisal_headers={
        'Host': 'uems.sysu.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'Accept': '*/*',
        'Origin': 'http://uems.sysu.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://uems.sysu.edu.cn/elect/s/courses?kclb=21&xnd=2015-2016&xq=3&fromSearch=false&sid='+self.sid,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'JSESSIONID='+cookies
        }
    #giving a number of course, drop it
    def drop_course(self, jxbh):
        data={
        'jxbh':jxbh,'sid':self.sid
        }
        try:
            requests.post(self.drop_url,data=data,headers=self.univerisal_headers,timeout=10)
            print 'DROP SUCCESS'
            return 1
        except:
            return 0
    #giving a number of course, select it
    def select_course(self, jxbh):
        data={
        'jxbh':jxbh,'sid':self.sid
        }
        try:
            requests.post(self.select_url,data=data,headers=self.univerisal_headers,timeout=10)
            print 'SELECT SUCCESS'
            if requests.status_code=='200':
                return 1
            else:
                return 0
        except:
            return 0

    def get_selected_course_unselected_course_unselected_empty(self, mode):
        self.semester='3'
        url='http://uems.sysu.edu.cn/elect/s/types?sid='+self.sid
        self.r=requests.get(url,headers=self.univerisal_headers)
        selector=etree.HTML(self.r.content)
        xpath_gb='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[2]/a/@href'
        xpath_gx='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td[2]/a/@href'
        xpath_zb='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td[2]/a/@href'
        xpath_zx='//*[@id="content"]/div[1]/div[1]/div[1]/table/tbody/tr[4]/td[2]/a/@href'
        self.gb_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_gb)[0]
        self.gx_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_gx)[0]
        self.zb_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_zb)[0]
        self.zx_sites="http://uems.sysu.edu.cn/elect/s/"+selector.xpath(xpath_zx)[0]

        sites_list=[self.gb_sites,self.gx_sites,self.zb_sites,self.zx_sites]
        site=sites_list[mode]
        #具体的选课页面:
        zx_r=requests.get(site,headers=self.univerisal_headers)
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
        print 'total_quantities:',unselected_quantities+selected_quantities
        #real
        selected_course_number=all_course_number[0:selected_quantities]
        selected_course_name=all_course_name[0:selected_quantities]
        self.selected_course_number=selected_course_number
        self.selected_course_name=selected_course_name

        sel=etree.HTML(zx_r.content)
        unselected_course_empty=sel.xpath('//*[@id="courses"]/tbody/tr/td[8]/text()')
        result={
            'selected_course_number':selected_course_number,
            'unselected_course_number':unselected_course_number,
            'unselected_course_empty':unselected_course_empty
        }
        print result
        return result


'''

    univerisal_headers={
    'Host': 'uems.sysu.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '60',
    'Accept': '*/*',
    'Origin': 'http://uems.sysu.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://uems.sysu.edu.cn/elect/s/courses?kclb=21&xnd=2015-2016&xq=3&fromSearch=false&sid=3e18b6f3-885e-4030-8516-d72cf105fd6f',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    
    data={
    'jxbh':jxbh,'sid':sid
    }
    try:
        requests.post(select_url,data=data,headers=univerisal_headers,cookies=cookies,timeout=10)
        print 'ELECT SUCCESS'
        return 1
    except:
        return 0

if __name__=='__main__':
    pass



POST http://uems.sysu.edu.cn/elect/s/elect HTTP/1.1
Host: uems.sysu.edu.cn
Connection: keep-alive
Content-Length: 60
Accept: */*
Origin: http://uems.sysu.edu.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://uems.sysu.edu.cn/elect/s/courses?kclb=21&xqm=4&sort=&ord=&xnd=2015-2016&xq=3&sid=3e18b6f3-885e-4030-8516-d72cf105fd6f&conflict=&blank=&hides=&fromSearch=false&kcmc=&sjdd=&kkdw=&rkjs=&skyz=&xf1=&xf2=&sfbyb=
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: JSESSIONID=455BD1C7F3D6D742B755546B09B8AD3D; safedog-flow-item=076B2E5146A03E38FD630EFA70AFA405

post data:
jxbh=35000184153001&sid=3e18b6f3-885e-4030-8516-d72cf105fd6f
'''