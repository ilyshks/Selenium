import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time


@pytest.fixture(params=["yandex", "edge"])
def driver(request):
    browser_name = request.param
    if browser_name == "yandex":
        binary_yandex_driver_file = "D:\\Yandex Driver\\yandexdriver.exe"
        options = webdriver.ChromeOptions()
        service = Service(binary_yandex_driver_file)
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "edge":
        binary_edge_driver_file = "D:\\Edge Driver\\msedgedriver.exe"
        service = Service(binary_edge_driver_file)
        driver = webdriver.Edge(service=service)
    else:
        raise ValueError("Unsupported browser")
    
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


def test_valid_registration(driver, wait):
    driver.get("https://www.saucedemo.com/")
    
    username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    username_field.send_keys("standard_user")
    
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys("secret_sauce")
    
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#login-button")))
    login_button.click()
    
    time.sleep(3)  # Ждем загрузки страницы
    assert "Products" in driver.page_source, "Регистрация не выполнена, тест провален!"


def test_invalid_registration(driver, wait):
    driver.get("https://www.saucedemo.com/")
    
    username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']")))
    username_field.send_keys("invalid_user")
    
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    password_field.send_keys("invalid_password")
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
    login_button.click()
    
    time.sleep(3)  # Ждем загрузки страницы
    assert "Epic sadface: Username and password do not match any user in this service" in driver.page_source, "Вход под невалидными данными выполнен, тест провален!"


def test_valid_search(driver, wait):
    driver.get("https://miet.ru/search")
    
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='q']")))
    search_box.send_keys("факультет")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)  # Ждем результаты поиска
    
    search_items = driver.find_elements(By.TAG_NAME, "a")
    total_count = sum(int(item.get_attribute("data-count")) for item in search_items if item.get_attribute("data-count"))
    assert total_count > 0, "Совпадений не найдено, тест провален!"


def test_invalid_search(driver, wait):
    driver.get("https://miet.ru/search")
    
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys("asdfghjkl")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)  # Ждем результаты поиска

    news = driver.find_element(By.LINK_TEXT, "Новости и анонсы")
    people = driver.find_element(By.LINK_TEXT, "Люди")
    departments = driver.find_element(By.PARTIAL_LINK_TEXT, "Подраздел")
    pages = driver.find_element(By.PARTIAL_LINK_TEXT, "Страни")

    total_count = sum(int(item.get_attribute("data-count")) for item in (news, people, departments, pages))
    # search_items = driver.find_elements(By.CLASS_NAME, "search-bar__list-item")
    # total_count = sum(int(item.get_attribute("data-count")) for item in search_items if item.get_attribute("data-count"))
    assert total_count == 0, "Unexpected search results found"
