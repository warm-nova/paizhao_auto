import os
import sys
import subprocess
from appium import webdriver
import shutil
import time
import base64

pkgname = "com.knowbox.ocr"
mainactivity = "com.knowbox.ocr.MainActivity"

#传递图片到手机中
def syncpic_paizuoye():
    #传入图片
    nowpath = os.getcwd() + "\\questionPic"
    sdcard_path = "/storage/sdcard0/DCIM/Camera"
    sdcard_path2 = "/storage/emulated/legacy/DCIM/Camera"


    print("step 2:Detect path in PC:", nowpath)

    for path,childpath,files in os.walk(nowpath):
        for i in range(len(files)):
            if files[i][-3:] == 'jpg' or files[i][-3:] == "JPG" or files[i][-3:] == 'PNG' or files[i][-3:] == 'png':

                desired_caps = {
                    'platformName': 'Android',
                    'deviceName': '220cba31',
                    # 'deviceName': '10.200.29.50:5555',
                    'platformVersion': '4.3',
                    'appPackage': 'com.knowbox.ocr',  # 红色部分如何获取下面讲解
                    'appActivity': 'MainActivity',
                    'noReset': True
                }
                driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                delpic_inappium = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/DCIM/Camera/*.jpg'],
                    'includeStderr': True,
                    'timeout': 5000})
                delpic_ocr = driver.execute_script('mobile: shell', {
                    'command': 'rm',
                    'args': ['-f', '/storage/emulated/legacy/as_ocr/images/PhotoCheck/*.*'],
                    'includeStderr': True,
                    'timeout': 5000})
                refresh_ocr = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast','-a','android.intent.action.MEDIA_MOUNTED','-d','file:///storage/emulated/legacy/as_ocr/images/PhotoCheck/'],
                    'includeStderr': True,
                    'timeout': 5000})

                print("STEP 1: DEL PIC FINISH")
                nowpic = nowpath + "\\" + files[i]
                print("Now pic is:" + nowpic)

                with open(nowpic,"rb") as f:
                     image_data = f.read()
                     base64_data = base64.b64encode(image_data,altchars=None)


                finaldata = str(base64_data,encoding='utf-8')
                print(finaldata)
                driver.push_file("/storage/emulated/legacy/DCIM/Camera/test.jpg",finaldata)


                #syncpic = 'adb push ' + nowpic + " /storage/emulated/legacy/DCIM/Camera/test.jpg"  # 传入图片
                #step2 = subprocess.Popen(syncpic, shell=True, stdout=subprocess.PIPE)
                #print(syncpic)

                print("STEP 2:SYNC PICTURE FINISH.")

                refresh_pic = driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d',
                             'file:///storage/emulated/legacy/DCIM/Camera/test.jpg'],
                    'includeStderr': True,
                    'timeout': 15000})



                print("STEP 3 FINISH")

                # start_appium = "appium -a 127.0.0.1 -p 4723 --session-override"
                # step0 = subprocess.Popen(start_appium, shell=True, stdout=subprocess.PIPE)
                # print("RUN SUCCESS")

                driver.implicitly_wait(30)
                driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.knowbox.ocr:id/action']").click()
                driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.knowbox.ocr:id/tv_album']").click()

                driver.find_element_by_xpath("//android.view.View[@resource-id='com.knowbox.ocr:id/check_view']").click()
                driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.knowbox.ocr:id/button_apply']").click()

                time.sleep(20)
                img_folder = os.getcwd() + '\\screenshots\\'
                timer = time.strftime('%m%d', time.localtime(time.time()))
                screen_save_path = files[i] + "_paizuoye" + "__" + timer + '.png'
                print("STEP4 : SCREENSHOT IN "+ img_folder)
                driver.get_screenshot_as_file(screen_save_path)
               # driver.reset()
                driver.quit()






syncpic_paizuoye()