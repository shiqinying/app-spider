import uiautomator2 as u2
import time
import random
from config import *

class Crawler(object):
    def __init__(self, device, app, swipe_duration=0.05):
        """
        :param device: usb(设备名称)/ADB WiFi(ip:port)/wifi (ip)
        :param app: packageName
        :param swipe_duration: 滑屏间隔
        """
        self.swipe_duration = swipe_duration
        # 连接手机
        self.driver = u2.connect(device)

        #  equivalent to `pm clear` 关闭app并且清除缓存数据
        self.driver.app_clear(app)
        print("app clear ...")

        # 启动app
        self.driver.app_start(app)
        print("app start ...")

    def get_size(self):
        """
        获取手机显示尺寸
        :return: tuple
        """
        return self.driver.window_size()

    def start_to_end(self):
        """
        获取滑动起始坐标
        :return: tuple
        """
        coord = self.get_size()
        start_x = int(coord[0] * 0.5)
        start_y = int(coord[1] * 0.75)
        end_x = int(coord[0] * 0.5)
        end_y = int(coord[1] * 0.25)
        return start_x, start_y, end_x, end_y

    def swipe_y(self):
        """
        循环滑动
        :return: None
        """
        start_end = self.start_to_end()
        while True:
            self.driver.swipe(*start_end, self.swipe_duration)
            time.sleep(1*self._random())
            if self.driver(text="没有更多内容了").exists():
                print('没有更多内容了')
                break

    def _random(self):
        '''
        反爬，模拟人工滑动
        随机抖动：0.90-1.00
        :return:
        '''
        return random.randint(90, 100) / 100

    def search(self,kw):
        time.sleep(2 * self._random())
        self.driver(resourceId="com.taobao.taobao:id/searchEdit").click()
        time.sleep(2 * self._random())
        self.driver(resourceId="com.taobao.taobao:id/searchEdit").clear_text()
        time.sleep(2 * self._random())
        self.driver.send_keys(kw)
        time.sleep(2 * self._random())
        self.driver(resourceId="com.taobao.taobao:id/searchbtn").click()
        #滑动
        self.swipe_y()
        self.driver.press('back')

    def run(self,kws):
        """
        启动
        :return: None
        """
        time.sleep(2)
        if self.driver(text='允许').exists():
            self.driver(text='允许').click()
        time.sleep(2)
        if self.driver(text='温馨提示').exists():
            self.driver(resourceId="com.taobao.taobao:id/yes").click()
        time.sleep(3)
        if self.driver(text='允许').exists():
            self.driver(text='允许').click()
        time.sleep(2*self._random())
        self.driver(resourceId="com.taobao.taobao:id/home_searchedit").click()
        for kw in kws:
            self.search(kw)

if __name__ == "__main__":

    kws = ['小米','苹果','华为','三星']
    crawler = Crawler(device=DEVICES['xiaomi8']['name'], app=APP['taobao'], swipe_duration=0.05)
    crawler.run(kws=kws)
