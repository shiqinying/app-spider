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
        if self.d(resourceId="username").exists():
            username = self.username
            pwd = self.pwd
            self.d(resourceId="username").click()
            self._sleep()
            for _ in list(username):
                self.d.send_keys(_)
            self._sleep()
            self.d(resourceId="password").click()
            self._sleep()
            self.d(focused=True).set_text(pwd)
            self._sleep()
            self.d(resourceId="btn-submit").click()
            self._sleep()
            # 点击首页
            if self.d.xpath(
                "//android.webkit.WebView/android.view.View[1]/android.view.View[6]/android.view.View[1]"
            ):
                self.d.xpath(
                    "//android.webkit.WebView/android.view.View[1]/android.view.View[6]/android.view.View[1]"
                ).click()
            # 是否出现保存密码
            self._sleep()
            if self.d(resourceId="com.android.chrome:id/infobar_icon").exists():
                self.d(resourceId="com.android.chrome:id/infobar_close_button").click()
            self._sleep(1)

    def run(self):
        '''
        注意操作间隔不要太短
        :return:
        '''
        # 服务条款和隐私声明
        self._sleep()
        if self.d(resourceId="com.android.chrome:id/terms_accept").exists():
            self.d(resourceId="com.android.chrome:id/terms_accept").click()
            self._sleep(1)
        #  改用搜狗搜索弹出框
        if self.d(text="改用搜狗搜索").exists(3):
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
        # 是否出现启用nfc功能弹窗
        if self.d(text='允许').exists():
            self.d(text='允许').click()
        # 爬取到一定次数后打开淘宝首页会比较慢，设定一个长时等待条件
        if self.d(text="我的淘宝").exists(60):
            self._sleep()
            self.d.xpath('//*[@text="淘宝网触屏版"]/android.view.View[1]/android.view.View[6]/android.view.View[4]').click()
            self._sleep()
            self.if_login()

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
            if self.d(resourceId="J_Search").exists(60):
                self.d(resourceId="J_Search").click()
            for _ in range(10):
                self.d.press('delete')
            for _ in list(kw):
                self.d.send_keys(_)
            self.d.press("enter")
            print('正在搜索：',kw)
            self._sleep(3)
            # 底部是否出现‘打开手机淘宝app’
            if self.d(text="打开手机淘宝App").exists(10):
                # self.d(resourceId="lbfa7b_close").click() "lbfa7b_close" 这个值每次都会发生变化
                self.d.click(0.039, 0.9)
            # 点击并滑动分页器到最后一页,(反爬分析)：顺序点击会自动后退刷新
            self.d(text="1/100").click()
            self.d.swipe_points(
                [(0.079, 0.919), (0.032, 0.919), (0.999, 0.919)], 2 * self._random()
            )
            # 倒序遍历翻页
            page_num = 100

            while True:
                print('当前在第{}页'.format(str(page_num)))
                self.d(text="上一页").click()
                page_num -= 1
                self._sleep(1)
                if self.d(text=self.page).exists(1) and page_num<=5:
                    print("到达第{}页，遍历完毕".format(self.page))
                    break
            self.d.press("back")


if __name__ == "__main__":
    """
    手机：小米8
    app：chrome
    注意：使用h5页面之前要卸载谷歌应用商城和淘宝app，不然会强制跳转
    反爬分析：使用本地网络访问能够持续不登陆状态访问一段时间（50页到100页），到达一定阈值后会提示登录，登录无验证码
    使用代理ip（阿布云全国动态ip）会刺激反爬，访问即要求登陆，登录有手机短信验证码，切换IP无网络响应，禁用cookie反爬无明显减弱
    换回本地网络网络恢复，证明淘宝并没有根据手机设备信息进行验证
    所以怀疑淘宝有ip黑名单，对主流的代理ip爬取建立黑名单ip池，对黑名单里的ip进行强验证
    
    更新策略：在没有可靠ip的情况下，不登陆爬取有些不现实，所以进入主页面首先进行登录
    
    登录过程中善用sleep，不然操作间隔太短容易被识别造成卡死
    
    遍历页数的时候，反爬系统会不定时返回第一页（比如在第72页之后返回第1页停止）
    """
    device = DEVICES['xiaomi8']['name']
    app = APP["chrome"]
    swipe_duration = 0.05
    url = "https://h5.m.taobao.com"
    kws = ["小米", "华为", "三星", "iphone", "HTC"]
    page = 1
    text = '没有更多了~'
    username= TAOBAO_USERNAME
    pwd = TAOBAO_PWD

    crawler = Crawler(
        device=device, app=app, swipe_duration=swipe_duration, url=url, kws=kws, page=page,username=username,pwd=pwd,text=text
    )
    crawler.run()
