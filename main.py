#! /usr/bin/python3
# coding:utf-8

# ====================
# Copyright Miffy 2020.
# All rights received.
#
# 2021/04/03
# v.5.0
#
# repl.it x UptimeRobot
# =====================

import os

import time
import random

# 傳到LINE要用ㄉ
import requests

from selenium import webdriver
# 解決彈出視窗用ㄉ
from selenium.webdriver.support import expected_conditions as EC
# 抓取下拉式選單要用ㄉ
from selenium.webdriver.support.ui import Select
# repl.it要用的設定
from selenium.webdriver.chrome.options import Options

# 讓程式自動喚醒 by UptimeRobot
import keep_alive

# ----------今天不要填我------------
# 記得是從0開始編號 (Miffy = 0, 永宏 = 1)
noMeList = []

# 
# ---------------------------------

# ----------今天我在家------------
# 記得是從0開始編號 (Miffy = 0, 永宏 = 1)
atHomeList = [0, 1, 3, 5, 7, 10, 12, 25, 31, 33]

# 米非, 永宏, 宣庭, 柏諭, 耀升, 廖崇佑, 雲甲, 凱奪, 沛儒, 威哥
# ---------------------------------


# ----------身分證列表--------------
IDcode = os.environ['IDcode_secret'].split(', ')

# ---------------------------------


# ------------姓名列表--------------
nameList = [
    '00 Miffy',
    '01 永宏',
    '02 柏輝',
    '03 軒霆',
    '04 承濬',
    '05 柏諭',
    '06 岱佑',
    '07 耀升',
    '08 亮亮',
    '09 品C',
    '10 廖崇佑',
    '11 鄭博旭',
    '12 凱奪好電',
    '13 邱建銘',
    '14 蔡東宏',
    '15 簡以安',
    '16 張澄鎧',
    '17 黃稟容',
    '18 傅昱仁',
    '19 黃楷竣',
    '20 王翊臣(つˆДˆ)つ｡☆',
    '21 謝博宇',
    '22 Ian Chen',
    '23 陳品睿',
    '24 大寮紅豆王',
    '25 雲甲',
    '26 遠割',
    '27 魯邦',
    '28 郭紘葦',
    '29 沈廷翰：）',
    '30 柯辰翰',
    '31 李沛儒',
    '32 黃羽良',
    '33 劉宗威'
]

# ---------------------------------


# ----[副程式] 傳送LINE Notify------
def sendLINE(MSG):

    headers = {
        "Authorization":
        "Bearer " + "EIinBm0t8Gx6xq6If6rmgweyazrkSrWwgctjenRKPTI",  # 權杖
        "Content-Type": "application/x-www-form-urlencoded"
    }

    localtime = time.asctime(time.localtime(time.time()))  # 產生系統時間
    params = {"message": "\n[" + localtime + "] GMT+0\n#ReplIt\n\n" + MSG}

    r = requests.post("https://notify-api.line.me/api/notify",headers=headers,params=params)

    print("\n[" + localtime + "]\n#ReplIt\n\n" + MSG)
    print(r.status_code)  # 200代表正常


# ----------------------------------


# ----[副程式] 確認時間並激活填報器------
def checkTime():

    # === 定義GMT+8的時間和日期 ===
    localtime_hour = time.localtime().tm_hour + 8

    if (localtime_hour > 24):
        localtime_hour -= 24
        localtime_wday = time.localtime().tm_wday + 2
    else:
        localtime_wday = time.localtime().tm_wday + 1
    # ============================

    # === 判斷是不是假日 ===
    if ((localtime_wday != 6) and (localtime_wday != 7)):

        # === 判斷是不是6.~7. ===
        if ((localtime_hour >= 6) and (localtime_hour <= 7)):
            # 激活填報主程式
            StartUpload()

        else:
            print("[ 現在是禮拜" + str(localtime_wday) + "的 " + str(localtime_hour) + "點。 ]\n[ 等待1hr後再偵測。 ]")
            time.sleep(3600)
            checkTime()

    else:
        print("[ 現在是禮拜" + str(localtime_wday) + "的 " + str(localtime_hour) + "點。 ]\n[ 等待六小時後再偵測。 ]")
        time.sleep(21600)
        checkTime()


# ------------------------------------


