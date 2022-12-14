from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
import pandas as pd
import numpy as np

IMPLICT_WAIT = 5


def find_place_id(df, place_name):
    result = df.loc[df['place_name'] == place_name]
    return int(result.loc['place_ID'])

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
def find_reviews(driver, places):
    # 500๊ฐ์ ๋ฆฌ๋ทฐ x 100๊ฐ์ ์ฌํ์ง์ ๋ํ ๋ฆฌ์คํธ
    places = np.array(places)

    place_reviews_collection = []
    error_search = []
    count = 0
    for place in places:
        count += 1
        place_id = place[0]
        #total_review = place[3]
        #collect_review = max(200, total_review//5)
        if '๊ฑฐ๋ฆฌ' in place[1]:
            target = place[1][:-2] + "๊ธธ"  # ๊ฑฐ๋ฆฌ๋ก ๊ฒ์ํ๋ฉด ๊ธธ์ฐพ๊ธฐ๋ก ๊ฒ์
        else:
            target = place[1]
        if count % 100 == 0: time.sleep(10)
        #if count == 4: break  # ํ์คํธ์ฉ
        try:
            # ํค์๋ ๊ฒ์
            search = driver.find_element(By.ID, "searchboxinput")
            search.send_keys(target)
            search_btn = driver.find_element(By.ID, "searchbox-searchbutton")
            search_btn.click()

            # ๊ฒ์ ๊ฒฐ๊ณผ ์์ง
            try:
                elem = driver.find_element(By.CLASS_NAME, "w6VYqd")

                # ๊ฒฐ๊ณผ๊ฐ ๋ชฉ๋ก์ผ๋ก ๋์ฌ ๋
                try:
                    elem = elem.find_elements(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
                    elem = elem.find_element(By.TAG_NAME, "a")
                    href = elem.get_attribute('href')
                    driver.get(href)

                finally:
                    driver.implicitly_wait(IMPLICT_WAIT)

                    sum_div = driver.find_element(By.CLASS_NAME, "lMbq3e")

                    # Review ๋ฒํผ
                    review_btn = sum_div.find_element(By.TAG_NAME, "button")
                    review_btn.click()
                    driver.implicitly_wait(IMPLICT_WAIT)


                    try:
                        keyword_box = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
                        #keyword_box = keyword_box.find_element(By.CLASS_NAME, "m6QErb.tLjsW")
                    except :
                        print("can't find keyword box")

                    #print(keyword_box.text)
                    #keywords=keyword_box.text
                    """
                    for s in keyword_box:
                        #print(keyword_box.text)
                        print(s.text)
                    """
                    keywords_btns = keyword_box.find_elements(By.CLASS_NAME, "tXNTee.LCTIRd.L6Bbsd")
                    print(len(keywords_btns))
                    keywords=""
                    for keyword_btn in keywords_btns:
                        #keyword_btn.click()
                        keywords+=keyword_btn.text
                        keywords+='|'
                        """
                        try:
                            driver.implicitly_wait(IMPLICT_WAIT)
                            key_word = keyword_btn.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(8) > div:nth-child(2) > div > button > span.uEubGf.fontBodyMedium")
                            num_key_word = keyword_btn.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div:nth-child(8) > div:nth-child(2) > div > button > span.bC3Nkc.fontBodySmall")
                            if num_key_word is not None:
                                keywords += key_word+":"+num_key_word+"|"

                        except Exception:
                            print("error")
                            pass
                        """
                    place_reviews_collection.append([place_id, place[1], keywords])
                    time.sleep(1)
                    #driver.implicitly_wait(IMPLICT_WAIT)


                    # ์คํฌ๋กค
                    """
                    reviews_div = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
                    loop = collect_review//9+1 # 1๋ฒ์ 9๊ฐ์ฉ ํ์ํ๋ค๊ณ? ๊ฐ์?

                    for j in range(loop):
                        driver.execute_script("arguments[0].scrollBy(0,2000)", reviews_div)
                        time.sleep(0.9)
                        driver.execute_script("arguments[0].scrollBy(0,2000)", reviews_div)
                        time.sleep(0.9)
                        driver.execute_script("arguments[0].scrollBy(0,2000)", reviews_div)
                        time.sleep(0.9)


                    # ์คํฌ๋ฉ
                    reviews = reviews_div.find_elements(By.CLASS_NAME, "jftiEf.fontBodyMedium")
                    review_count = 0
                    for review in reviews:
                        review_count += 1

                        try:
                            user = review.get_attribute('aria-label')
                            rating = review.find_element(By.CLASS_NAME, "DU9Pgb")

                            rating = rating.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute("aria-label")
                            rating = int(rating.strip('๋ณํ ๊ฐ'))
                            place_reviews_collection.append([place_id, user, rating])

                        except Exception:
                            pass

                        finally:
                            if review_count > collect_review: break
                    """

                    # ๋ค๋ก๊ฐ๊ธฐ

                    back_btn = driver.find_element(By.CLASS_NAME, "hWERUb")
                    back_btn = back_btn.find_element(By.TAG_NAME, "button")
                    back_btn.click()
                    driver.implicitly_wait(IMPLICT_WAIT)


            except:
                pass

            # ๊ฒ์ ๊ฒฐ๊ณผ ์ญ์?
            delete_btn = driver.find_element(By.XPATH, '//*[@id="sb_cb50"]')
            delete_btn.click()

        except:
            error_search.append(place)

    if driver is not None:
        driver.quit()
    return place_reviews_collection, error_search


number = 3  # 1~14
batch_size = 40
places = pd.read_csv("Busan_place_profiles.csv", header="infer")
#places = pd.read_csv("Busan_utility_error2.csv", header="infer")
places = places.iloc[number*batch_size-batch_size:number*batch_size]
#places = places.iloc[number*batch_size-batch_size:]

# ์คํจ LISt :

driver = create_driver(headless=False)  # Method defined in previous examples
url = 'https://www.google.co.kr/maps'
driver.get(url)  # ๐ Visits a page

# ์์? ํ์
result, error = find_reviews(driver, places)
result = np.array(result)
df = pd.DataFrame(result)
number = str(number)
df.to_csv("Busan_keyword_matrix"+number+".csv", index=False)
#df.to_csv("Busan_utility_matrix_"+'1_2.csv', index=False)
err_df = pd.DataFrame(np.array(error))
err_df.to_csv("Busan_keyword_error"+number+".csv", index=False)

print(result, len(result))
print(error)
