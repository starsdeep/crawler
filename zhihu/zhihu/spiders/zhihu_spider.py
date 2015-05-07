#encoding=utf8
__author__ = 'starsdeep'

import sys,os
reload(sys)
sys.setdefaultencoding('UTF8')
import scrapy
from scrapy.http import Request,FormRequest
from scrapy.selector import Selector
from collections import defaultdict
import json
from selenium import webdriver
import ConfigParser
import requests
from scrapy import log
import time,datetime
from zhihu import settings
from zhihu.items import ZhihuTopicItem
import json


import logging
from scrapy.log import ScrapyFileLogObserver


def create_session():
    global session
    global cookies
    cf = ConfigParser.ConfigParser()
    cf.read("./zhihu/spiders/config.ini")
    cookies = cf._sections['cookies']

    email = cf.get("info", "email")
    password = cf.get("info", "password")
    cookies = dict(cookies)

    s = requests.session()
    login_data = {"email": email, "password": password}
    header = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
        'Host': "www.zhihu.com",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }

    r = s.post('http://www.zhihu.com/login', data=login_data, headers=header)

    if r.json()["r"] == 1:
        print "Login Failed, reason is:"
        for m in r.json()["msg"]:
            print r.json()["msg"][m]
        print "Use cookies"
        has_cookies = False
        for key in cookies:
            if key != '__name__' and cookies[key] != '':
                has_cookies = True
                break
        if has_cookies == False:
            raise ValueError("请填写config.ini文件中的cookies项.")
    return s, cookies