# ======================= [主程式] ========================
def StartUpload():

    # Chromedriver設定
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    # 設定執行次數
    times = len(IDcode)
    
    # 公式解的答案和種類
    # MrRight = 0
    # MrRight_type = 0


    # 列清單:)
    LIST = "\n"
    for n in range(0, times, 1):

        if((n not in noMeList) or (n not in atHomeList)):
            LIST = LIST + "\t- " + IDcode[n] + "\t(" + nameList[n] + ")\n"

    sendLINE("今天要填的人有：Ｄ\n（共 " + str(times) + " 人）\n" + LIST)

    # [ 終於開始填 ]
    for n in range(0, times, 1):
        
        LIST = ">> [ 正在填 " + IDcode[n] + " ]\n"
        LIST = LIST + "( " + nameList[n] + " )\n\n"

        if(n in noMeList):

            LIST = LIST + "[X] 今天不填！\n"
            sendLINE(LIST)
            continue

        try:
            # 開啟網頁
            driver.get("https://webap1.kshs.kh.edu.tw/kshsSSO/publicWebAP/bodyTemp/index.aspx")

            
            # 破解radio
            #radio = driver.find_element_by_id('ContentPlaceHolder1_RadioButtonList1_1')
            #radio.click()
            
            # 破解list
            #s1 = Select(driver.find_element_by_id('ContentPlaceHolder1_DropDownList1'))
            #s1.select_by_index(3)
            
            # 破解checkbox
            #checkbox = driver.find_element_by_id('ContentPlaceHolder1_CheckBoxList1_0')
            #checkbox.click()
            #checkbox = driver.find_element_by_id('ContentPlaceHolder1_CheckBoxList1_2')
            #checkbox.click()
            
            
            # ======== ↓↓驗證公式解↓↓ =========
            
            '''
            # 確認是不是找過答案了
            if (MrRight == 0):
                
                print("還沒找過答案")

                # 分流，確定是 [選單] 還是 [單選按鈕]
                if (driver.find_elements_by_id('ContentPlaceHolder1_DropDownList1')):

                    print("finding list...")
                    
                    # [選單]
                    MrRight = 0
                    MrRight_type = 1

                    # 一個一個找，從 選項 1~8
                    for MrRight in range(1, 8, 1):
                        s1 = Select(driver.find_element_by_id('ContentPlaceHolder1_DropDownList1'))
                        s1.select_by_index(MrRight)

                        # 填身分證 + dissmiss alert
                        LoginForLogin()


                        if EC.alert_is_present()(driver):
                            
                            # if there appears alert, it means the answer isn't correct
                            message = driver.switch_to_alert().text
                            print(message)
                            
                            # 點掉alert
                            driver.switch_to_alert().accept()
                        
                        else:
                            
                            # if there no any alert, break out 'for'
                            break


                else:
                    
                    print("finding radio...")
                    
                    # 單選
                    MrRight = 0
                    MrRight_type = 2

                    # 一個一個找，從 id 0~8
                    for MrRight in range(0, 8, 1):
                        radio = driver.find_element_by_id("ContentPlaceHolder1_RadioButtonList1_" + str(MrRight))
                        radio.click()

                        # 填身分證
                        LoginForLogin()

                        if EC.alert_is_present()(driver):
                            
                            # if there appears alert, it means the answer isn't correct
                            message = driver.switch_to_alert().text
                            print(message)
                            
                            # 點掉alert
                            driver.switch_to_alert().accept()
                        
                        else:
                            
                            # if there no any alert, break out 'for'
                            break

            else:
                
                # [找過答案了，直接填]
                
                # 分流，確定是 [選單] 還是 [單選按鈕]
                if (MrRight_typt == 1):

                    # 選單
                    s1 = Select(driver.find_element_by_id('ContentPlaceHolder1_DropDownList1'))
                    s1.select_by_index(MrRight)

                else:

                    # 單選
                    radio = driver.find_element_by_id("ContentPlaceHolder1_RadioButtonList1_" + str(MrRight))
                    radio.click()
            '''
            
            # ======== ↑↑驗證公式解↑↑ =========

            # 填身分證字號
            time.sleep(1)
            search_input = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtId")
            search_input.clear()
            search_input.send_keys(IDcode[n])

            # 按登入鍵
            start_search_btn = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnId")
            start_search_btn.click()

            # 按下alert的確認
            #driver.switch_to_alert().accept()

            # [ 如果已經填過 ]
            if EC.alert_is_present()(driver):
                # 點掉alert
                driver.switch_to_alert().accept()
                LIST = LIST + "[O] 已經填過了拉！\n"

            # [ 如果還沒填過 ]
            else:
                # 選擇 "額溫"
                start_search_input = driver.find_element_by_id("ContentPlaceHolder1_rbType_1")
                start_search_input.click()

                # 產生並填入體溫 (個十位)
                rand = random.randint(35, 36)
                start_search_select = driver.find_element_by_id("ContentPlaceHolder1_ddl1")
                start_search_select.send_keys(rand)
                LIST = LIST + str(rand) + "."

                # 產生並填入體溫 (小數位)
                rand = random.randint(5, 9)
                start_search_select = driver.find_element_by_id("ContentPlaceHolder1_ddl2")
                start_search_select.send_keys(rand)
                LIST = LIST + str(rand) + "\n"

                # 選擇差勤
                s1 = Select(driver.find_element_by_id('ContentPlaceHolder1_ddl3'))

                # 請假的填法
                if(n in atHomeList):
                    LIST = LIST + "差勤：請假！\n"
                    s1.select_by_index(2) #改這個數字
                else:
                    LIST = LIST + "差勤：正常\n"
                    s1.select_by_index(1)

                # 提交體溫
                start_search_btn = driver.find_element_by_id("ContentPlaceHolder1_btnId0")
                start_search_btn.click()

                # 按下確認鈕 (???)
                driver.switch_to_alert().accept()

                # DEBUG
                LIST = LIST + "[O] 填報成功！\n"

        except Exception as e:
            # DEBUG
            LIST = LIST + "[X] 出現奇怪ㄉ錯誤\n" + str(e)

        sendLINE(LIST)

    # 關閉瀏覽器
    driver.close()
    driver.quit()

    # DEBUG
    sendLINE("[ 程式執行完成。 ]")

    # 等待三小時後，重新開始等待
    sendLINE("[ 開始8hr的待機。 ]")
    time.sleep(28800)
    checkTime()


# ========================================================

# 啟動喚醒程式
keep_alive.keep_alive()

# 程式進入點
checkTime()