import requests

def send_verification_code(utel, area):
    """
    :发送验证码,参数分别是手机号和区号。不知道是不是区号，反正无论填写啥都能发验证码
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
        'utel': utel,
        'area': area
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

if __name__ == '__main__':
    print(send_verification_code('15091108117', '10'))

