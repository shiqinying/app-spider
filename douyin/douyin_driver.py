import uiautomator2 as u2
import time
import random
import queue
import chaojiying
from config import *


class Crawler(object):
    def __init__(
        self,
        device,
        app,
        swipe_duration,
        hot_stars,
        chaojiying_name,
        chaojiying_pwd,
        chaojiying_soft_id,
        chaojiying_code_type,
        tel,
        pwd,
    ):
        """
        :param device: usb(设备名称)/ADB WiFi(ip:port)/wifi (ip)
        :param app: packageName
        :param swipe_duration: 滑屏间隔
        :param hot_stars: 需要搜索的star列表
        :param chaojiying_name: 超级鹰用户名
        :param chaojiying_pwd:  超级鹰密码
        :param chaojiying_soft_id: 超级鹰软件id
        :param chaojiying_code_type: 超级鹰验证码类型
        :param tel: 抖音手机号
        :param pwd: 抖音密码
        """
        self.swipe_duration = swipe_duration
        self.q = self.init_queue(hot_stars)
        self.chaojiying_name = chaojiying_name
        self.chaojiying_pwd = chaojiying_pwd
        self.chaojiying_soft_id = chaojiying_soft_id
        self.chaojiying_code_type = chaojiying_code_type
        self.tel = tel
        self.pwd = pwd

        # 连接手机
        self.d = u2.connect(device)
        # 关闭app并且清除缓存
        self.d.app_clear(app)
        print("app clear ...")
        # 启动app
        self.d.app_start(app)
        print("app start ...")
        # 获取手机屏幕大小
        self.coord = self.d.window_size()
        print("手机屏幕大小：", self.coord)

    def start_to_end(self):
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

    def swipe_y(self):
        """
        循环滑动
        :return: None
        """
        start_to_end = self.start_to_end()
        while True:
            self.d.swipe(*start_to_end, self.swipe_duration)
            if self.d(text="没有更多了~").exists():
                print("当前粉丝没有更多了~")
                break

    def init_queue(self, hot_stars):
        """
        将需要搜索的star初始化到队列
        :param hot_stars:
        :return:
        """
        q = queue.Queue(100)
        for _ in hot_stars:
            q.put(_)
        print("初始化star队列完成", q.qsize())
        return q

    def search(self):
        # 点击搜索
        self.d(description="搜索").click()
        # 选中搜索框
        self.d(resourceId="com.android.systemui:id/status_bar_contents").down(className='android.widget.LinearLayout').click()
        # 清除搜索框
        self.d(focused=True).clear_text()
        time.sleep(2 * self._random())
        # 从队列获取一个需要搜索的star
        star = self.q.get()
        print("正在操作", "*" * 10, star)
        # 输入   注意用法
        for _ in list(star):
            time.sleep(0.1 * self._random())
            self.d.send_keys(_)
        # 点击搜索
        self.d(text="搜索").click()
        # 点击《用户》
        time.sleep(2 * self._random())
        self.d(resourceId="android:id/text1", text="用户").click()
        # 点击第一个用户
        time.sleep(2 * self._random())
        self.d(className="android.widget.LinearLayout",instance=4).click()
        # 点击粉丝
        time.sleep(2 * self._random())
        self.d(text="粉丝").click()
        # 滑动粉丝列表
        time.sleep(2 * self._random())
        self.swipe_y()
        # 滑动到最底部后返回到首页
        for _ in range(4):
            self.d.press("back")

    def login(self):
        time.sleep(2 * self._random())
        # 首页点击《我》标签 进入登录页面
        # d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/chd"]/android.widget.FrameLayout[5]')
        #d.xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/ccf"]/android.widget.FrameLayout[5]')
        #反爬分析：xpath路径是动态变化的，应该是隔天变动的，改用坐标点击
        self.d(text='我').click()
        time.sleep(2)
        if self.d(text='手机验证码或密码登录').exists():
            self.d(text="手机验证码或密码登录").click()
        # 点击屏幕右上角密码登陆
        self.d(text="密码登录").click()
        time.sleep(2 * self._random())
        # 点击 手机号码输入框
        self.d(text="输入手机号码").click()
        # 模拟手工输入方式手机号码
        for _ in list(self.tel):
            time.sleep(0.1 * self._random())
            self.d.send_keys(_)
        time.sleep(1 * self._random())
        # 点击密码输入框
        self.d(text="输入账号密码").click()
        time.sleep(1 * self._random())
        # 输入密码
        self.d(focused=True).set_text(self.pwd)
        time.sleep(1 * self._random())
        # 点选我已阅读 用户协议 ,容易误点‘用户协议’，采用相对定位
        self.d(text="我已阅读并同意 用户协议 和 隐私政策").left(className='android.widget.ImageView').click()
        time.sleep(1 * self._random())
        # 点击登录
        self.d(description="确认").click()
        time.sleep(2 * self._random())
        # 解决图片验证码和手机验证码
        self.captcha_has_or_not()

    def captcha_has_or_not(self):
        while True:
            # 判断是否有图片验证码，需多次判断，以防验证码填写失败
            if self.d(text="请输入图片中的字符").exists():
                print("出现图片验证码！！！")
                # 将验证码截取出来保存到本地
                self.save_captcha()
                # captcha_code = input('请输入验证码：')
                # 通过超级鹰平台识别验证码
                captcha_code = self._chaojiying()
                # 点击验证码输入框
                self.d(className="android.widget.EditText").click()
                # 输入验证码
                self.d.send_keys(captcha_code)
                self.d(text="确定").click()
                time.sleep(2 * self._random())

                # 判断是否出现手机验证码，暂且手动输入，出错概率很低，不必循环判断
                if self.d(text="为保护你的账号安全，请重新验证").exists():
                    self.d(text="获取验证码").click()
                    time.sleep(2 * self._random())
                    self.d(text="输入验证码").click()
                    tel_captcha = input("请输入手机验证码：")
                    self.d.send_keys(tel_captcha)
                    # 点击确认
                    self.d(resourceId="com.ss.android.ugc.aweme:id/o1").click()
                    time.sleep(2 * self._random())
                    print("登陆成功")
                    break
            else:
                print("登陆成功")
                break

        # 判断是否出现手机验证码，暂且手动输入，出错概率很低，不必循环判断
        if self.d(text="为保护你的账号安全，请重新验证").exists():
            self.d(text="获取验证码").click()
            time.sleep(2 * self._random())
            self.d(text="输入验证码").click()
            tel_captcha = input("请输入手机验证码：")
            self.d.send_keys(tel_captcha)
            # 点击确认
            self.d(resourceId="com.ss.android.ugc.aweme:id/o1").click()
            time.sleep(2 * self._random())
            print("登陆成功")
    def save_captcha(self):
        """
        截取保存图片验证码
        :return:
        """
        time.sleep(2 * self._random())
        # 获取验证码元素边框像素位置  例：bountds={'top': 385,'right': 360,'bottom': 585,'left': 200}
        bounds = self.d(text="请输入图片中的字符").down(className='android.widget.ImageView').info.get("bounds")
        bounts = (bounds["left"], bounds["top"], bounds["right"], bounds["bottom"])
        # 截屏
        screen_shot = self.d.screenshot()
        # 从截屏中截取验证码
        captcha = screen_shot.crop(bounts)
        # 保存验证码到当前文件夹
        captcha.save("captcha.png")
        print("验证码保存成功")

    def _chaojiying(self):
        cjy = chaojiying.Chaojiying_Client(
            self.chaojiying_name, self.chaojiying_pwd, self.chaojiying_soft_id
        )
        im = open("captcha.png", "rb").read()
        # {'err_no': 0, 'err_str': 'OK', 'pic_id': '9073610502616700001', 'pic_str': '3rhr', 'md5': 'e18ed33cf0007d024657a41706e91f59'}
        captcha_code = cjy.PostPic(im, self.chaojiying_code_type).get("pic_str")
        print("当前验证码是：", captcha_code)
        return captcha_code

    def run(self):
        # 检测是否有警告提示
        time.sleep(3)
        if self.d(text="第 1 项权限（共 2 项）"):
            self.d(text="允许").click()
            print("开启权限1")
        time.sleep(1)
        if self.d(text="第 2 项权限（共 2 项）"):
            self.d(text="允许").click()
            print("开启权限2")
        # 随便点击一下消除屏障
        time.sleep(3)
        self.d.click(0.5 * self._random(), 0.5 * self._random())
        # 主动登录，不登陆搜索容易弹出登录提示
        self.login()
        while True:
            # 判断star队列是否为空
            time.sleep(1 * self._random())
            if self.q.empty():
                print("star遍历完毕")
                return
            # 搜索并遍历star粉丝列表
            self.search()


