from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
binary_yandex_driver_file = r"D:\Yandex Driver\yandexdriver.exe"
service = Service(binary_yandex_driver_file)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.saucedemo.com/")
input_username = driver.find_element(By.ID, "user-name")
if input_username is None:
   print("Элемент не найден")
else:
   print("Элемент найден")

input("Нажмите Enter, чтобы закрыть окно браузера...")
driver.quit()