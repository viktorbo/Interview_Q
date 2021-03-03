from task1_and_ui_tests.pages.checkme.helper import CheckmeHelper


class TestTask1_and_UI:

    def test_check_the_filling_of_the_table(self, log, chrome_driver, database):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        # LOADING checkme TABLE DATA TO THE SQLITE DATABASE
        table_header = checkme_site.parse_table_header()
        current_table_content = checkme_site.parse_table_content()

        db_table_name = 'checkme'
        db_table_columns = ['id', *table_header]
        db_table_columns_description = ['INTEGER PRIMARY KEY AUTOINCREMENT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT']

        database.create_table(table_name=db_table_name,
                              descripted_columns=dict(zip(db_table_columns, db_table_columns_description)))

        database.add_records(table_name=db_table_name,
                             columns_names=table_header,
                             val=current_table_content)
        log.info("TABLE CONTENT HAS BEEN LOADED TO DATABASE.")

        # ADDING SOME RECORDS TO THE TABLE ON THE SITE
        log.info("--- ADDING SOME RECORDS TO THE TABLE ---")
        new_table_records = [('Joja', 5, 100500), ('Lupa', 1, 777), ('Pupa', 2, 300)]
        checkme_site.add_table_records(new_table_records)
        current_site_table_content = checkme_site.parse_table_content()
        log.info(f"Records {new_table_records} were added to the checkme (site) table!")


        # DATABASE / SITE DATA COMPARISON
        log.info("--- DATABASE / SITE DATA COMPARISON ---")
        site_table_set = set(current_site_table_content)
        database_set = set([obj[1:] for obj in database.select_all('checkme')])

        log.info(f"Records in DATABASE, but NOT on the SITE: {list(database_set.difference(site_table_set))}")
        log.info(f"Records ON the SITE, but NOT in DATABASE: {list(site_table_set.difference(database_set))}")
        log.info(f"Duplicated records: {list(set.intersection(database_set, site_table_set))}")

        # INPUT DATA COMPARISON FOR SITE
        log.info("--- INPUT DATA COMPARISON ---")

        new_table_records_names = [obj[0] for obj in new_table_records]
        new_records_from_site = [obj[:-1] for obj in current_site_table_content if obj[0] in new_table_records_names]

        assert len(new_table_records) == len(new_records_from_site), \
            log.error("Count of new records in the checkme (site) don't equal the number of new records")

        for i in range(len(new_table_records)):
            if set(new_table_records[i]) == set(new_records_from_site[i]) and new_table_records[i] != new_records_from_site[i]:
                log.info(f"Columns order in new record {new_records_from_site[i]} don't match with original record {new_table_records[i]}")

    def test_check_add_record(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        origin_table_content = checkme_site.parse_table_content()

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)
        new_table_content = checkme_site.parse_table_content()

        assert set(set(new_table_content).difference(set(origin_table_content)).pop()[0:3]) == set(new_record), \
            log.error("Record added incorrectly or not added!")
        log.info("Record was added successfully!")

    def test_check_click_dicard_button(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        checkme_site.click_the_open_button()
        new_record = ('Joka', 200, 1000)
        checkme_site.enter_item_information(*new_record)
        checkme_site.click_the_discard_button()

        assert checkme_site.all_fields_is_empty(), log.error("Discard button doesn't work!")
        log.info("Discard button works!")

    def test_count_sorting_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        sorted_counts = sorted([checkme_site.get_count(i+1) for i in range(len(checkme_site.parse_table_content()))])
        checkme_site.click_the_counts_header()
        counts = [checkme_site.get_count(i+1) for i in range(len(checkme_site.parse_table_content()))]

        assert counts == sorted_counts, log.error("Sorting by count doesn't work!")
        log.info("Sorting by count works fine with original records.")

    def test_count_sorting_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)

        sorted_counts = sorted([checkme_site.get_count(i + 1) for i in range(len(checkme_site.parse_table_content()))])
        checkme_site.click_the_counts_header()
        counts = [checkme_site.get_count(i + 1) for i in range(len(checkme_site.parse_table_content()))]

        assert counts == sorted_counts, log.error("Sorting by count after adding record doesn't work!")
        log.info("Sorting by count works after adding a record.")

    def test_price_sorting_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        sorted_prices = sorted([checkme_site.get_price(i + 1) for i in range(len(checkme_site.parse_table_content()))])
        checkme_site.click_the_prices_header()
        prices = [checkme_site.get_price(i + 1) for i in range(len(checkme_site.parse_table_content()))]

        assert prices == sorted_prices, log.error("Sorting by price doesn't work!")
        log.info("Sorting by price works fine with original records.")

    def test_price_sorting_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)

        sorted_prices = sorted([checkme_site.get_price(i + 1) for i in range(len(checkme_site.parse_table_content()))])
        checkme_site.click_the_prices_header()
        prices = [checkme_site.get_price(i + 1) for i in range(len(checkme_site.parse_table_content()))]

        assert prices == sorted_prices, log.error("Sorting by price after adding record doesn't work!")
        log.info("Sorting by price works after adding a record.")

    def test_delete_record_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        del_index = 1

        table_content = checkme_site.parse_table_content()
        table_content.pop(del_index)

        checkme_site.click_the_delete_record(del_index+1)

        assert table_content == checkme_site.parse_table_content(), log.error("Another record was removed!")
        log.info("Record removing works correctly with original records.")

    def test_delete_record_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        del_index = 1

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)

        table_content = checkme_site.parse_table_content()
        table_content.pop(del_index)

        checkme_site.click_the_delete_record(del_index+1)

        assert table_content == checkme_site.parse_table_content(), log.error("Another record was removed!")
        log.info("Record removing works correctly after adding a record.")

    def test_delete_new_record(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)

        table_content = checkme_site.parse_table_content()
        del_index = len(table_content)
        table_content.pop(del_index-1)

        checkme_site.click_the_delete_record(del_index)

        assert len(checkme_site.parse_table_content()) == len(table_content), log.error("The last added record wasn't removed!")
        log.info("New record was removed.")

