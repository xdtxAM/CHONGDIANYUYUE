import requests
import json
import time
import random
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

def send_email(receiver, mail_content):
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '1035917380'
    # pwd为qq邮箱的授权码
    pwd = 'XXXXXXXXXXXXXXXX'
    # 发件人的邮箱
    sender_qq_mail = '1035917380@qq.com'
    # 邮件标题
    mail_title = '充电器预约成功'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
def find_charging_stations():
    """
    查找充电桩状态，并返回第一个空闲的充电桩信息
    """
    api_list = [
        'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001038',
        'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001037',
        'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560002140',
        'http://cdz.gpsserver.cn/ChargeCarSys?gtel=18560001771'  # 老校区
    ]

    while True:  # 循环查询充电桩状态
        for api in api_list:
            print('正在查询：', api)
            response = requests.get(api)
            data = json.loads(response.text)[0]
            mc = data['mc']  # 充电桩地址
            dz = data['dz']
            gtel = data['gtel']  # 充电桩编号
            print(f"{mc} {dz} {gtel}")
            glzt_list = [data[f'glzt{i}'] for i in range(1, 21)]
            for i, glzt in enumerate(glzt_list):
                if glzt == '0':  # 找到第一个状态为0的充电桩
                    return mc, gtel, i+1
            time.sleep(1)  # 每次查询之后等待1秒
        time.sleep(240)  # 每轮查询之后等待5分钟

# 第二个主程序
def get_current_timestamp():
    timestamp = int(time.time() * 1000)
    return str(timestamp)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1'
]

ACCEPT_LANGUAGES = [
    'zh-CN,zh;q=0.9',
    'en-US;q=0.8,en;q=0.7',
    'ja-JP;q=0.9,ja;q=0.8',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_random_accept_language():
    return random.choice(ACCEPT_LANGUAGES)

def get_random_referer():
    referers = [
        'http://cdz.gpsserver.cn/wxhtml/login.html',
        'http://cdz.gpsserver.cn/wxhtml/ChargeCarsys/ChargeCarsys.html?gtel=18560001771_0&b_yy=1'
    ]
    return random.choice(referers)

def start_appointment(gtel, i, usr, pwd):
    # 构建请求头部
    headers = {
        'Host': 'cdz.gpsserver.cn',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': get_random_accept_language(),
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://cdz.gpsserver.cn',
        'User-Agent': get_random_user_agent(),
        'Connection': 'keep-alive',
        'Referer': get_random_referer()
    }

    # 发送 POST 请求，开始登录
    data = {
        'uUser': usr,
        'dma': pwd,
        'openid': ''
    }
    response = requests.post('http://cdz.gpsserver.cn/Login', headers=headers, data=data)

    # 从响应头部中获取 Cookie
    cookie = response.headers.get('Set-Cookie')

    # 构建请求头部，开始预约
    headers['Cookie'] = cookie
    data = {
        'b_cmzt': '0',
        'gtel': gtel,
        'td': i,
        'b_yy': '1',
        'sjtime': get_current_timestamp()
    }
    response = requests.post('http://cdz.gpsserver.cn/CcdSJ', headers=headers, data=data)

    # 开始预约并返回预约结果
    if response.json()[0]['par'] == 'succeed':
        print('预约成功')
        # send_email('1035917380@qq.com', str(data))
    elif response.json()[0]['par'] == 'err_gnoreg':
        print('预约失败')

def read_json_file():
    # 打开 JSON 文件，读取其中的数据
    with open("data.json", "r") as f:
        data_dict = json.load(f)

    # 将数据打包为一个元组并返回
    return data_dict["account"], data_dict["user"], data_dict["password"]

if __name__ == '__main__':
    mc, gtel, i = find_charging_stations()
    print(f"已找到空闲充电桩：{mc}的第{i}号充电桩，编号是{gtel}")
    print('正在预约...请等待')
    time.sleep(2)
    start_appointment(gtel, i, read_json_file()[1], read_json_file()[2])

