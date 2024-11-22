from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
binary_yandex_driver_file = r"D:\Yandex Driver\yandexdriver.exe"
service = Service(binary_yandex_driver_file)
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
driver.get("https://account.miet.ru/login?backurl=https%3A%2F%2Fmiet.ru")


input_username = driver.find_element(By.ID, "inputLogin")
input_password = driver.find_element(By.NAME, "USER_PASSWORD")
button = driver.find_element(By.TAG_NAME, "button")
block_auth = driver.find_element(By.CLASS_NAME, "auth-container__content")
css = driver.find_element(By.CSS_SELECTOR, "")



input("Нажмите Enter, чтобы закрыть окно браузера...")
driver.quit()