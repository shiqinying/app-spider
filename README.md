# app-spider
uiautomator2+mitmdump实现对app的爬取

# 架构

![image](https://github.com/shiqinying/app-spider/raw/master/screenshots/架构.png)
# 效果预览
淘宝

![image](https://github.com/shiqinying/app-spider/raw/master/screenshots/taobao/taobao_h5_driver.gif)

抖音

![image](https://github.com/shiqinying/app-spider/raw/master/screenshots/douyin/douyin_driver.gif)

fresh

![image](https://github.com/shiqinying/app-spider/raw/master/screenshots/fresh/youxian_driver.gif)




# 环境
* python3.6
* windows
* 安卓手机

# 使用方法
* 根据工具使用说明/自动化测试工具.md配置uiautomator2
* 根据工具使用说明/抓包软件.md配置charles和mitmproxy
* 将config_template.py文件更改为config.py,配置相应变量
* 创建虚拟环境
```shell
mkvirtualenv --python==指定的python版本 env_name
workon env_name
```
* 安装依赖包 pip install -r requirements.txt

    （生成requirements.txt方法 pip install -r requirements.txt）
    
* 