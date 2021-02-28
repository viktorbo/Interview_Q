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