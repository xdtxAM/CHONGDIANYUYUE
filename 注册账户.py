import requests
import json
import code验证码


def login_by_sms(utel, smsche):
    """
    通过短信验证码登录,参数分别是手机号和验证码
    :param utel:手机号
    :param smsche:验证码
    :return:
    """
    url = 'http://cdz.gpsserver.cn/LoginSms'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': 'UArealanstr=zh; AppUAreab_mode=0; jzmm=true; GetRfSimfalg=0; pageitem=0; uUser=tong; dma=991013; JSESSIONID=3336BCEA0013941ECAF84C4FA374B2D5; AppName=%u4E91%u4EAB%u5145%u7535',
        'DNT': '1',
        'Host': 'cdz.gpsserver.cn',
        'Origin': 'http://cdz.gpsserver.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://cdz.gpsserver.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    data = {
        'utel': utel,
        'smsche': smsche,
        'uUser[isTrusted]': 'true'
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()

        json_data = response.json()
        # print(json_data)
        # first_uuser = json_data[0]['uUser']  # 获取第一个 uUser 值
        # 获取最后一个 uUser 值
        last_uuser = json_data[len(json_data) - 1]['uUser']
        # return first_uuser, last_uuser
        return last_uuser
    except requests.exceptions.Timeout:
        return "请求超时"
    except requests.exceptions.RequestException as e:
        return f"请求出错：{e}"
    except (ValueError, KeyError):
        return "响应数据解析失败"


def save_to_json(account, smsche, password):
    # 将用户输入放入 Python 字典中
    data = {'account': account, 'user': smsche, 'password': password}

    # 将 Python 字典转换成 JSON 字符串并写入 JSON 文件中
    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    phone = input('输入手机号后按回车键继续')
    code验证码.send_verification_code(phone, '10')
    smsche = input('输入验证码后按回车键继续')  # 这个信息是就是登陆标识符
    password = input('输入密码后按回车键继续')
    print(login_by_sms(phone, smsche))
    login_bin = login_by_sms(phone, smsche)
    # save_to_json的存储顺序是，先是手机号，后是登陆标识符，再是密码
    save_to_json(phone, login_bin, password)
