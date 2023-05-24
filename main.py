import random
import urllib.parse
import time
import os

import requests
import urllib.parse
import json


class Data_Operation:
    """
    Do:
        操作 json 里面的数据，完成读取或者写入，包含追加写入、读取两个功能
    Arguments:
        name: json 文件中的字段名
        value: json 文件中的字段值
    Returns:
        None
    """

    def __init__(self, name, value): # 初始化两个参数 name 和 value
        self.name = name
        self.value = value

    def zhuijia(self):
        # 给 json 文件中写入数据
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 追加 token 字段
        data[self.name] = self.value

        # 将新的数据写入文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def duqu(self):
        # 在 json 文件中读取数据
        with open('data.json', "r") as f:
            data_dict = json.load(f)
        # 将数据打包为一个元组并返回
        return data_dict[self.name]


class Id_SMS_Phone_Get:
    """
    Do:
        获取用户手机号，验证码以及充电账户的 ID
    """
    def __init__(self, phone, smsche):
        self.phone = phone
        self.smsche = smsche

    def Send_VerificationCode(self):
        """
        Do:
            发送验证码,参数分别是手机号和区号。不知道是不是区号，反正无论填写啥都能发验证码
        Arguments:
            phone: 手机号
        """
        url = 'http://cdz.gpsserver.cn/WpassSmsArea'

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': 'UArealanstr=zh; AppUAreab_mode=0; jzmm=true; GetRfSimfalg=0; pageitem=0; dma=912492; JSESSIONID=3336BCEAF84C4FA374B2D5; uUser=o6rmujo6KwZzm3qhqon_o_10; AppName=%u7535%u52A8%u81EA%u884C%u8F66%u667A%u80FD%u5145%u7535%u7CFB%u7EDF',
            'DNT': '1',
            'Host': 'cdz.gpsserver.cn',
            'Origin': 'http://cdz.gpsserver.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://cdz.gpsserver.cn/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }

        payload = {
            'utel': self.phone,
            'area': '10'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()

            result = response.json()
            print(result)
            if result[0]['par'] == 'succeed':
                return '验证码发送成功'
            else:
                return '验证码发送失败'
        except requests.exceptions.RequestException as e:
            return f"请求出错：{e}"

    def Get_Uuser(self):
        """
        Do:
            通过短信验证码获取到最长的 uuser
        Arguments:
            phone: 手机号
            smsche: 短信验证码
        Returns:
            max_uuser: 最长的 uuser 
        """
        url = 'http://cdz.gpsserver.cn/LoginSms'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': 'UArealanstr=zh; AppUAreab_mode=0; jzmm=true; GetRfSimfalg=0; pageitem=0; uUser=tong; dma=991013; '
                      'JSESSIONID=3336BCEA0013941ECAF84C4FA374B2D5; AppName=%u4E91%u4EAB%u5145%u7535',
            'DNT': '1',
            'Host': 'cdz.gpsserver.cn',
            'Origin': 'http://cdz.gpsserver.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://cdz.gpsserver.cn/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/112.0.0.0 Safari/537.36'
        }
        data = {
            'utel': self.phone,
            'smsche': self.smsche,
            'uUser[isTrusted]': 'true'
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            # last_uuser = json_data[len(json_data) - 1]['uUser']
            # 首先将所有 uUser 的值提取出来放到列表里
            uuser_list = [item['uUser'] for item in json_data]
            # 找到最长的 uUser
            max_uuser = max(uuser_list, key=len)
            return max_uuser
        except requests.exceptions.Timeout:
            return "请求超时"
        except requests.exceptions.RequestException as e:
            return f"请求出错：{e}"
        except (ValueError, KeyError):
            return "响应数据解析失败"


def Print_Separator():
    """
    Do:
        打印分割线
    """
    separator = '*' * 20 + ' 分割线 ' + '*' * 20
    print(separator)


class Qing_QiuXiang_Guan:

    # 第二个主程序
    def GetCurrentTimeStamp(self):
        """
        获取当前时间戳，主要是为了构造请求头部，获取随机时间。伪造请求头部的时间戳，防止被服务器拒绝。
        """
        timestamp = int(time.time() * 1000)
        return str(timestamp)

    def GetRandomUserAgent(self):
        """
        随机获取一个 User-Agent
        :return:
        """
        USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
        ]

        return random.choice(USER_AGENTS)

    def GetRandomReferer(self):  # 随机获取一个 Referer，主要就是为了看你这个页面是从哪里请求过去的
        Referer = [
            'http://cdz.gpsserver.cn/wxhtml/login.html',
            'http://cdz.gpsserver.cn/wxhtml/ChargeCarsys/ChargeCarsys.html?gtel=18560001771_0&b_yy=1'
        ]
        return random.choice(Referer)

    def GetRandomAcceptLanguage(self):  # 随机获取一个 Accept-Language
        ACCEPT_LANGUAGES = [
            'zh-CN,zh;q=0.9',
            'en-US;q=0.8,en;q=0.7',
            'ja-JP;q=0.9,ja;q=0.8',
        ]

        return random.choice(ACCEPT_LANGUAGES)


