from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import numpy as np

IMPLICT_WAIT = 5


def create_driver(headless=True):
    chrome_options = Options()
    if headless:  # ๐ Optional condition to "hide" the browser window
        chrome_options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    # ๐  Creation of the "driver" that we're using to interact with the browser

    driver.implicitly_wait(IMPLICT_WAIT)
    # ๐ How much time should Selenium wait until an element is able to interact
    return driver

# ๊ตฌ๊ธ๋งต์์ ํค์๋์ ๋ํ ๊ฒ์ ๊ฒฐ๊ณผ ๋ฐํ
# keyword = ๊ณ์๊ตฌ ์ฌํ์ง
def find_places(driver, keywords, filter='์์ธ'):
    place_infos = []
    error_search = []
    count = 0
    for keyword in keywords:
        count += 1
        if '๊ฑฐ๋ฆฌ' in keyword:
            target = keyword[:-2]+"๊ธธ" # ๊ฑฐ๋ฆฌ๋ก ๊ฒ์ํ๋ฉด ๊ธธ์ฐพ๊ธฐ๋ก ๊ฒ์
        else : target = keyword
        if count%100==0: time.sleep(30)
        #if count == 4: break  # ํ์คํธ์ฉ
        try:
            # ํค์๋ ๊ฒ์
            search = driver.find_element(By.ID, "searchboxinput")
            search.send_keys(target)
            search_btn = driver.find_element(By.ID, "searchbox-searchbutton")
            search_btn.click()

            # ๊ฒ์ ๊ฒฐ๊ณผ ์์ง

            # ์คํฌ๋กค ๋ด๋ฆฌ๊ธฐ
            # test = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')

            # print(test.get_attribute("class"))

            #scroll_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')
            #for j in range(10):
            #    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
            #    time.sleep(0.9)

            try:
                elem = driver.find_element(By.CLASS_NAME, "w6VYqd")
                # elem = elem.find_elements(By.TAG_NAME, "div")[1]
                # ๊ฒฐ๊ณผ๊ฐ ๋ชฉ๋ก์ผ๋ก ๋์ฌ ๋
                try:
                    elem = elem.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
                    elem = elem.find_element(By.TAG_NAME, "a")

                    elem.click()
                finally:
                    driver.implicitly_wait(IMPLICT_WAIT)
                    time.sleep(2.4)
                    # pop_div = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
                    sum_div = driver.find_element(By.CLASS_NAME, "lMbq3e")

                    # ์ฅ์๋ช, ํ์?, ๊ด๊ด์ง ํ์ด div
                    #place_info["name"] = sum_div.find_element(By.TAG_NAME, "h1").text
                    avg_and_type = list(sum_div.find_element(By.CLASS_NAME, "skqShb").text.split('\n'))
                    #place_info["avg_rating"] = float(avg_and_type[0])
                    place_type = avg_and_type[2]

                    # ์์น div
                    location = driver.find_element(By.CLASS_NAME, "rogA2c")
                    place_location = location.text
                    place_infos.append([keyword, place_type, place_location])
            except:
                pass

            # ๊ฒ์ ๊ฒฐ๊ณผ ์ญ์?
            delete_btn = driver.find_element(By.XPATH, '//*[@id="sb_cb50"]')
            delete_btn.click()

            # print("error/ success collected: ", place_info)




            #elements = elem.find_elements((By.TAG_NAME, 'a'))

            #for e in elements:
            #    print(e.text)
            # place = elem.find_element(By.XPATH, './/div/div[@role="listbox]')
            """
                try:
                    # idx๋ฒ์งธ place์ ์๋ฆฌ๋จผํธ ์์ง
                    place = driver.find_element(By.TAG_NAME, 'h1')
                    lines = place.text.split('\n')
                    # First Line = ์ฅ์๋ช
                    place_info['name'] = lines[0]
                    # ๋๋จธ์ง = details
                    place_info['details'] = ','.join(lines[1:])
    
                    place.click()
                    place.implicitly_wait(IMPLICT_WAIT)
    
                    # ์์ธ ์?๋ณด ์๋ฆฌ๋จผํธ ์์ง
                    elem = driver.find_element(By.CLASS_NAME, 'widget-pane-content-holder')
                    # ์ฃผ์ ์์ง
                    try:
                        addr = elem.find_element(By.XPATH, './/div/div[@data-section-id="ad]')
                        place_info['address'] = addr.text
                    except Exception:
                        pass
    
                    print(place_info)
                except NoSuchElementException:
                    # ๊ฒ์ ๊ฒฐ๊ณผ ์ค idx๋ฅผ ๋์ด๊ฐ for loop์ ๋น?์ง ๋ฐฉ์ง
                    break
    
                except Exception:
                    raise
            """
        except:
            error_search.append(keyword)
            place_infos.append([keyword, '', ''])


    if driver is not None:
        driver.quit()
    return place_infos, error_search