if __name__ == "__main__":
    """
    手机：小米8
    app: 抖音
    反爬分析：千万不要使用resourceId和xpath定位元素，resourseId每天都会变化，尽量使用text或者descrition，
    最坏方案使用像素相对位置d.click(xxx,ooo)
    项目中如果有元素不能定位，请按照如上方案更改
    """
    device = DEVICES['xiaomi8']['name']
    app = APP["douyin"]
    swipe_duration = 0.05
    hot_stars = ["1651144627","迪丽热巴", "1101395521", "jingyingGL", "陈赫", "何炅"]
    chaojiying_name = CJY_NAME
    chaojiying_pwd = CJY_PWD
    chaojiying_soft_id = CJY_SOFT_ID  # http://www.chaojiying.com/user/mysoft/
    chaojiying_code_type = 1902  # 题目类型 参考 http://www.chaojiying.com/price.html
    tel = DOUYIN_TEL
    pwd = DOUYIN_PWD

    crawler = Crawler(
        device=device,
        app=app,
        swipe_duration=swipe_duration,
        hot_stars=hot_stars,
        chaojiying_name=chaojiying_name,
        chaojiying_pwd=chaojiying_pwd,
        chaojiying_soft_id=chaojiying_soft_id,
        chaojiying_code_type=chaojiying_code_type,
        tel=tel,
        pwd=pwd,
    )
    crawler.run()
