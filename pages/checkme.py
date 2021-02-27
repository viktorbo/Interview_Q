from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait


class Checkme:

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://checkme.kavichki.com/"

    def find_element(self, locator, time=10):
        return wait(self.driver, time).until(EC.presence_of_element_located(locator),
                                             message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return wait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                             message=f"Can't find elements by locator {locator}")

    def go_to_site(self):
        return self.driver.get(self.url)

    def refresh(self):
        return self.driver.refresh()