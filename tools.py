#coding=utf-8
import os
import re
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import  formataddr

import pymongo
import pymysql
import requests
from lxml import etree
from rest_framework.response import Response
import redis
# 邮箱配置
my_mail = '3210440292@qq.com'
# 授权码
my_pass = 'xbxhxcdlpsmadgga'

# 短信应用SDK AppID
appid = 1400373174   # SDK AppID是1400开头
# 短信应用SDK AppKey
appkey = "7b8eebd19d6600c45333aba5ab62796d"
class My_mysql:
    def __init__(self, path='localhost', port=3306,user='root',password='root',db=None):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    def __enter__(self):
        # 打开文件
        # self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        self.conn = pymysql.connect(host=self.path,port=self.port,user =self.user,password =self.password,db =self.db)
        return self.conn.cursor()

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True
class MyRedis:
    def __init__(self, path='localhost', port='6379'):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port

    def __enter__(self):
        # 打开文件
        self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        # self.conn = pymongo.MongoClient(self.path,self.port)
        return self.conn

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True

class MyMongo:
    def __init__(self, path='localhost', port=27017,db='',table=''):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port
        self.db = db
        self.table = table

    def __enter__(self):
        # 打开文件
        # self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        self.conn = pymongo.MongoClient(self.path,self.port)
        self.db = self.conn[self.db]
        self.table = self.db[self.table]
        return self.table

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True


