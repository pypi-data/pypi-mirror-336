from uiautomator import Device
import subprocess
import pycountry, phonenumbers
from phonenumbers import geocoder
import requests
import random
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains
#twine upload dist/*
#__init__.py
#rm -rf dist build *.egg-info setup.py
#python3 setup.py sdist bdist_wheel
#pip install --upgrade clselove
def auto(pan,d):
    kind, name = pan.split("@")[0], pan.split("#")[0].split("@")[-1]
    name_se = pan.split("#")[-1] if "#" in pan else None
    def b():
        clickable_elements = d(clickable=True)
        clickable_elements[int(name)].click()
    action_map = {
        "cl_te": lambda: d(text=name).click(),"cl_cl": lambda: d(className=name).click(),"cl_id": lambda: d(resourceId=name).click(),"cl_de": lambda: d(description=name).click(),
        "cl_tee": lambda: d(text=name),"cl_cll": lambda: d(className=name),"cl_idd": lambda: d(resourceId=name),"cl_dee": lambda: d(description=name),
        "se_te": lambda: d(text=name).set_text(name_se) if name_se else None,"se_cl": lambda: d(className=name).set_text(name_se) if name_se else None,"se_id": lambda: d(resourceId=name).set_text(name_se) if name_se else None,"se_de": lambda: d(description=name).set_text(name_se) if name_se else None,
        "cr_te": lambda: d(text=name).clear_text(),"cr_cl": lambda: d(className=name).clear_text(),"cr_id": lambda: d(resourceId=name).clear_text(),"cr_de": lambda: d(description=name).clear_text(),
        "sc_te": lambda: any(d(scrollable=True).scroll.forward() for _ in range(20)) if not d(text=name).exists else d(text=name).click(),"sc_cl": lambda: any(d(scrollable=True).scroll.forward() for _ in range(10)) if not d(className=name).exists else d(className=name).click(),"sc_id": lambda: any(d(scrollable=True).scroll.forward() for _ in range(10)) if not d(resourceId=name).exists else d(resourceId=name).click(),"sc_de": lambda: any(d(scrollable=True).scroll.forward() for _ in range(10)) if not d(description=name).exists else d(description=name).click(),
        "en": lambda: d.press('enter'),"ba": lambda: d.press.back(),"ti": lambda: time.sleep(int(name)),
        "cr": lambda: subprocess.run(f"adb -s {ip_address} shell pm clear {name}", shell=True, capture_output=True, text=True),
        "op": lambda: subprocess.run(f"adb -s {ip_address} shell am start -n {name}", shell=True, capture_output=True, text=True),
        "st": lambda: subprocess.run(f"adb -s {ip_address} shell am force-stop {name}", shell=True, capture_output=True, text=True),
        "sw": lambda: subprocess.run(f"adb -s {ip_address} shell input swipe {name}",shell=True, capture_output=True, text=True),
       "not": lambda: subprocess.run(f"adb -s {ip_address} shell cmd statusbar expand-notifications", shell=True, capture_output=True, text=True),
       "col": lambda:subprocess.run(f"adb -s {ip_address} shell cmd statusbar collapse", shell=True, capture_output=True, text=True),
       "bo": lambda: b(),
            }
    action_map.get(kind, lambda: None)()
def get_phone(name):
    response_get = requests.get(f'{name}.json')
    user_data = response_get.json()
    if not user_data:
        print('No phone found', name)
        return None, None, None, None
    first_key = random.choice(list(user_data.keys()))
    phone = user_data[first_key].strip()
    requests.delete(f'{name}/{phone}.json')
    parsed_number = phonenumbers.parse(f'+{phone}')
    country = pycountry.countries.get(alpha_2=phonenumbers.region_code_for_country_code(parsed_number.country_code))
    country_code, fn, co = parsed_number.country_code, country.name[0], country.name.split(",")[0] if country else (None, None)
    return phone, country_code, fn, co
def se(pan,driver):
    kind, name = pan.split("@")[0], pan.split("#")[0].split("@")[-1]
    name_se = pan.split("#")[-1] if "#" in pan else None
    action_map = {
       "cl_xp": lambda:driver.find_element(By.XPATH, name).click(),
       "cl_id": lambda:driver.find_element(By.ID, name).click(),
       "cl_na": lambda:driver.find_element(By.NAME, name).click(),
       "cl_cl": lambda:driver.find_element(By.CLASS_NAME, name).click(),
       "cl_cs": lambda:driver.find_element(By.CSS_SELECTOR, name).click(),
       "cl_ta": lambda:driver.find_element(By.TAG_NAME, name).click(),
       "se_xp": lambda:driver.find_element(By.XPATH, name).send_keys(name_se),
       "se_id": lambda:driver.find_element(By.ID, name).send_keys(name_se),
       "se_na": lambda:driver.find_element(By.NAME, name).send_keys(name_se),
       "se_cl": lambda:driver.find_element(By.CLASS_NAME, name).send_keys(name_se),
       "se_cs": lambda:driver.find_element(By.CSS_SELECTOR, name).send_keys(name_se),
       "se_ta": lambda:driver.find_element(By.TAG_NAME, name).send_keys(name_se),
       "cr_xp": lambda:driver.find_element(By.XPATH, name).clear(),
       "cr_id": lambda:driver.find_element(By.ID, name).clear(),
       "cr_na": lambda:driver.find_element(By.NAME, name).clear(),
       "cr_cl": lambda:driver.find_element(By.CLASS_NAME, name).clear(),
       "cr_cs": lambda:driver.find_element(By.CSS_SELECTOR, name).clear(),
       "cr_ta": lambda:driver.find_element(By.TAG_NAME, name).clear(),
       "get": lambda:driver.get(name),
       "qu": lambda:driver.quit(),
       "clo": lambda:driver.close(),
       "add_co": lambda:driver.add_cookie(name),
       "de_co": lambda:driver.delete_all_cookies(),
       "get_co": lambda:driver.get_cookies(),
       "get_url": lambda:driver.current_url,
       "get_ti": lambda:driver.title,
       "ba": lambda:driver.back(),
       "ha": lambda:driver.switch_to.window(driver.window_handles[int(name)]),
       "sc": lambda:driver.save_screenshot(name),
       "wa": lambda:driver.implicitly_wait(name),
       "re": lambda:driver.refresh(),
       "size": lambda:driver.set_window_size(int(name), (name_se)),
       "en": lambda:ActionChains(driver).send_keys(Keys.ENTER).perform(),
       "html": lambda:driver.page_source,
            }
    action_map.get(kind, lambda: None)()


