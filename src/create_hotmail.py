import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re
import requests


# data_full= [{'username': 'vigorous_euclid6', 'password': '00aYrV5g57', 'firstname': 'Trần Đỗ Thị', 'lastname': 'Hoa', 'data_of_birth': '02/28/2003', 'current_row': 2},..,{}]
def reg_outlook(driver, data):
    wait = WebDriverWait(driver, 12)
    driver.set_page_load_timeout(40)
    try:
        driver.get('https://outlook.live.com/owa/?nlp=1&signup=1')
        # fill username
        username_wait = wait.until(EC.visibility_of_element_located((By.ID, "MemberName")))  # wait page loaded
        username_wait.send_keys(data['username'])
        time.sleep(1)
        driver.find_element(By.ID, "iSignupAction").click()

        # fill password
        password_wait = wait.until(EC.presence_of_element_located((By.ID, "PasswordInput")))
        password_wait.send_keys(data['password'])
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 150)")
        driver.find_element(By.ID, 'iSignupAction').click()

        # fill firstname and lastname
        firstname_wait = wait.until(EC.visibility_of_element_located((By.ID, "FirstName")))  # wait page loaded
        firstname_wait.send_keys(data['firstname'])  # fill username
        driver.find_element(By.ID, 'LastName').send_keys(data['lastname'])
        driver.find_element(By.ID, 'iSignupAction').click()

        # select day of birth
        wait.until(EC.visibility_of_element_located((By.ID, "Country")))
        birth_of_date = str(data['data_of_birth']).split('/')  # [month,date,year]
        Select(driver.find_element(By.ID, 'BirthMonth')).select_by_index(int(birth_of_date[0]))
        Select(driver.find_element(By.ID, 'BirthDay')).select_by_index(int(birth_of_date[1]))
        driver.find_element(By.ID, 'BirthYear').send_keys(birth_of_date[2])
        driver.execute_script("""document.querySelector('input#iSignupAction').click();""")

        # wait for solver captcha
        WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.ID, "enforcementFrame")))
        # solve captcha anycaptcha automation...
        if check_sign_in_btn(driver):
            return 'LIVE| {} | {}'.format(data['username'], data['password'])
        # wait login mail
        WebDriverWait(driver, 30).until(EC.url_contains('https://outlook.live.com/mail/0'))
        # turn on pop
        return 'LIVE| {} | {}'.format(data['username'], data['password'])
    except Exception as e:
        e = re.sub(r'Stacktrace.+', '', str(e), flags=re.S)
        error_mess = driver.find_elements(By.ID, 'MemberNameError')
        print('DEAD| {} | {} | {} | {}'.format(data['username'], data['password'], error_mess, e))
        if error_mess:
            return '{}'.format(error_mess[0].text)
        elif driver.find_elements(By.CSS_SELECTOR, 'a[title="Send code"]'):
            return 'verify phone'
        else:
            return 'Error: {}'.format(e)
    finally:
        time.sleep(4)


def check_sign_in_btn(driver):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Stay signed in?"]')))
        return True
    except Exception as e:
        return False
