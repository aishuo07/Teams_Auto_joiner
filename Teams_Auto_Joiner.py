from time import sleep
from tkinter import Tk
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from datetime import date
import json


my_date = date.today()

Day = str(my_date.weekday())
with open("E:/config.json") as json_data_file:
    data = json.load(json_data_file)

while Day in data["class_days"]:
    now = datetime.now()

    current_time = now.strftime("%H")
    if int(data["class_start_time"]) <= int(current_time) < int(data["class_end_time"]):
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        driver = webdriver.Chrome(options=chrome_options, executable_path=data["driver_path"])
        email = data["email_id"]
        password = data["password"]
        action = ActionChains(driver)
        driver.get('https://www.microsoft.com/en-in/microsoft-365/microsoft-teams/group-chat-software')
        sleep(10)
        driver.find_element_by_id('mectrl_headerPicture').click()
        sleep(2.5)
        email_element = driver.find_element_by_name('loginfmt')
        email_element.send_keys(email)

        driver.find_element_by_id('idSIButton9').click()
        sleep(4)

        pass_element = driver.find_element_by_name('passwd')
        pass_element.send_keys(password)


        driver.find_element_by_id('idSIButton9').click()
        sleep(2)
        try:
            driver.find_element_by_id('idSIButton9').click()
            sleep(2)
        except:
            pass
        sleep(10)
        try:
            driver.find_element_by_class_name('use-app-lnk').click()
        except NoSuchElementException:
            pass
        sleep(2)
        more_button = driver.find_elements_by_class_name('more-button-container')
        list_class_links = []
        for i in more_button:
            sleep(1)
            i.click()
            sleep(3)
            driver.find_elements_by_xpath("//*[@class='ts-popover-label']")[3].click()
            sleep(1)
            driver.find_element_by_xpath('//*[@class="ts-btn ts-btn-fluent ts-btn-fluent-primary"]').click()
            list_class_links.append(Tk().clipboard_get())
        count = 0
        while True:
            for i in list_class_links:
                driver.get(i)
                count =0
                try:
                    driver.find_element_by_id('openTeamsClientInBrowser').click()
                    sleep(5)
                except NoSuchElementException:
                    pass
                try:
                    driver.find_element_by_class_name('app-svg icons-filled icons-default-fill').click()
                    sleep(1)
                    driver.find_element_by_class_name('ts-sym has-icon kb-active').click()
                    sleep(1)
                    total_members = driver.find_element_by_class_name('section-header-count')[1]

                except NoSuchElementException:
                    pass
                class_name = driver.find_elements_by_class_name('channel-anchor')
                sleep(5)
                for j in class_name:
                    j.click()
                    time_passed = 0
                    sleep(3)
                    try:
                        driver.find_element_by_xpath('//*[@class="ts-sym ts-btn ts-btn-primary inset-border icons-call-jump-in ts-calling-join-button app-title-bar-button app-icons-fill-hover call-jump-in"]').click()
                        if "Mute microphone" in driver.page_source:
                            driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]').click()
                        if "Turn camera off" in driver.page_source:
                            driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]').click()
                        sleep(5)
                        driver.find_element_by_xpath('//*[@class="join-btn ts-btn inset-border ts-btn-primary"]').click()
                        sleep(3)
                        driver.find_element_by_xpath('//*[@id="roster-button"]').click()
                        while True:
                            attendees = driver.find_elements_by_xpath("//*[@class='toggle-number']")[1]
                            number_of_attendees = attendees.text[1:-1]
                            print(number_of_attendees)
                            if int(number_of_attendees)<20:
                                count = 1
                                break
                            time_passed+=300
                            sleep(300)

                    except NoSuchElementException or ElementClickInterceptedException:
                        pass

                    if count == 1:
                        print("Class attended for {} minutes".format(int(time_passed/60)))
                        break
                    sleep(10)
            sleep(10)
            now = datetime.now()

            current_time = now.strftime("%H")
            if int(current_time)>=int(data["class_end_time"]):
                driver.quit()