class Send_Messages:
    """
    Do:
        发送消息，两个渠道，一个是微信，一个是 Bark。
        选择其中一个使用即可
    Args:
        WXToken: PushPlus 的 Token
        WXContent: PushPlus 的消息内容
        BarkText: Bark 的消息内容
    """
    def __init__(self, WXToken, WXContent, BarkText):
        self.WXToken = WXToken
        self.WXContent = WXContent
        self.BarkText = BarkText

    def WXSeng(self):
        # 对消息内容进行 UrlEncode 编码
        content = urllib.parse.quote(self.WXContent)

        url = f'http://www.pushplus.plus/send?token={self.WXToken}&content={self.WXContent}'

        res = requests.get(url)
        if res.status_code == 200:
            print('PushPlus 消息发送成功！')
        else:
            print(f'PushPlus 消息发送失败，错误代码：{res.status_code}')

    def BarkIOS(self):
        url = f'https://api.day.app/M5y4fu4kwn6QmSrXhHRS7o/{self.BarkText}'
        response = requests.get(url)

        if response.status_code == 200:
            print('请求成功！')
        else:
            print(f'请求失败，错误代码：{response.status_code}')


class Find_And_Appointment:
    """
    Do:
        查找充电桩并预约
    Args:
        usr: 用户名
        pwd: 密码
    """

    def __init__(self, usr, pwd):
        self.usr = usr
        self.pwd = pwd

    def Find_Charging_Stations(self):
        """
        Do:
            查找充电桩状态，如果找到了并返回第一个空闲的充电桩信息
        Args:
            None
        Returns:
            mc: 充电桩地址
            gtel: 充电桩编号
            i: 充电桩编号
        Steps:
            1. 调用 API 获取充电桩列表。
            2. 遍历充电桩列表，查找第一个状态是空闲的充 电桩。
            3. 如果找到空闲充电桩，则返回该充电桩的信息。否则继续查询。
        """

        api_list = [
            # 'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001038', # 4 号楼
            'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001037',
            'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560002140',
            # 'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001771'  # 老校区
        ]
        find_times = 1

        while True:  # 循环查询充电桩状态
            print(f"第{find_times}轮查询")
            if find_times == 50:
                break
            for api in api_list:
                print('正在查询：', api)
                response = requests.get(api)
                data = json.loads(response.text)[0] # 将返回的 json 数据转换为字典
                mc = data['mc']  # 充电桩地址
                dz = data['dz']
                gtel = data['gtel']  # 充电桩编号
                print(f"{mc} {dz} {gtel}")
                glzt_list = [data[f'glzt{i}'] for i in range(1, 21)]
                for i, glzt in enumerate(glzt_list):
                    if glzt == '0':  # 找到第一个状态为 0 的充电桩
                        print('找到了')
                        return mc, gtel, i + 1
                    
                time.sleep(2)  # 每次查询之后等待1秒
            time.sleep(30)  # 每轮查询之后等待5分钟
            find_times += 1
            Print_Separator() # 打印分隔符
        return None, None, None    

    def Start_Appointment(self):
        """
            开始预约充电，执行充电预约程序。
            完成账户登录之后获取 cookie ，然后构造预约充电的请求头部，发送预约请求。
        Arguments:
            gtel: 充电桩编号, i: 充电桩编号, usr: 用户名, pwd: 密码
        Returns:
            None  直接打印预约成功与否的信息
        step:
            1. 构造请求头部
            2. 发送 POST 请求， 开始登录， 之后登陆成功获取cookie
            3. 构造预约充电的请求头部
            4. 发送 POST 请求，开始预约充电
            5. 打印预约成功与否的信息
        """
        
        mc, gtel, i = self.Find_Charging_Stations()

        qingqiuxiangguan = Qing_QiuXiang_Guan()  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
        # 传入到下面的 POST 请求中
        headers = {
            
            'Host': 'cdz.gpsserver.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': qingqiuxiangguan.GetRandomAcceptLanguage(),
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://cdz.gpsserver.cn',
            'User-Agent': qingqiuxiangguan.GetRandomUserAgent(),
            'Connection': 'keep-alive',
            'Referer': qingqiuxiangguan.GetRandomReferer(),
        }
        # 发送 POST 请求，开始登录
        data = {
            'uUser': self.usr,
            'dma': self.pwd,
            'openid': ''
        }
        response = requests.post('http://cdz.gpsserver.cn/Login', headers=headers, data=data)
        print(response.json())
        # 从响应头部中获取 Cookie
        cookie = response.headers.get('Set-Cookie')

        # 构建请求头部，开始预约
        if cookie is not None: # 如果 cookie 不为空，则构建请求头部, 因为headers里面没有定义cookie这个键值
            headers['Cookie'] = cookie
        data = {
            'b_cmzt': '0',
            'gtel': gtel,
            'td': i,
            'b_yy': '1',
            'sjtime': qingqiuxiangguan.GetCurrentTimeStamp()
        }
        response = requests.post('http://cdz.gpsserver.cn/CcdSJ', headers=headers, data=data)
        # 开始预约并返回预约结果
        if response.json()[0]['par'] == 'succeed':
            print('预约成功')
            BackMessage = '已为你抢到充电位置：', '地址是：', mc, '充电桩编号是：', i, '请打开公众号点击开始充电'
            BackMessage = str(BackMessage)
            # 以下是微信推送
            # do = DataOperation("token", None)
            # token = do.duqu()
            # sendmessages = SendMessages(token, BackMessage, None)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数。前面是微信的调用参数，后面是Bark的调用参数
            # sendmessages.WXSeng()

            # 以下是Bark推送
            sendmessages = Send_Messages(None, None, BackMessage)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数。前面是微信的调用参数，后面是Bark的调用参数
            sendmessages.BarkIOS()

        elif response.json()[0]['par'] == 'err_gnoreg':
            print('预约失败')
        else:
            print('预约失败，请检查密码是否正确')


