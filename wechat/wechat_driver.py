import uiautomator2 as u2
import time
import random
from config import *

class Crawler(object):
    def __init__(self, device, app, swipe_duration,friend_total):
        """
        :param device: usb(设备名称)/ADB WiFi(ip:port)/wifi (ip)
        :param app: packageName
        :param swipe_duration: 滑屏间隔
        """
        self.swipe_duration = swipe_duration
        self.friend_total = friend_total
        # 连接手机
        self.d = u2.connect(device)

        #  equivalent to `pm clear` 关闭app并且清除缓存数据
        self.d.app_clear(app)
        print("app clear ...")

        # 启动app
        self.d.app_start(app)
        print("app start ...")

    def get_size(self):
        """
        获取手机显示尺寸
        :return: tuple
        """
        return self.d.window_size()

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
            self.d.swipe(*start_end, self.swipe_duration)
            time.sleep(1*self._random())
            text = self.friend_total+'位联系人'
            if self.d(text=text).exists():
                print(text)
                break

    def _random(self):
        '''
        反爬，模拟人工滑动
        随机抖动：0.90-1.00
        :return:
        '''
        return random.randint(90, 100) / 100


    def run(self,phone,pwd):
        """
        启动
        :return: None
        """
        time.sleep(2 * self._random())
        if self.d(text='登录').exists():
            self.d(text='登录').click()

        time.sleep(2*self._random())
        if self.d(text='请填写手机号').exists():
            self.d(text='请填写手机号').click()

        time.sleep(2*self._random())
        self.d.send_keys(phone)

        time.sleep(2 * self._random())
        if self.d(text='下一步').exists():
            self.d(text='下一步').click()

        time.sleep(2 * self._random())
        if self.d(text='请填写微信密码').exists():
            self.d(text='请填写微信密码').click()

        time.sleep(2 * self._random())
        self.d.send_keys(pwd)

        time.sleep(2 * self._random())
        if self.d(text='登录').exists():
            self.d(text='登录').click()

        time.sleep(2 * self._random())
        if self.d(text='暂不设置').exists(timeout=60):
            self.d(text='暂不设置').click()

        time.sleep(2 * self._random())
        # 点击通讯录
        self.d.xpath('//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]').click()

        #点击我
        # self.d.xpath(
        #     '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[4]').click()
        # time.sleep(2* self._random())
        # self.d(resourceId="android:id/title", text="相册").click()
        #
        # time.sleep(2* self._random())
        # self.d(text="我的朋友圈").click()

        time.sleep(2 *self._random())
        self.swipe_y()




if __name__ == "__main__":
    phone = WECHAT_PHONE
    pwd = WECHAT_PWD
    friend_total= '716'
    crawler = Crawler(device=DEVICES['xiaomi8']['name'], app=APP["weixin"], swipe_duration=0.05,friend_total=friend_total)
    crawler.run(phone,pwd)
