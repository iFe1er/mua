#-*- coding: utf-8 -*-
import requests,re
from lxml import etree

def get_jokes_lists():
    r=requests.get('http://lengxiaohua.com/random')
    sel=etree.HTML(r.content)
    first_word_list=sel.xpath('//span[@class="first_char"]/text()')
    joke_list=sel.xpath('//pre[@js="joke_summary"]/text()')
    new_list=map((lambda x,y:x+y),first_word_list,joke_list)

    return new_list
