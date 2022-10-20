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
    if headless:  # 👈 Optional condition to "hide" the browser window
        chrome_options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    # 👆  Creation of the "driver" that we're using to interact with the browser

    driver.implicitly_wait(IMPLICT_WAIT)
    # 👆 How much time should Selenium wait until an element is able to interact
    return driver

# 구글맵에서 키워드에 대한 검색 결과 반환
# keyword = 계양구 여행지
def find_places(driver, keywords, filter='서울'):
    place_infos = []
    error_search = []
    count = 0
    for keyword in keywords:
        count += 1
        if '거리' in keyword:
            target = keyword[:-2]+"길" # 거리로 검색하면 길찾기로 검색
        else : target = keyword
        if count%100==0: time.sleep(30)
        #if count == 4: break  # 테스트용
        try:
            # 키워드 검색
            search = driver.find_element(By.ID, "searchboxinput")
            search.send_keys(target)
            search_btn = driver.find_element(By.ID, "searchbox-searchbutton")
            search_btn.click()

            # 검색 결과 수집

            # 스크롤 내리기
            # test = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')

            # print(test.get_attribute("class"))

            #scroll_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')
            #for j in range(10):
            #    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
            #    time.sleep(0.9)

            try:
                elem = driver.find_element(By.CLASS_NAME, "w6VYqd")
                # elem = elem.find_elements(By.TAG_NAME, "div")[1]
                # 결과가 목록으로 나올 때
                try:
                    elem = elem.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
                    elem = elem.find_element(By.TAG_NAME, "a")

                    elem.click()
                finally:
                    driver.implicitly_wait(IMPLICT_WAIT)
                    time.sleep(2.4)
                    # pop_div = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
                    sum_div = driver.find_element(By.CLASS_NAME, "lMbq3e")

                    # 장소명, 평점, 관광지 타이 div
                    #place_info["name"] = sum_div.find_element(By.TAG_NAME, "h1").text
                    avg_and_type = list(sum_div.find_element(By.CLASS_NAME, "skqShb").text.split('\n'))
                    #place_info["avg_rating"] = float(avg_and_type[0])
                    place_type = avg_and_type[2]

                    # 위치 div
                    location = driver.find_element(By.CLASS_NAME, "rogA2c")
                    place_location = location.text
                    place_infos.append([keyword, place_type, place_location])
            except:
                pass

            # 검색 결과 삭제
            delete_btn = driver.find_element(By.XPATH, '//*[@id="sb_cb50"]')
            delete_btn.click()

            # print("error/ success collected: ", place_info)




            #elements = elem.find_elements((By.TAG_NAME, 'a'))

            #for e in elements:
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
locals = ['서울', '인천', '대구', '울산', '부산', '광주', '경기도', '강원도',
          '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도',
          '제주시', '서귀포시', '속초', '강릉','여수', '포항']
"""

# 실패 LISt : 2, 3, 4, 5, 6, 8, 9, 11, 12, 13
for profile in profiles:
    keywords.append(profile[0])
print(keywords)


driver = create_driver()  # Method defined in previous examples
url = 'https://www.google.co.kr/maps'
driver.get(url)  # 👈 Visits a page



# 수정 필요
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

# 장소ID, 장소명, 위치, 평점, 시설분류
# 서울=00

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

df.to_csv('서울.csv')
# 👇 Finding elements
"""
"""
driver.find_elements(By.XPATH, "*")          # 👈 Get all direct elements
driver.find_element(By.CSS_SELECTOR, "#btn") # 👈 Get one element with id "btn"
driver.find_elements(By.TAG_NAME, "h1")      # 👈 Get all 'h1' elements
driver.find_elements(By.CLASS_NAME, "cls")   # 👈 Get all elements with classname "cls"
"""
