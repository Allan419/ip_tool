import time
import requests
import json

from utils.http import get_request_headers
# from utils.log import logger
from settings import VALIDATE_TIMEOUT
from domain import Proxy

'''
实现代理池Proxy的检验
'''


def check_proxy(proxy):
    """
    检查proxy的响应速度，匿名程度，支持的协议类型
    :param proxy: 代理IP模型对象
    :return 检查后的代理IP对象
    """
    # print(f"正在检测 {proxy}")
    # 准备代理IP字典
    proxies = {
        'http': f'http://{proxy.ip}:{proxy.port}',
        'https': f'https://{proxy.ip}:{proxy.port}'
    }

    # 测试代理IP
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)

    # 支持协议 support 'http':'protocol=0; 'https':'protocol=1';both: 'protocol=2'
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1

    return proxy


def __check_http_proxies(proxies, is_http=True):
    nick_type = -1  # 表征匿名程度,'高匿名':nick_type=0; '匿名':nick_type=1; '透明':nick_type=2
    speed = -1  # 表征相应速度
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    # print("检测中 $$$$$$$$$$$$$$$$$$$$$$$$$$")
    try:
        start = time.time()
        # print(f"正在检测 ************************************* ")
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=VALIDATE_TIMEOUT)
        if response.ok:

            speed = round(time.time() - start, 2)
            content = json.loads(response.text)
            origin = content['origin']
            proxy_connection = content['headers'].get('Proxy-Connection', None)

            if ',' in origin:
                nick_type = 2  # 表示透明代理
            elif proxy_connection:
                nick_type = 1  # 表示匿名代理
            else:
                nick_type = 0  # 表示高匿代理

            return True, nick_type, speed

        else:
            return False, nick_type, speed

    except Exception as e:
        # logger.exception(e)
        # print(e)
        return False, nick_type, speed

if __name__ == '__main__':

    proxy = Proxy('150.138.106.80','80')
    a = check_proxy(proxy)
    proxy = Proxy('182.46.97.28','9999')
    a = check_proxy(proxy)
    print(a)
