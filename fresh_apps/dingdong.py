import uiautomator2 as u2
import time
from config import *

class Crawler(object):
    def __init__(self, device, app, swipe_duration=0.05):
        """
        :param device: usb(设备名称)/ADB WiFi(ip:port)/wifi (ip)
        :param app: packageName
        :param swipe_speed: 滑屏间隔 s
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

    def handle_category(self):
        """
        遍历分类标签
        :return: None
        """
        # 点击过的分类
        clicked_items = []
        while True:
            time.sleep(2)
            # 获取当前屏幕上所有分类名称
            if self.driver(resourceId="com.yaya.zone:id/name").exists(30):
                current_items = self.driver(resourceId="com.yaya.zone:id/name")
                current_items_name = [
                    name.get_text() for name in current_items if name.get_text() != "推荐"
                ]
                if not current_items_name:
                    print("获取控件列表失败")
                    return
                print(current_items_name)
                # 遍历当前屏幕没有点击过的分类
                for name in current_items_name:
                    if name not in clicked_items:
                        self.driver(text=name).click()
                        clicked_items.append(name)
                        print("正在处理" + ">" * 10 + name)
                        self.swipe()
                        if name == "厨房用品":
                            print("操作完成")
                            return

    def swipe(self):
        """
        滑动
        :return: None
        """
        start_end = self.start_to_end()
        while True:
            self.driver.swipe(*start_end, self.swipe_duration)
            if self.driver(text="到底了，看看别的分类吧").exists():
                break

    def run(self):
        """
        启动
        :return: None
        """
        # 自动跳过弹窗，因为此功能不稳定，作者已取消
        # self.driver.disable_popups()
        # 检测是否有警告提示（清除缓存会有提示）
        for _ in range(3):
            time.sleep(1)
            if self.driver(resourceId="android:id/custom"):
                self.driver(text="允许").click()
                print("跳过警告")
        # 检测是否有弹窗广告
        if self.driver(resourceId="com.yaya.zone:id/iv_close").exists(timeout=5):
            self.driver(resourceId="com.yaya.zone:id/iv_close").click()
            print("跳过弹窗广告")
        time.sleep(3)
        # 点击<分类>
        if self.driver(resourceId="com.yaya.zone:id/tab_category").exists(30):
            self.driver(resourceId="com.yaya.zone:id/tab_category").click()
            print("点击分类")
        else:
            print("点击 <分类> 失败")
            return
        time.sleep(2)
        # 遍历分类目录
        self.handle_category()


if __name__ == "__main__":
    """
    叮咚买菜
    反爬分析：
    手机不安装xponsed+JustTrustME 自动化和代理都不会返回数据
    本地代理拦截一段时间对方会停止返回数据
    使用动态代理ip访问恢复正常
    虽然app很小，但是还是有一定的反爬策略
    """
    print(DEVICES['jinli']['name'])
    crawler = Crawler(
        device=DEVICES['jinli']['name'], app=APP["dingdong"], swipe_duration=0.01
    )
    crawler.run()
