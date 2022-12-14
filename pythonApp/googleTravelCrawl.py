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
    if headless:  # π Optional condition to "hide" the browser window
        chrome_options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # π  Creation of the "driver" that we're using to interact with the browser

    driver.implicitly_wait(IMPLICT_WAIT)
    # π How much time should Selenium wait until an element is able to interact
    return driver


# κ΅¬κΈλ§΅μμ ν€μλμ λν κ²μ κ²°κ³Ό λ°ν
# keyword = κ³μκ΅¬ μ¬νμ§
def find_places(driver, keywords):
    place_profiles = []
    for keyword in keywords:
        print("keyword", keyword)
        place_profile = {}

        try:
            # ν€μλ κ²μ
            """
            search = driver.find_element(By.TAG_NAME, "input")
            search.click()
            search.send_keys(keyword)
            driver.implicitly_wait(IMPLICT_WAIT)
            time.sleep(2.4)
            search.send_keys(Keys.ENTER)
            driver.implicitly_wait(IMPLICT_WAIT)
            """
            # κ²μ κ²°κ³Ό μμ§ Ld2paf
            # μ£Όμ λͺμ λ λ³΄κΈ° λ²νΌ ν΄λ¦­
            more_btn = more_btn.find_element(By.XPATH, '//button[text()="μ£Όμ λͺμ λͺ¨λ λ³΄κΈ°"]')
            more_btn = driver.find_element(By.CLASS_NAME, "aBgjX")
            more_btn = more_btn.find_element(By.TAG_NAME, "button")
            more_btn.click()


            # μ€ν¬λ‘€ λ΄λ¦¬κΈ°
            # test = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div/div/div/div/div/div/div')

            # print(test.get_attribute("class"))

            # νμ¬ κ²μ λͺ©λ‘μ λν΄ μμ Nκ°μ μλ¦¬λ¨ΌνΈ μμ§
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

                    # μ₯μλͺ, νμ , κ΄κ΄μ§ νμ΄ div
                    place_info["name"] = sum_div.find_element(By.TAG_NAME, "h1").text
                    avg_and_type = list(sum_div.find_element(By.CLASS_NAME, "skqShb").text.split('\n'))
                    place_info["avg_rating"] = float(avg_and_type[0])
                    place_info["type"] = avg_and_type[2]

                    # μμΉ div
                    location = driver.find_element(By.CLASS_NAME, "rogA2c")
                    place_info["location"] = location.text

                    place_infos["list"].append(place_info)
                    """
                except Exception:
                    pass

            # κ²μ κ²°κ³Ό μ­μ 
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
                    # idxλ²μ§Έ placeμ μλ¦¬λ¨ΌνΈ μμ§
                    place = driver.find_element(By.TAG_NAME, 'h1')
                    lines = place.text.split('\n')
                    # First Line = μ₯μλͺ
                    place_info['name'] = lines[0]
                    # λλ¨Έμ§ = details
                    place_info['details'] = ','.join(lines[1:])

                    place.click()
                    place.implicitly_wait(IMPLICT_WAIT)

                    # μμΈ μ λ³΄ μλ¦¬λ¨ΌνΈ μμ§
                    elem = driver.find_element(By.CLASS_NAME, 'widget-pane-content-holder')
                    # μ£Όμ μμ§
                    try:
                        addr = elem.find_element(By.XPATH, './/div/div[@data-section-id="ad]')
                        place_info['address'] = addr.text
                    except Exception:
                        pass

                    print(place_info)
                except NoSuchElementException:
                    # κ²μ κ²°κ³Ό μ€ idxλ₯Ό λμ΄κ° for loopμ λΉ μ§ λ°©μ§
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
driver.get(url)  # π Visits a page

"""
places = ['κ°λ¨', 'κ°λ', 'κ°μ', 'κ°λΆ', 'κ΄μ', 'κ΄μ§', 'κ΅¬λ‘', 'κΈμ²',
          'λΈμ', 'λλλ¬Έ', 'λλ΄', 'λμ', 'λ§ν¬', 'μλλ¬Έ', 'μ±λ', 'μ±λΆ',
          'μμ΄', 'μ‘ν', 'μλ±ν¬', 'μ©μ°', 'μμ²', 'μν', 'μ’λ‘', 'μ€κ΅¬', 'μ€λ']
"""
local_names = travel_list("μ§μ­λͺ.txt")

# μμ  νμ
place_profiles = find_places(driver, local_names)

# for place in places:
#    seoul.append(find_places(driver, place))

print(place_profiles)
# μ₯μID, μ₯μλͺ, μμΉ, νμ , μμ€λΆλ₯
# μμΈ=00
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

df.to_csv('μμΈ.csv')
# π Finding elements
"""
"""
driver.find_elements(By.XPATH, "*")          # π Get all direct elements
driver.find_element(By.CSS_SELECTOR, "#btn") # π Get one element with id "btn"
driver.find_elements(By.TAG_NAME, "h1")      # π Get all 'h1' elements
driver.find_elements(By.CLASS_NAME, "cls")   # π Get all elements with classname "cls"
"""
print("end!")