number=14 # 1~14
number = str(number)
profiles = pd.read_csv("place_profile"+number+".csv", header="infer")
profiles = np.array(profiles)
keywords = []
"""
locals = ['์์ธ', '์ธ์ฒ', '๋๊ตฌ', '์ธ์ฐ', '๋ถ์ฐ', '๊ด์ฃผ', '๊ฒฝ๊ธฐ๋', '๊ฐ์๋',
          '์ถฉ์ฒญ๋ถ๋', '์ถฉ์ฒญ๋จ๋', '๊ฒฝ์๋ถ๋', '๊ฒฝ์๋จ๋', '์?๋ผ๋ถ๋', '์?๋ผ๋จ๋',
          '์?์ฃผ์', '์๊ทํฌ์', '์์ด', '๊ฐ๋ฆ','์ฌ์', 'ํฌํญ']
"""

# ์คํจ LISt : 2, 3, 4, 5, 6, 8, 9, 11, 12, 13
for profile in profiles:
    keywords.append(profile[0])
print(keywords)


driver = create_driver()  # Method defined in previous examples
url = 'https://www.google.co.kr/maps'
driver.get(url)  # ๐ Visits a page



# ์์? ํ์
result, error = find_places(driver, keywords)
result = np.array(result)
#for place in places:
#    seoul.append(find_places(driver, place))

print(result)
print(error)

profiles = np.array(profiles)
try:
    profiles = np.concatenate([profiles, result[:, 1:]], 1)
    print(profiles[:])
    df = pd.DataFrame(profiles)
    df.to_csv('place_profile_v2'+number+'.csv', index=False)

except:
    pd.DataFrame(profiles).to_csv(number+'_profile1.csv', index=False)
    pd.DataFrame(result).to_csv(number+'_profile2.csv', index=False)
    print('fail: ', number)

# ์ฅ์ID, ์ฅ์๋ช, ์์น, ํ์?, ์์ค๋ถ๋ฅ
# ์์ธ=00

"""
profiles = []
for idx, gu in enumerate(seoul):
    for place in gu['list']:
        if idx < 10: place_id = '0'+str(idx)
        else: place_id = str(idx)
        place_id = "00"+place_id
        place_name = place['name']
        place_avg = place['avg_rating']
        place_type = place['type']
        place_loc = place['location']
        profile = [place_id, place_name, place_avg, place_type, place_loc]
        profiles.append(profile)

profiles = np.array(profiles)
df = pd.DataFrame(profiles)

df.to_csv('์์ธ.csv')
# ๐ Finding elements
"""
"""
driver.find_elements(By.XPATH, "*")          # ๐ Get all direct elements
driver.find_element(By.CSS_SELECTOR, "#btn") # ๐ Get one element with id "btn"
driver.find_elements(By.TAG_NAME, "h1")      # ๐ Get all 'h1' elements
driver.find_elements(By.CLASS_NAME, "cls")   # ๐ Get all elements with classname "cls"
"""
