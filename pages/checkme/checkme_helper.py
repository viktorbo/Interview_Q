from pages.checkme.checkme import Checkme
from pages.checkme.checkme_locators import PageLocators
from selenium.webdriver.common.by import By


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

    # HEADER PARSING
    def get_names_header(self):
        return self.find_element(locator=PageLocators.NAME_HEADER_XPATH_LOCATOR, time=2).text

    def get_counts_header(self):
        return self.find_element(locator=PageLocators.COUNT_HEADER_XPATH_LOCATOR, time=2).text

    def get_prices_header(self):
        return self.find_element(locator=PageLocators.PRICE_HEADER_XPATH_LOCATOR, time=2).text

    def get_actions_header(self):
        return self.find_element(locator=PageLocators.ACTION_HEADER_XPATH_LOCATOR, time=2).text

    def parse_table_header(self):
        return self.get_names_header(), self.get_counts_header(), self.get_prices_header(), self.get_actions_header()

    # CONTENT PARSING
    def get_name(self, n):
        name_xpath_locator = f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr[{n}]/td[1]"
        return self.find_element(locator=(By.XPATH, name_xpath_locator), time=1).text

    def get_count(self, n):
        count_xpath_locator = f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr[{n}]/td[2]"
        return self.find_element(locator=(By.XPATH, count_xpath_locator), time=1).text

    def get_price(self, n):
        price_xpath_locator = f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr[{n}]/td[3]"
        return self.find_element(locator=(By.XPATH, price_xpath_locator), time=1).text

    def get_actions(self, n):
        actions_xpath_locator = f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr[{n}]/td[4]"
        return tuple([action.text for action in self.find_elements(locator=(By.XPATH, actions_xpath_locator), time=1)])

    def get_record(self, n):
        return self.get_name(n), self.get_count(n), self.get_price(n), self.get_actions(n)

    def parse_table_content(self):
        content_xpath_locator = f"{PageLocators.TABLE_CONTENT_XPATH_LOCATOR[1]}/tr"
        return [self.get_record(i+1) for i in range(len(self.find_elements(locator=(By.XPATH, content_xpath_locator))))]

