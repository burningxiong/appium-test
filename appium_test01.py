#! /usr/bin/env python
# coding: utf8
import os
import unittest
from appium import webdriver
import time
import random

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class WalletAndroidTests(unittest.TestCase):
    def setUp(self):
        # 初始化Desired Capabilities
        # 用于告知appium server，关于安卓应用的信息
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.3.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = "D:/ZIMPAY-WALLET.apk"
        desired_caps['appPackage'] = 'com.zimpay.wallet'
        desired_caps['appActivity'] = 'com.zimpay.wallet.activity.LoginActivity'
        # 创建appium server对象
        self.driver = webdriver.Remote('http://192.168.1.130:4723/wd/hub', desired_caps)

    def tearDown(self):
        # 结束测试
        self.driver.quit()

    def test_bandVISA(self):
        # 配置服务器IP和端口
        self.wait_element("com.zimpay.wallet:id/service_config","by_id").click()
        textfields1 = self.wait_element("android.widget.EditText","by_class_name")
        textfields1[0].send_keys("192.168.0.125")
        textfields1[1].send_keys("8030")
        textfields1[2].send_keys("8080")
        self.wait_element("com.zimpay.wallet:id/ok_btn","by_id").click()
        # 登录
        textfields2 = self.wait_element("android.widget.EditText","by_class_name")
        textfields2[0].send_keys("8615922712265")
        textfields2[1].send_keys("1234567")
        self.wait_element("com.zimpay.wallet:id/ok_btn","by_id").click()
        # 绑定VISA卡
        self.wait_element("com.zimpay.wallet:id/visa_cards","by_id").click()
        self.wait_element("com.zimpay.wallet:id/add_button","by_id").click()
        self.wait_element("com.zimpay.wallet:id/card_no","by_id").send_keys("4" + self.get_rand_str(15))
        self.wait_element("com.zimpay.wallet:id/card_type","by_id").click()
        # 选择VISA卡类型
        self.wait_element("android.widget.TextView","by_class_name")[random.randint(0,1)]
        self.driver.keyevent(4)
        self.wait_element("com.zimpay.wallet:id/Button","by_id").click()
        self.wait_element("com.zimpay.wallet:id/card_user_name","by_id").send_keys("test" + self.get_rand_str(6))
        # 返回类型是list
        self.wait_element("com.zimpay.wallet:id/card_mobile","by_id").send_keys(self.get_rand_str(11))
        # 选择有效日期
        self.wait_element("com.zimpay.wallet:id/card_expire_date","by_id").click()
        self.driver.keyevent(4)
        self.wait_element("com.zimpay.wallet:id/radiobutton1","by_id").click()
        self.wait_element("com.zimpay.wallet:id/card_ok_btn","by_id").click()
        # 等待绑定成功
        self.wait_element("com.zimpay.wallet:id/add_button","by_id")

    def wait_element(self,str_mark,str_type):
        """ 等待控件显示完全
        """
        int_flag = 1
        while int_flag:
            try:
                if "by_id" == str_type:
                    obj_res = self.driver.find_element_by_id(str_mark)
                if "by_class_name" == str_type:
                    obj_res = self.driver.find_elements_by_class_name(str_mark)
                if "by_name" == str_type:
                    obj_res = self.driver.find_elements_by_name(str_mark)
                int_flag = 0
            except:
                int_flag = 1
                time.sleep(1)
        return obj_res

    def get_rand_str(self,int_digit):
        """ 获取任意位数的数字串
        """
        str1 = ""
        for i in range(int_digit):
          str1 += str(random.randint(0,9))
        return str1

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WalletAndroidTests)
    for i in range(2):
        unittest.TextTestRunner(verbosity=2).run(suite)