class PeopleSpider(scrapy.Spider):

    name = 'zhihu_topic'
    start_urls = []
    #r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
    #r_local = redis.StrictRedis(host='localhost', port=settings.REDIS_LOCAL_PORT, db=0)
    driver = None

    def __init__(self):
        #log.start(logfile=time.strftime("log/%Y%m%d%H%M%S")+".log", logstdout=False)
        #log.start(logfile='log/testlog.log', logstdout=False)
        logfile = open('log/testlog.log', 'w')
        log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
        log_observer.start()

        log.msg("initiating crawler...",level=log.INFO)
        chromedriver = "/Users/starsdeep/tools/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        self.username = '695321146@qq.com'
        self.password = 'cq314159'



    def start_requests(self):
        self.driver.get(settings.LOGIN_URL)
        u = self.driver.find_element_by_name("email")
        p = self.driver.find_element_by_name("password")
        u.clear()
        u.send_keys(self.username)
        p.clear()
        p.send_keys(self.password)
        u.submit()
        print "already submitted, waiting to login "
        time.sleep(settings.UNTRACABLE_REQUEST_WAIT)
        print "wait time expired, the current url is: " + self.driver.current_url

        if self.driver.current_url == settings.LOGIN_URL:
            log.msg("login failed, investigating...",level=log.ERROR)
            sys.exit()

        else:
            self.parse_root()

    def parse_root(self):
        root_topic_url = 'http://www.zhihu.com/topic/19776749/organize/entire'
        self.driver.get(root_topic_url)
        #child_topic_list_xpath = '//*[@id="zh-topic-organize-page-children"]/ul/li/ul'
        child_topic_list_xpath = '//*[@id="zh-topic-organize-page-children"]/ul/li/ul/li/a'
        elements = self.driver.find_elements_by_xpath(child_topic_list_xpath)

        item = ZhihuTopicItem()
        item['layer'] = '0'
        item['id'] = '19776749'
        item['name'] = '根话题'
        item['parent_id'] = '0'
        item['child_ids'] = list()
        
        topic_names = list()
         #根话题
        for child in elements:
            item['child_ids'].append(child.get_attribute('data-token'))
            topic_names.append(topic_name = child.text)
            #print topic_name
            #print id
        yield item

        

    def parse_topic_page(self, layer_num, parent_topic_id, topic_id):
        url = 'http://www.zhihu.com/topic/' + topic_id + '/organize/entire'
        self.driver.get(url)

        child_topic_list_xpath = '//*[@id="zh-topic-organize-page-children"]/ul/li/ul/li/a'
        items = self.driver.find_elements_by_xpath(child_topic_list_xpath)

        if items.size()==0:
            return

        load_num = 0
        while True:
            load_more = self.driver.find_element_by_name('load')
            try:
                next.click()
                load_num += 1
                # get the data and write it to scrapy items
            except:
                break

        print "topic: " + topic_id + " load time is " + str(load_num)

        for child in items:
            id = child.get_attribute('data-token')
            topic_name = child.text
            topic_id_dict[topic_name] = id
            topic_tree['19776749'].append(id)
            print topic_name
            print id





        '''
        #一级话题
        for id in topic_tree['19776749']:
            url = 'http://www.zhihu.com/topic/' + id + '/organize/entire'
            self.driver.get(url)
            with open('test.html','w') as of:
                of.write(self.driver.page_source)


# class ZhihuTopicSpider(scrapy.Spider):
#
#     name = "zhihu_topic"
#     allowed_domains = ["zhihu.com"]
#     start_urls = []
#
#     def __init__(self):
#         chromedriver = "/Users/starsdeep/tools/chromedriver"
#         os.environ["webdriver.chrome.driver"] = chromedriver
#         self.driver = webdriver.Chrome(chromedriver)
#         self.session = None
#         self.cookies = dict()
#         self.session, self.cookies = create_session()
#
#
#     def start_requests(self):
#         root_topic_url = 'http://www.zhihu.com/topic/19776749/organize/entire'
#         self.driver.get(root_topic_url)
#         with open('test.html','w') as of:
#             of.write(self.driver.page_source)
#         sys.exit()
#         #response = self.session.get(root_topic_url, cookies=self.cookies)
#         #with open('test.html', 'w') as of:
#         #    of.write(response.content)
#
#
#
#     def get_topics(self):
#         topics = []
#         infile = open('./')
#
#     # def start_requests(self):
#     #     return [FormRequest(
#     #         "http://www.zhihu.com/login",
#     #         formdata = {'email':'695321146@qq.com',
#     #                     'password':'cq314159'
#     #         },
#     #         callback = self.after_login
#     #     )]
#
#     '''
#     def start_requests(self):
#         self.driver.get('http://www.zhihu.com/#signin')
#         username = self.driver.find_element_by_name('email')
#         password = self.driver.find_element_by_name('password')
#         _xsrf = self.driver.find_element_by_name('_xsrf')
#
#
#         username.send_keys('695321146@qq.com')
#         password.send_keys('cq314159')
#         _xsrf.send_keys('7393afb8e85366db69b79d231eb49227')
#
#         self.driver.find_element_by_class_name('sign-button').click()
#         #after singin
#         root_topic_url = 'http://www.zhihu.com/topic/19776749/organize/entire'
#
#         self.driver.get(root_topic_url)
#         with open('test.html','w') as of:
#             of.write(self.driver.page_source)
#
#         print "############# what happened11111 ############"
#         sys.exit()
#     '''
#
#     def after_login(self, response):
#         root_topic_url = 'http://www.zhihu.com/topic/19776749/organize/entire'
#
#         self.driver.get(root_topic_url)
#         with open('test.html','w') as of:
#             of.write(self.driver.page_source)
#
#         print "############# what happened11111 ############"
#         sys.exit()
#         yield Request(root_topic_url, callback = self.parse_root)
#
#
#     def parse_root(self, response):
#         print "############# what happened ############"
#         with open('test.html','w') as of:
#             of.write(response.body)
#         #print response.body
#         sel = Selector(response)
#         child_topic_list_xpath = '//*[@id="zh-topic-side-children-list"]/div/div/a'
#
#         #根话题
#         topic_id_dict = dict()
#         topic_tree = defaultdict(list)
#         layer1_urls = list()
#         for child in sel.xpath(child_topic_list_xpath):
#             id = child.xpath('@data-token').extract()[0]
#             topic_name = child.xpath('text()').extract()[0] #unicode
#             topic_id_dict[topic_name] = id
#             topic_tree['19776749'].append(id)
#
#         '''
#         #一级话题
#         for id in topic_tree['19776749']:
#             url = 'http://www.zhihu.com/topic/' + id + '/organize/entire'
#             self.driver.get(url)
#             with open('test.html','w') as of:
#                 of.write(self.driver.page_source)
#
#         '''













