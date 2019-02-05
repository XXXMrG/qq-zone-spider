#!/usr/bin/env python3
# encoding: utf-8
# 
# 
from  selenium import webdriver
import requests
import time
import os
from urllib import parse
import configparser

class Spider(object):
    def __init__(self):
        self.web=webdriver.Chrome()
        self.web.get('https://user.qzone.qq.com')
        config = configparser.ConfigParser(allow_no_value=False)
        config.read('userinfo.ini')
        self.__username =config.get('qq_info','qq_number')
        self.__password=config.get('qq_info','qq_password')
        self.__list = config.get('get_info', 'qq_list')
        self.headers={
                'host': 'h5.qzone.qq.com',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'connection': 'keep-alive'
        }
        self.req=requests.Session()
        self.cookies={}

    

    def login(self):
        # 去掉注释可以实现自动通过账号密码登录，否则需要手动扫描二维码
        #self.web.switch_to_frame('login_frame')
        # log=self.web.find_element_by_id("switcher_plogin")
        # log.click()
        # time.sleep(1)
        # username=self.web.find_element_by_id('u')
        # username.send_keys(self.__username)
        # ps=self.web.find_element_by_id('p')
        # ps.send_keys(self.__password)
        # btn=self.web.find_element_by_id('login_button')
        # time.sleep(1)
        # btn.click()
        
        self.web.get('https://user.qzone.qq.com/{}'.format(self.__username))
        time.sleep(40)
        cookie=''
        for elem in self.web.get_cookies():
            cookie+=elem["name"]+"="+ elem["value"]+";"
        self.cookies=cookie
        self.get_g_tk()
        self.headers['Cookie']=self.cookies
        self.web.quit()



    # 构造 request 用的 g_tk，根据 qzfl_v8_2.1.61.js 进行密钥构建
    def get_g_tk(self):
        p_skey = self.cookies[self.cookies.find('p_skey=')+7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h=5381
        for i in p_skey:
            h+=(h<<5)+ord(i)
        print('g_tk',h&2147483647)
        self.g_tk=h&2147483647

    def get_mood_url(self):
        url='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
              "sort":0,
                  "start":0,
              "num":20,
            "cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "replynum":100,
              "callback":"_preloadCallback",
              "code_version":1,
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
              "format":"jsonp",
              "need_private_comment":1,
              "g_tk": self.g_tk
              }
        url = url + parse.urlencode(params)
        return url

    def get_mood_detail(self):
        url = self.get_mood_url()
        for qq in eval(self.__list):
            QQ_number = qq
            url_ = url + '&uin=' + str(QQ_number)
            pos = 0
            t = True
            while (t):
                url__ = url_ + '&pos=' + str(pos)
                mood_detail = self.req.get(url=url__, headers=self.headers)
                print(QQ_number,pos)
                if "\"msglist\":null" in mood_detail.text or "\"message\":\"对不起,主人设置了保密,您没有权限查看\"" in mood_detail.text:
                    t = False
                else:
                    if not os.path.exists("./mood_detail/" + str(QQ_number)):
                        os.mkdir("mood_detail/" + str(QQ_number))
                    with open('./mood_detail/'+ str(QQ_number) + "/" + "_" + str(pos) + '.json', 'w',encoding='utf-8') as w:
                        w.write(mood_detail.text)
                    pos += 20
            time.sleep(2)

    def go_next(self):
        self.web.switch_to_frame('app_canvas_frame')
        next = self.web.find_element_by_id('pager_next_0')
        print(next)
        next.click()
        cookie=''
        for elem in self.web.get_cookies():
            cookie+=elem["name"]+"="+ elem["value"]+";"
        self.cookies=cookie


if __name__=='__main__':
    sp=Spider()
    sp.login()
    sp.get_mood_detail()