def main():
    # 初始化，先判断是否本地是否有 data.json 文件，如果没有则创建一个
    if not os.path.isfile('data.json'):
        data = {
            "account": "",
            "user": "",
            "password": "",
            "token": "",
        }

        with open('data.json', 'w') as f:
            json.dump(data, f)

        Print_Separator()
        print('你现在是第一次使用，需要进行一些初始化操作....,两秒钟后开始初始化')
        time.sleep(2)

        Print_Separator()
        print('请打开网址关注公众号后，输入你的 token，记住关闭公众号的免打扰，否则收不到预约信息：https://www.pushplus.plus/push1.html')
        YourToekn = input('请输入你的 token，例如：3b0e5f6558eXXXXXXXX7e6a5292，然后按回车键，请输入：')

        do = Data_Operation('token', YourToekn)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
        do.zhuijia()
        # 微信公众号提醒信息操作完毕

        Print_Separator()
        phone = input('输入手机号后按回车键继续：')

        po = Id_SMS_Phone_Get(phone, '')  # 实例化，传入手机号和验证码，但是我们必须先使用 PowerOperition 下面的
        # SendVerificationCode才能有验证码，怎么办呢，我们可以先传入一个空的验证码，然后再调用 PowerOperition 下面的 SendVerificationCode 方法，这样就可以获取到验证码了
        po.Send_VerificationCode()  # 调用 PowerOperition 下面的 SendVerificationCode 方法，这样就可以获取到验证码了
        # 这里不需要传入参数，因为po已经有了phone和smsche，即使smsche是空的，也不影响
        Print_Separator()
        print('验证码已发送，请注意查收！')

        Print_Separator()
        ReceiveCode = input('输入验证码后按回车键继续：')
        # 接下来把用户输入的验证码传入 GetUuser方法中
        po = Id_SMS_Phone_Get(phone, ReceiveCode)  # 实例化，传入手机号和验证码
        Login = po.Get_Uuser()  # 调用 PowerOperition 下面的 GetUuser 方法，这样就可以获取到登陆标识符了

        Print_Separator()
        print(f'账号：{phone}，登陆标识符：{Login}')
        Print_Separator()
        print(
            '请在下面网址输入你的登陆标识符进行密码修改：http://cdz.gpsserver.cn/wxhtml/USearch/USearchdma.html?openid=&area=')
        PassWord = input('输入你修改后的密码————后按回车键继续：')
        Print_Separator()
        print('正在写入数据库，请稍等……')

        # 实例化一个对象，用来调用其他类的方法，name 是 account，phone 是 value
        dp = Data_Operation('account', phone)
        # 调用 DataOperation 下面的 zhuijia 方法，zhuijia 里面需要两个参数，一个是 name，一个是 value
        dp.zhuijia()

        dp = Data_Operation('user', Login)
        dp.zhuijia()

        dp = Data_Operation('password', PassWord)
        dp.zhuijia()

        print(f'账号：{phone}，登陆标识符：{Login}，密码：{PassWord},已写入数据库！')
        Print_Separator()
        print('写入完成，新用户信息配置成功，两秒钟后启动充电预约程序')
        time.sleep(2)

    # 开始查找空闲的充电桩
    # findandappointment = FindAndAppointment(None, None)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
    # findandappointment.FindChargingStations()

    # 如果找到之后，那就开始从数据库读取用户保存的信息，使用该用户的信息进行预约
    do = Data_Operation('user', None)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
    usr = do.duqu()
    do = Data_Operation('password', None)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
    pw = do.duqu()

    # 开始执行预约程序
    Print_Separator()
    findandappointment = Find_And_Appointment(usr, pw)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数
    findandappointment.Start_Appointment()


def handler(event, context):
    # 微信发送
    # do = DataOperation("token", None)
    # token = do.duqu()
    # sendmessages = SendMessages(token, '系统初始化完毕，任务：找到充电器并自动预约，查找系统已经运行成功！！！',
    #                             None)  # 实例化一个对象，用来调用其他类的方法，把获取到的参数。前面是微信的调用参数，后面是Bark的调用参数
    # sendmessages.WXSeng()

    # Bark发送
    sendmessages = Send_Messages(None, None,
                                '系统初始化完毕，任务：找到充电器并自动预约，查找系统已经运行成功！！！')  # 实例化一个对象，用来调用其他类的方法，把获取到的参数。前面是微信的调用参数，后面是Bark的调用参数
    sendmessages.BarkIOS()

    main()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
    }


if __name__ == '__main__':
    handler(None, None)
