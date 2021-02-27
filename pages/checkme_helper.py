from pages.checkme import Checkme
from selenium.webdriver.common.by import By


class PageLocators:
    # PARTS OF TABLE
    TABLE_HEADER_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/thead")
    TABLE_CONTENT_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/tbody")

    # PARTS OF HEADER
    NAME_HEADER_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/thead/tr/th[1]")
    COUNT_HEADER_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/thead/tr/th[2]")
    PRICE_HEADER_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/thead/tr/th[3]")
    ACTION_HEADER_XPATH_LOCATOR = (By.XPATH, "//table[@id='tbl']/thead/tr/th[4]")

    # BUTTONS
    OPEN_BUTTON_ID_LOCATOR = (By.ID, "open")
    DISCARD_BUTTON_XPATH_LOCATOR = (By.XPATH, "//a[text()='Сбросить']")
    ADD_BUTTON_ID_LOCATOR = (By.ID, "add")

    # FIELDS IN ADD FORM
    INPUT_NAME_FIELD_ID_LOCATOR = (By.ID, "name")
    INPUT_COUNT_FIELD_ID_LOCATOR = (By.ID, "count")
    INPUT_PRICE_FIELD_ID_LOCATOR = (By.ID, "price")


class CheckmeHelper(Checkme):

    # HEADER
    def click_the_names_header(self):
        return self.find_element(locator=PageLocators.NAME_HEADER_XPATH_LOCATOR, time=2).click()

    def click_the_counts_header(self):
        return self.find_element(locator=PageLocators.COUNT_HEADER_XPATH_LOCATOR, time=2).click()

    def click_the_prices_header(self):
        return self.find_element(locator=PageLocators.PRICE_HEADER_XPATH_LOCATOR, time=2).click()

    def click_the_actions_header(self):
        return self.find_element(locator=PageLocators.ACTION_HEADER_XPATH_LOCATOR, time=2).click()

    # BUTTONS
    def click_the_open_button(self):
        return self.find_element(locator=PageLocators.OPEN_BUTTON_ID_LOCATOR, time=2).click()

    def click_the_discard_button(self):
        return self.find_element(locator=PageLocators.DISCARD_BUTTON_XPATH_LOCATOR, time=2).click()

    def click_the_add_button(self):
        return self.find_element(locator=PageLocators.ADD_BUTTON_ID_LOCATOR, time=2).click()

    def click_the_delete_record(self, n):
        return self.find_element(locator=(By.XPATH, f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr[{n}]/td/a[@class='delete']"), time=2).click()

    # FIELDS
    def enter_name(self, name=None):
        name_field = self.find_element(locator=PageLocators.INPUT_NAME_FIELD_ID_LOCATOR, time=2)
        if name:
            name_field.click()
            name_field.send_keys(name)
        return name_field

    def enter_count(self, count=None):
        count_field = self.find_element(locator=PageLocators.INPUT_COUNT_FIELD_ID_LOCATOR, time=2)
        if count:
            count_field.click()
            count_field.send_keys(count)
        return count_field

    def enter_price(self, price=None):
        price_field = self.find_element(locator=PageLocators.INPUT_PRICE_FIELD_ID_LOCATOR, time=2)
        if price:
            price_field.click()
            price_field.send_keys(price)
        return price_field

    def enter_item_information(self, name=None, count=None, price=None):
        self.enter_name(name)
        self.enter_count(count)
        self.enter_price(price)


