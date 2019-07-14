import requests
from config import *


# adsl动态拨号代理
def get_random_proxy():
    try:
        url = ADSL_URL
        return requests.get(url).text
    except requests.exceptions.ConnectionError:
        return None

if __name__=="__main__":
    '''
    http://httpbin.org/get是境外网站，访问有延迟
    可以使用 docker run -p 80:80 kennethreitz/httpbin
    部署在自己的服务器进行访问测试
    '''
    ip = get_random_proxy()

    print(ip)

    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }
    r = requests.get('https://www.baidu.com', proxies=proxies)
    print(r.text)