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


def create_driver(headless=False):
    chrome_options = Options()
    if headless:  # 👈 Optional condition to "hide" the browser window
        chrome_options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # 👆  Creation of the "driver" that we're using to interact with the browser

    driver.implicitly_wait(IMPLICT_WAIT)
    # 👆 How much time should Selenium wait until an element is able to interact
    return driver


# 구글맵에서 키워드에 대한 검색 결과 반환
# keyword = 계양구 여행지
def find_places(driver, keywords):
    place_profiles = []
    for keyword in keywords:
        print("keyword", keyword)
        place_profile = {}

        try:
            # 키워드 검색
            """
            search = driver.find_element(By.TAG_NAME, "input")
            search.click()
            search.send_keys(keyword)
            driver.implicitly_wait(IMPLICT_WAIT)
            time.sleep(2.4)
            search.send_keys(Keys.ENTER)
            driver.implicitly_wait(IMPLICT_WAIT)
            """
            # 검색 결과 수집 Ld2paf
            # 주요 명소 더 보기 버튼 클릭
            more_btn = more_btn.find_element(By.XPATH, '//button[text()="주요 명소 모두 보기"]')
            more_btn = driver.find_element(By.CLASS_NAME, "aBgjX")
            more_btn = more_btn.find_element(By.TAG_NAME, "button")
            more_btn.click()


            # 스크롤 내리기
            # test = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')

            # print(test.get_attribute("class"))

            # 현재 검색 목록에 대해 상위 N개의 엘리먼트 수집
            elems = driver.find_element(By.CLASS_NAME, "Ld2paf")

            for e in elems:
                try:
                    e.click()
                    driver.implicitly_wait(IMPLICT_WAIT)

                    """
                    time.sleep(2.4)
                    # pop_div = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
                    sum_div = driver.find_element(By.CLASS_NAME, "lMbq3e")

                    place_info = dict({})

                    # 장소명, 평점, 관광지 타이 div
                    place_info["name"] = sum_div.find_element(By.TAG_NAME, "h1").text
                    avg_and_type = list(sum_div.find_element(By.CLASS_NAME, "skqShb").text.split('\n'))
                    place_info["avg_rating"] = float(avg_and_type[0])
                    place_info["type"] = avg_and_type[2]

                    # 위치 div
                    location = driver.find_element(By.CLASS_NAME, "rogA2c")
                    place_info["location"] = location.text

                    place_infos["list"].append(place_info)
                    """
                except Exception:
                    pass

            # 검색 결과 삭제
            delete_btn = driver.find_element(By.CLASS_NAME, "SS0SXe")
            delete_btn = delete_btn.find_element(By.TAG_NAME, "button")
            delete_btn.click()

            # print("error/ success collected: ", place_info)

            # elements = elem.find_elements((By.TAG_NAME, 'a'))

            # for e in elements:
            #    print(e.text)
            # place = elem.find_element(By.XPATH, './/div/div[@role="listbox]')
            """
                try:
                    # idx번째 place의 엘리먼트 수집
                    place = driver.find_element(By.TAG_NAME, 'h1')
                    lines = place.text.split('\n')
                    # First Line = 장소명
                    place_info['name'] = lines[0]
                    # 나머지 = details
                    place_info['details'] = ','.join(lines[1:])

                    place.click()
                    place.implicitly_wait(IMPLICT_WAIT)

                    # 상세 정보 엘리먼트 수집
                    elem = driver.find_element(By.CLASS_NAME, 'widget-pane-content-holder')
                    # 주소 수집
                    try:
                        addr = elem.find_element(By.XPATH, './/div/div[@data-section-id="ad]')
                        place_info['address'] = addr.text
                    except Exception:
                        pass

                    print(place_info)
                except NoSuchElementException:
                    # 검색 결과 중 idx를 넘어가 for loop에 빠짐 방지
                    break

                except Exception:
                    raise
            """
        except Exception:
            pass

    if driver is not None:
        driver.quit()


def travel_list(file_name):
    local_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:

            local_list.append(line.strip())
        print(local_list)

    return local_list


driver = create_driver()  # Method defined in previous examples
url = 'https://www.google.com/travel/things-to-do?dest_mid=%2Fm%2F0hsqf&dest_state_type=main&dest_src=yts&q=%EC%84%9C%EC%9A%B8&ved=0CAAQ8IAIahcKEwi47tjXwtD6AhUAAAAAHQAAAAAQFg'
driver.get(url)  # 👈 Visits a page

"""
places = ['강남', '강동', '강서', '강북', '관악', '광진', '구로', '금천',
          '노원', '동대문', '도봉', '동작', '마포', '서대문', '성동', '성북',
          '서초', '송파', '영등포', '용산', '양천', '은평', '종로', '중구', '중랑']
"""
local_names = travel_list("지역명.txt")

# 수정 필요
place_profiles = find_places(driver, local_names)

# for place in places:
#    seoul.append(find_places(driver, place))

print(place_profiles)
# 장소ID, 장소명, 위치, 평점, 시설분류
# 서울=00
"""
"""
profiles = []
"""
for idx, gu in enumerate(place_profiles):
    for place in gu['list']:
        if idx < 10:
            place_id = '0' + str(idx)
        else:
            place_id = str(idx)
        place_id = "00" + place_id
        place_name = place['name']
        place_avg = place['avg_rating']
        place_type = place['type']
        place_loc = place['location']
        profile = [place_id, place_name, place_avg, place_type, place_loc]
        profiles.append(profile)

profiles = np.array(profiles)
df = pd.DataFrame(profiles)

df.to_csv('서울.csv')
# 👇 Finding elements
"""
"""
driver.find_elements(By.XPATH, "*")          # 👈 Get all direct elements
driver.find_element(By.CSS_SELECTOR, "#btn") # 👈 Get one element with id "btn"
driver.find_elements(By.TAG_NAME, "h1")      # 👈 Get all 'h1' elements
driver.find_elements(By.CLASS_NAME, "cls")   # 👈 Get all elements with classname "cls"
"""
print("end!")