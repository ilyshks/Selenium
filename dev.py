from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class BaseTest:
    def __init__(self, browser_name):
        if browser_name == "yandex":
            binary_yandex_driver_file = "D:\\Yandex Driver\\yandexdriver.exe"
            options = webdriver.ChromeOptions()
            service = Service(binary_yandex_driver_file)
            self.driver = webdriver.Chrome(service=service, options=options)
        elif browser_name == "edge":
            binary_edge_driver_file = "D:\\Edge Driver\\msedgedriver.exe"
            service = Service(binary_edge_driver_file)
            self.driver = webdriver.Edge(service=service)
        else:
            raise ValueError("Unsupported browser")
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()


class TestValidRegistration(BaseTest):
    def __init__(self, browser_name):
        super().__init__(browser_name)

    def test_valid_registration(self):
        self.driver.get("https://www.saucedemo.com/")
        
        # Ожидание появления элемента с именем "user-name"
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username_field.send_keys("standard_user")
        
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys("secret_sauce")
        
        login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        
        time.sleep(3)  # Ждем загрузки страницы
        if "Products" in self.driver.page_source:
            print("Регистрация выполнена успешно, тест пройден!")
        else:
            print("Регистация не выполнена, тест провален!")


class TestInvalidRegistration(BaseTest):
    def __init__(self, browser_name):
        super().__init__(browser_name)

    def test_invalid_registration(self):
        self.driver.get("https://www.saucedemo.com/")
        
        # Ожидание появления элемента с именем "user-name"
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username_field.send_keys("invalid_user")
        
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys("invalid_password")
        
        login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        
        time.sleep(3)  # Ждем загрузки страницы
        if "Epic sadface: Username and password do not match any user in this service" in self.driver.page_source:
            print("Вход под невалидными данными не выполнен, тест пройден!")
        else:
            print("Вход под невалидными данными выполнен, тест провален!")


class TestValidSearch(BaseTest):
    """
    Тестирование валидного запроса.
    """
    def __init__(self, browser_name):
        super().__init__(browser_name)

    def test_valid_search(self):
        print(self.__doc__)
        self.driver.get("https://miet.ru/search")
        
        # Ожидание появления элемента поиска
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("факультет")
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(3)  # Ждем результаты поиска
        
        # Суммируем все data-count у элементов класса search-bar__list-item
        search_items = self.driver.find_elements(By.CLASS_NAME, "search-bar__list-item")
        total_count = sum(int(item.get_attribute("data-count")) for item in search_items if item.get_attribute("data-count"))
        if total_count > 0:
            print(f"Найдено {total_count} результатов, тест пройден!")
        else:
            print("Совпадений не найдено, тест провален!")


class TestInvalidSearch(BaseTest):
    """
    Тестирование невалидного запроса.
    """
    def __init__(self, browser_name):
        super().__init__(browser_name)

    def test_invalid_search(self):
        print(self.__doc__)
        self.driver.get("https://miet.ru/search")
        
        # Ожидание появления элемента поиска
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("asdfghjkl")
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(3)  # Ждем результаты поиска
        
        # Суммируем все data-count у элементов класса search-bar__list-item
        search_items = self.driver.find_elements(By.CLASS_NAME, "search-bar__list-item")
        total_count = sum(int(item.get_attribute("data-count")) for item in search_items if item.get_attribute("data-count"))
        
        if total_count == 0:
            print("Совпадений не найдено, тест пройден!")
        else:
            print(f"Найдено {total_count} результатов, тест провален!")
        assert total_count == 0, "Unexpected search results found"


if __name__ == "__main__":
    
    for browser in ("yandex", "edge"):
        # Тестирование регистрации с валидными данными
        test_valid_reg = TestValidRegistration(browser)
        test_valid_reg.test_valid_registration()
        test_valid_reg.tearDown()

        # Тестирование регистрации с невалидными данными
        test_invalid_reg = TestInvalidRegistration(browser)
        test_invalid_reg.test_invalid_registration()
        test_invalid_reg.tearDown()
    
        # Тестирование поиска с валидным значением
        test_valid_search = TestValidSearch(browser)
        test_valid_search.test_valid_search()
        test_valid_search.tearDown()

        # Тестирование поиска с невалидным значением
        test_invalid_search = TestInvalidSearch(browser)
        test_invalid_search.test_invalid_search()
        test_invalid_search.tearDown()