class Tools(object):
    #  格式化结果集
    def dictfetch(self,cursor):
        # 声明描述符 description 字段名
        desc = cursor.description
        # 重组结果
        return [dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
                ]
    def Send_Mail(self,subject,content,mailladdress):
        # 声明邮件对象
        msg = MIMEText(content,'plain','utf-8')
        # 设置发送方对象
        msg['From']= formataddr(['在线教育平台',my_mail])
        # 设置收件方对象
        msg['To'] = formataddr(['尊敬的客户',mailladdress])
        # 设置标题
        msg['Subject'] = subject
        # 设置smtp服务器
        server = smtplib.SMTP_SSL(host='smtp.qq.com',port=465)
        # 登录邮箱
        server.login(my_mail,my_pass)
        # 发送文件
        server.sendmail(my_mail,[mailladdress],msg.as_string())
        # 关闭smtp链接
        server.quit()

    def md5_str(self,my_str):
        from hashlib import md5
        my_str=str(my_str).encode(encoding='utf-8')
        code= md5(my_str).hexdigest()
        return code
    def encode_jwt_str(self,my_dict):
        import datetime
        import jwt
        payload = {
            'exp': int((datetime.datetime.now() + datetime.timedelta(hours=4)).timestamp()),
            'data': my_dict
        }
        encode_jwt = jwt.encode(payload, key='201528', algorithm='HS256')
        encode_str = str(encode_jwt, 'utf-8')
        return encode_str
    def decode_jwt_str(self,jwt_str):
        import jwt
        try:
            decode_jwt = jwt.decode(jwt_str, key='201528', algorithms=['HS256'])
            if decode_jwt:
                return decode_jwt
        except Exception as e:
            print(e)
            return False
        # 发短信
    def Send_Messgae(self,phone_num,code,min=0):
        # 需要发送短信的手机号码
        phone_numbers = [phone_num]
        # 短信模板ID，需要在短信应用中申请
        template_id = 614434
        # 签名
        sms_sign = "刘悦的技术博客"

        from qcloudsms_py import SmsSingleSender
        from qcloudsms_py.httpclient import HTTPError

        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

        ssender = SmsSingleSender(appid, appkey)
        params = [code, min]  # 当模板没有参数时，`params = []`
        try:
            result = ssender.send_with_param(86, phone_numbers[0],
                                             template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数不允许为空串
            print(result)
            print(dict(result)['errmsg'])
            return dict(result)
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

    def xTree(self,datas):
        lists = []
        tree = {}
        parent_id = ''
        for i in datas:
            item = i
            tree[item['id']] = item
        root = None
        for i in datas:
            obj = i
            if not obj['pid']:
                root = tree[obj['id']]
                lists.append(root)
            else:
                parent_id = obj['pid']
                if 'childlist' not in tree[parent_id]:
                    tree[parent_id]['childlist'] = []
                tree[parent_id]['childlist'].append(tree[obj['id']])
        return lists

    # # 定义权限检测装饰器
    # def my_decorator(self,func):
    #     def warpper(request, *args, **kwargs):
    #         # 如果get请求不到
    #         if request.GET.get('jwt', None):
    #             jwt = request.GET.get('jwt', None)
    #         else:
    #             jwt = request.POST.get('jwt', None)
    #         # 解密jwt
    #         ret = self.decode_jwt_str(jwt)
    #         if not ret:
    #             return Response({'code': 403, 'msg': 'jwt失效'})
    #         # 查询用户所属的角色
    #         role = Role.objects.get(pk=ret['data']['rid'])
    #         # 判断所诉角色的资格
    #         if 'super_user' in request.path_info and role.id != 3:
    #             return Response({'code': 403, 'msg': '该用户没有权限'})
    #         elif 'add_course' in request.path_info and role.id!= 4:
    #             return Response({'code': 403, 'msg': '该用户没有权限'})
    #         # elif 'show_category' in request.path_info and role.id!= 5:
    #         #     return Response({'code': 403, 'msg': '该用户没有权限'})
    #         # 如果这个角色的权限 没有这个请求的权限
    #         alist = Role_Middle_Authority.objects.filter(rid=ret['data']['rid']).all()
    #         method_list = []
    #         for i in alist:
    #             method_list.append(Authority.objects.get(pk=i.Aid).name)
    #         if request.method not in method_list:
    #             return Response({'code': 403, 'msg': '该用户没有权限'})
    #         return func(request, *args, **kwargs)
    #     return warpper
    # 纠正词语
    def correct_text(self,text):
        from aip import AipNlp
        app_id = '20241605'
        app_key = 'wysngaXktvdUH5odSMKmnjTx'
        app_secret = 'utpC3dHTUAHMdRn71HxvXS8InMFHpmXM'
        client = AipNlp(app_id, app_key, app_secret)
        print(client.ecnet(text))
        return client.ecnet(text)['item']['correct_query']
    # 情感分析
    def emotion_text(self,text):
        from aip import AipNlp
        app_id = '20241605'
        app_key = 'wysngaXktvdUH5odSMKmnjTx'
        app_secret = 'utpC3dHTUAHMdRn71HxvXS8InMFHpmXM'
        client = AipNlp(app_id, app_key, app_secret)
        return client.sentimentClassify(text)['items'][0]['sentiment']

    def filter_tags(self,htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后entity,如>为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr
    def up_file(self,uploader,index,value,maxnum):
        print(index,maxnum,'\n')
        # 上传文件块
        uploader.upload(index, value)
        # if index ==maxnum:
        #     res = uploader.complete()

    def robot_send_msg(self,place,msg):
        import time
        import hmac
        import hashlib
        import base64
        import urllib.parse

        timestamp = str(round(time.time() * 1000))
        # secret = 'SECb5af2ae8030a377b02a9d75171a4a7d3ae5998dc7b2cfaad2383410318766243'
        secret = 'SEC575ce17d343c24992d3b04277f6805ab2b5b1f09a876f0be6f6d7efb0719cffa'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote(base64.b64encode(hmac_code))
        import requests, json  # 导入依赖库
        headers = {'Content-Type': 'application/json'}  # 定义数据类型
        # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=97278eb277475dc83fbabf4d97fe08fd846f5786934c2c98e8a69a9dd4d38e1d&timestamp=' + timestamp + "&sign=" + sign
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token=372c7da9a628572e9aa1281a6011cb4bcd42a503e85ab67625c247171862ffd2&timestamp=' + timestamp + "&sign=" + sign
        # data = {
        #     "msgtype": "text",
        #     "text": {"content": msg},
        #     "isAtAll": True}
        data={
            "msgtype": "markdown",
            "markdown": {
                "title": "%s天气"%place,
                "text": msg
            },
            "at": {
                "isAtAll": True
            }
        }
        res = requests.post(webhook, data=json.dumps(data), headers=headers)  # 发送post请求
        if res.json()['errcode'] == 0:
            return res.json()['errmsg']
        else:
            return res.json()['errmsg']

    #
    # def get_url(self):
    #     url = 'http://tianqi.sogou.com/pc/weather/57670'
    #     import upyun
    #     from selenium import webdriver
    #     from selenium.webdriver.chrome.options import Options
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument('window-size=1920x1080')  # 虚拟屏幕大小
    #     browser = webdriver.Chrome(options=chrome_options)
    #     browser.get(url)
    #     ul = browser.find_element_by_class_name('r-weather')
    #     time.sleep(2)
    #     img_path = os.path.join(BASE_DIR, "static/test.png")
    #     ul.screenshot(img_path)
    #     up = upyun.UpYun('mdsave', 'ljq', 'm3QsiAaLhMvB8owYEwdl1l2atviBVF3U')
    #     headers = {'x-gmkerl-quality': '90'}
    #     with open(img_path, 'rb')as f:
    #         res = up.put('test.png', f.read(), headers)
    #     img_url = 'http://mdsave.test.upcdn.net/test.png'
    #     return img_url, browser.page_source
    #
    # def get_temperature(self):
    #     img_url, html = self.get_url()
    #     tree = etree.HTML(html)
    #     place = tree.xpath('//em[@class="city-name"]/text()')[0]
    #     # 获取温度
    #     temperature = "**" + tree.xpath('//span[@class="num"]/text()')[0] + "°**" + \
    #                   tree.xpath('//div[@class="r1-img"]/p/text()')[0]
    #     time = "[%s](%s)" % (tree.xpath('///a[@class="date"]/text()')[0].replace(" ", "").replace("\n", ""),
    #                          tree.xpath('///a[@class="date"]/@href')[0])
    #     # 状态
    #     condition = "".join(tree.xpath('//p[@class="condition"]//text()')).replace("\n", "").replace(" ", "")
    #     quality = "".join(tree.xpath('//p[@class="livindex"]//text()')).replace("\n", "").replace(" ", "")
    #     sand_time = tree.xpath('//div[@class="row4"]/p/text()')[0]
    #     msg = '#### 当前位置：%s\n>目前温度：%s <br>\n>%s\n>%s\n>%s  \n>![test.png](%s)\n###### %s' % (
    #         place, temperature, time, condition, quality, img_url, sand_time)
    #     return place, msg

mytool = Tools()

'#### 杭州天气 @150XXXXXXXX \n> 9度，西北风1级，空气良89，相对温度73%\n> ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n> ###### 10点20分发布 [天气](https://www.dingalk.com) \n'
# print(mytool.emotion_text('快手百度抖音'))
# html='<p><span style="color: rgb(74, 74, 74);">&nbsp;&nbsp;2010年，谷歌正式退出中国市场，无数人扼腕叹息，如今十年过去了，谷歌还有两条重要的业务线并没有完全退出，一个是页面统计业务(Google Analytics)，另外一个则是谷歌广告联盟(Google Adsense)，说起广告联盟，玩儿过网站的朋友应该并不陌生，对于中小型站长、博主来说，要想通过网站的流量取得一些收入，除了和一些线下线上厂商谈包月广告位，更多的可能就是投放广告联盟广告了。但随着网络广告的不断发展，广告形式有了很大的变化，出现了CPC、CPS、CPA、CPV等众多广告类型。</span></p>'
# print(mytool.filter_tags(html))
# mytool.Send_Messgae('18568418146','1234',2)

# str = "{'result': 0, 'errmsg': 'OK', 'ext': '', 'sid': '2104:45191106015907157627466624', 'fee': 1}"

