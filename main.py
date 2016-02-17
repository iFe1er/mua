# -*- coding: utf-8 -*-
''' 采用PIL 和pytesser进行简单的验证码识别
程序包中已经包含了pytesser，但是需要自己安装PIL

使用样例
getverify1('v1.jpg') 返回值为识别出的字符

author：nwpulei@gmail.com
2013-1-1
'''
import sys
from PIL import *
from pytesseract import *
from PIL import ImageEnhance
# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

#由于都是数字
#对于识别成字母的 采用该表进行修正
'''
rep={'O':'0',
    'I':'1','L':'1',
    'Z':'2',
    'S':'8'
    };

'''
class verifyFunction:
    def __init__(self,path):
        self.path=path
        self.threshold = 140
        self.table = []
        for i in range(256):
            if i < self.threshold:
                self.table.append(0)
            else:
                self.table.append(1)

    
    
    def  getverify1(self):
        #打开图片
        im = Image.open(self.path)
        #转化到亮度
        imgry = im.convert('L')
        box = (2,2,66,19)
        region = imgry.crop(box)
        region.save(self.path.split('.')[0]+'g.jpg')
        #二值化
        out = region.point(self.table,'1')
	out.save(self.path.split('.')[0]+'b.jpg')
	nim=out
	enhancer = ImageEnhance.Contrast(nim)
	nim = enhancer.enhance(1)
	nim.save(self.path.split('.')[0]+'b.tif')
        #识别
	text = image_to_string(Image.open(self.path.split('.')[0]+'b.jpg'))
        #识别对吗
        text = text.strip()
        text = text.upper()
        for r in text:
            if r == ']':
                text=text.replace(r,'J')
            elif r ==' ':
                text=text.replace(r,'')
	    elif r=='\n':
		text=text.replace(r,'')
            elif r =='5':
                text=text.replace(r,'S')
            elif r=='0':
                text=text.replace(r,'O')
            elif r =='2':
                text=text.replace(r,'Z')
            elif r=='!':
                text=text.replace(r,'I')
            elif r=='(':
                if text.find('Z')!=-1:
                    text=text.replace('(','')
                    text=text.replace('Z','Q')
                elif text.find('2')!=-1:
                    text=text.replace('(','')
                    text=text.replace('2','Q')
            else:
                continue
        print text
        return text
    
    def  getverify1_2(self):
        #打开图片
        im = Image.open(self.path)
        #转化到亮度
        imgry = im.convert('L')
        box = (4,3,64,18)
        region = imgry.crop(box)
        region.save(self.path.split('.')[0]+'g.jpg')
        #二值化
        out = region.point(self.table,'1')
        out.save(self.path.split('.')[0]+'b.jpg')
        #识别
        text = image_to_string(out)
        #识别对吗
        text = text.strip()
        text = text.upper()
        for r in text:
            if r == ']':
                text=text.replace(r,'J')
            elif r ==' ':
                text=text.replace(r,'')
            elif r =='5':
                text=text.replace(r,'S')
            elif r=='0':
                text=text.replace(r,'O')
            elif r =='2':
                text=text.replace(r,'Z')
            elif r=='!':
                text=text.replace(r,'I')
            elif r=='(':
                if text.find('Z')!=-1:
                    text=text.replace('(','')
                    text=text.replace('Z','Q')
                elif text.find('2')!=-1:
                    text=text.replace('(','')
                    text=text.replace('2','Q')
            else:
                continue
        print 'SUBSTITUDE',text
        return text    


#getverify1('veri.jpg')
#getverify1('v2.jpg')
#getverify1('v3.jpg')
#getverify1('v4.jpg')



    
