import uiautomator2 as u2
import time
import random
import queue
from chaojiying import Chaojiying_Client
from config import *


class Crawler(object):
    def __init__(self, device, app, swipe_duration, url, kws, page,username,pwd,text):
        """
        :param device: usb(设备名称)/ADB WiFi(ip:port)/wifi (ip)
        :param app: packageName
        :param swipe_duration: 滑屏间隔
        :param url: 入口链接
        :param kws: 搜索关键字
        :param page: 结束页数
        :param username: 用户名
        :param pwd: 密码
        :param text: 滑动结束文本提示
        """
        self.swipe_duration = swipe_duration
        self.url = url
        self.kws = kws
        self.page = page
        self.username = username
        self.pwd = pwd
        self.text = text
        # 连接手机
        self.d = u2.connect(device)
        # 关闭app并且清除缓存
        self.d.app_clear(app)
        print("app clear ...")
        # 启动app
        self.d.app_start(app)
        print("app start ...")
        # 获取手机屏幕尺寸
        self.coord = self.d.window_size()
        print("手机屏幕大小：", self.coord)

    def _start_to_end(self):
        """
        获取滑动起始坐标
        :return: tuple
        """
        start_x = int(self.coord[0] * 0.5) * self._random()
        start_y = int(self.coord[1] * 0.75) * self._random()
        end_x = int(self.coord[0] * 0.5) * self._random()
        end_y = int(self.coord[1] * 0.25) * self._random()
        return start_x, start_y, end_x, end_y

    def _random(self):
        """
        反爬
        随机抖动：0.95-1.00
        :return:
        """
        return random.randint(90, 100) / 100

    def _swipe_y(self):
        """
        循环滑动
        :return: None
        """
        start_to_end = self._start_to_end()
        while True:
            self.d.swipe(*start_to_end, self.swipe_duration)
            text = self.text
            if self.d(text=text).exists():
                print(text)
                break

    def _sleep(self, s=2):
        return time.sleep(s * self._random())

    def if_login(self):
        if self.d(text="短信验证码登录").exists():
            username = self.username
            pwd = self.pwd
            self.d(resourceId="username").click()
            for _ in list(username):
                self.d.send_keys(_)
            self.d(resourceId="password").click()
            # self.d.send_keys(pwd)
            self._sleep()
            self.d(focused=True).set_text(pwd)
            self.d(resourceId="btn-submit").click()
            # 点击首页
            if self.d.xpath(
                "//android.webkit.WebView/android.view.View[1]/android.view.View[6]/android.view.View[1]"
            ).exists:
                self.d.xpath(
                    "//android.webkit.WebView/android.view.View[1]/android.view.View[6]/android.view.View[1]"
                ).click()
            # 是否出现保存密码
            if self.d(resourceId="com.android.chrome:id/infobar_icon").exists():
                self.d(resourceId="com.android.chrome:id/infobar_close_button").click()
            self._sleep(10)

    def run(self):
        # 服务条款和隐私声明
        self._sleep()
        if self.d(resourceId="com.android.chrome:id/terms_accept").exists():
            self.d(resourceId="com.android.chrome:id/terms_accept").click()
            self._sleep(1)
        #  改用搜狗搜索弹出框
        if self.d(text="改用搜狗搜索").exists():
            self.d(text="继续使用 Google").click()
            self._sleep(1)
        # 点击并输入网址
        self._sleep()
        self.d(resourceId="com.android.chrome:id/search_box_text").click()
        self.d.send_keys(self.url)
        self.d.press("enter")
        # 判断是否需要登陆
        self._sleep(1)
        self.if_login()
        # 判断是否出现 ‘chrome 正在尝试使用 nfc’
        if self.d(resourceId="com.lbe.security.miui:id/contentPanel").exists(60):
            # 拒绝
            self.d(resourceId="android:id/button2").click()
        # 爬取到一定次数后打开淘宝首页会比较慢，设定一个长时等待条件
        if self.d(text="天猫").exists(60):
            pass
        # 搜索宝贝，（反爬）主页加载完毕后，点击搜索框有时会无效，循环判断页面是否跳转
        while True:
            if self.d(text="寻找宝贝店铺").exists(1):
                self.d(text="寻找宝贝店铺").click()
                self._sleep()
            else:
                break
        for kw in self.kws:
            self._sleep()
            #点击并清除搜索框
            self.d(resourceId="J_Search").click()
            for _ in range(10):
                self.d.press('delete')
            for _ in list(kw):
                self.d.send_keys(_)
            self.d(text="提交").click()
            self._sleep(3)
            self.if_login()
            # 底部是否出现‘打开手机淘宝app’
            if self.d(text="打开手机淘宝App").exists(30):
                # self.d(resourceId="lbfa7b_close").click() "lbfa7b_close" 这个值每次都会发生变化
                self.d.click(0.039, 0.9)
            # 点击并滑动分页器到最后一页,(反爬分析)：顺序点击会自动后退刷新
            self.d(text="1/100").click()
            self.d.swipe_points(
                [(0.079, 0.919), (0.032, 0.919), (0.999, 0.919)], 2 * self._random()
            )
            # 倒序遍历翻页
            while True:
                self.d(text="上一页").click()
                self._sleep(2)
                if self.d(text=self.page).exists():
                    print("到达第{}页，遍历完毕".format(self.page))
                    break
                self.if_login()
            self.d.press("back")


if __name__ == "__main__":
    """
    手机：小米8
    app：chrome
    注意：使用h5页面之前要卸载谷歌应用商城和淘宝app，不然会强制跳转
    """
    device = "50eb01c7"  # 127.0.0.1:62028  192.168.31.218:5555
    app = "com.android.chrome"
    swipe_duration = 0.05
    url = "https://h5.m.taobao.com"
    kws = ["小米", "华为", "三星", "iphone", "HTC"]
    page = 98
    text = '没有更多了~'
    username= TAOBAO_USERNAME
    pwd = TAOBAO_PWD

    crawler = Crawler(
        device=device, app=app, swipe_duration=swipe_duration, url=url, kws=kws, page=page,username=username,pwd=pwd,text=text
    )
    crawler.run()
