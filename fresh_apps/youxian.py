import uiautomator2 as u2
import time
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
            current_items = self.driver(
                resourceId="cn.missfresh.application:id/tv_classify_name"
            )
            current_items_name = [name.get_text() for name in current_items]
            if not current_items_name:
                print("获取分类列表失败")
                return
            print(current_items_name)
            # 遍历当前屏幕没有点击过的分类
            for name in current_items_name:
                if name not in clicked_items:
                    self.driver(text=name).click()
                    clicked_items.append(name)
                    print("正在处理" + ">" * 10 + name)
                    self.swipe()
                    if name == "超市":
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
            if self.driver(text="我是有底线的~").exists():
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
        if self.driver(text="需开启以下权限"):
            self.driver(text="下一步").click()
            print("下一步")
        time.sleep(1)
        if self.driver(text="第 1 项权限（共 2 项）"):
            self.driver(text="允许").click()
            print("开启权限1")
        time.sleep(1)
        if self.driver(text="第 2 项权限（共 2 项）"):
            self.driver(text="允许").click()
            print("开启权限2")

        # 检测是否有弹窗广告
        time.sleep(1)
        if self.driver(resourceId="cn.missfresh.application:id/v_bottom1").exists(
            timeout=5
        ):
            self.driver(resourceId="cn.missfresh.application:id/v_bottom1").click()
            print("跳过弹窗广告")
        # 点击<分类>
        category_button = self.driver.xpath(
            '//*[@resource-id="cn.missfresh.application:id/cv_main_bottom_tab_layout"]/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]'
        )
        if category_button:
            category_button.click()
            print("点击分类")
        else:
            print("点击 <分类> 失败")
            return
        # 遍历分类目录
        self.handle_category()


if __name__ == "__main__":
    """
    模拟器：127.0.0.1:62028
    小米8：192.168.31.218:5555
    usb: 50eb01c7
    每日优鲜：cn.missfresh.application
    """
    crawler = Crawler(
        device=DEVICES['xiaomi8']['name'], app=APP["youxian"], swipe_duration=0.01
    )
    crawler.run()
