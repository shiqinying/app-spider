import uiautomator2 as u2
import time
import random


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

        # equivalent to `am force-stop`, thus you could lose data ，强制退出app
        # self.driver.app_stop(app)
        # print('app stop ...')

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

    def _random(self):
        """
        反爬，模拟人工滑动
        随机抖动：0.90-1.00
        :return:
        """
        return random.randint(90, 100) / 100

    def swipe_y_slow(self):
        """
        缓慢滑动半屏
        :return: None
        """
        start_end = self.start_to_end()
        self.driver.swipe(*start_end, 0.5)
        print("滑屏")

    def swipe_y(self):
        """
        循环滑动
        :return: None
        """
        start_end = self.start_to_end()
        while True:
            self.driver.swipe(*start_end, self.swipe_duration)
            if self.driver(text="已经到底啦").exists():
                print("已经到底啦")
                break

    def swipe_x(self):
        """
        横向滑动
        :return: None
        """
        coord = self.get_size()
        start_x = int(coord[0] * 0.75)
        start_y = int(coord[1] * 0.5)
        end_x = int(coord[0] * 0.25)
        end_y = int(coord[1] * 0.5)

        for _ in range(2):
            self.driver.swipe(start_x, start_y, end_x, end_y)
            print("横向滑过图片")

        # 此处有反爬，如果不设置延迟，无法完成点击操作
        time.sleep(2)
        self.driver.xpath(
            '//*[@resource-id="com.jingdong.pdj:id/iv_start_weibo"]'
        ).click()
        print("点击立即体验")

    def handle_shop(self):
        """
        遍历分类标签
        :return: None
        """
        # 点击过的分类列表，去重
        clicked_items = []
        # 结束信号，如果滑动屏幕后'没有更多商家啦'出现第二次，则结束函数
        flag = 0
        self.swipe_y_slow()
        while True:
            time.sleep(1)
            # 获取当前屏幕上所有店铺名称
            current_items = self.driver(
                resourceId="com.sankuai.meituan:id/txt_poiList_adapter_name"
            )
            current_items_name = [name.get_text() for name in current_items]
            if not current_items_name:
                print("获取商铺列表失败")
                return
            print(current_items_name)
            # 遍历当前屏幕没有点击过的分类
            for name in current_items_name:
                if name not in clicked_items:
                    self.driver(text=name).click()
                    clicked_items.append(name)
                    print("正在处理" + ">" * 10 + name)
                    time.sleep(2)
                    # 判断门店是否休息中，休息中会有弹出图片窗口
                    if self.driver(text="本店休息啦").exists():
                        self.driver.click(0.543, 0.082)
                    self.swipe_y_slow()
                    self.swipe_y()
                    self.driver.press("back")
                    time.sleep(1)
            self.swipe_y_slow()
            if self.driver(text="已经到底啦").exists():
                flag += 1
                if flag == 2:
                    print("商铺遍历结束")
                    break

    def run(self):
        """
        启动
        :return: None
        """
        # 自动跳过弹窗，因为此功能不稳定，作者已取消
        # self.driver.disable_popups()
        # 检测是否有警告提示（清除缓存会有提示）
        time.sleep(1)
        if self.driver(text="第 1 项权限（共 2 项）"):
            self.driver(text="允许").click()
            print("开启权限1")
        time.sleep(1)
        if self.driver(text="第 2 项权限（共 2 项）"):
            self.driver(text="允许").click()
            print("开启权限2")

        # 点击《超市/生鲜》
        time.sleep(3)
        self.driver(description="超市/生鲜").click()

        # 遍历商铺
        time.sleep(5)
        self.handle_shop()


if __name__ == "__main__":
    """
    模拟器：127.0.0.1:62028
    小米8：192.168.31.218:5555  50eb01c7
    美团：com.sankuai.meituan
    """
    crawler = Crawler(device="50eb01c7", app="com.sankuai.meituan", swipe_duration=0.05)
    crawler.run()
