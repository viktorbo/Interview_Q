from ui_tests.pages.checkme.helper import CheckmeHelper


class TestTask1_and_UI:

    def test_task_1(self, log, chrome_driver, database):
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

        new_record = ('Joka', 200, 1000)
        checkme_site.add_table_record(*new_record)
        log.info(f"Record {new_record} has been added to table.")

        table_content = checkme_site.parse_table_content()
        log.info(f"Current table content: {table_content}")

        assert new_record in [obj[0:3] for obj in table_content], \
            log.error("Record added incorrectly or not added!")
        log.info("Record was added successfully!")

    def test_check_click_discard_button_form(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        checkme_site.click_the_open_button()
        new_record = ('Joka', 200, 1000)
        log.info(f"Fill the new record form fields: {new_record}")
        checkme_site.enter_item_information(*new_record)

        log.info("Click the discard button...")
        checkme_site.click_the_discard_button()

        assert checkme_site.all_fields_is_empty(), log.error("Discard button doesn't work for 'add new record' form. "
                                                             "Form is not empty!")
        log.info("Discard button works correctly for 'add new record' form!")

    def test_check_click_discard_button_table(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        original_table_content = checkme_site.parse_table_content()
        log.info(f"Original table content: {original_table_content}")

        new_record = ('Joka', 200, 1000)
        log.info(f"Adding record {new_record} to the table ...")
        checkme_site.add_table_record(*new_record)

        log.info("Click the discard button...")
        checkme_site.click_the_discard_button()

        new_table_content = checkme_site.parse_table_content()
        log.info(f"New table content: {new_table_content}")

        assert original_table_content == new_table_content, log.error("Discard button doesn't work for table content!")
        log.info("Discard button works for table content!")

    def test_count_sorting_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        before_sortig_content = checkme_site.parse_table_content()
        log.info(f"Content before sorting: {before_sortig_content}")

        log.info("Click the count header...")
        checkme_site.click_the_counts_header()

        after_sorting_content = checkme_site.parse_table_content()
        log.info(f"Content after sorting: {after_sorting_content}")

        assert sorted(before_sortig_content, key=lambda x: x[1]) == after_sorting_content, log.error("Sorting by count works incorrectly!")
        log.info("Sorting by count works correctly with original records.")

    def test_count_sorting_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        before_sortig_content = checkme_site.parse_table_content()
        log.info(f"Content before sorting: {before_sortig_content}")

        new_record = ('Joka', 200, 1000)
        log.info(f"Adding record {new_record} to the table ...")
        checkme_site.add_table_record(*new_record)

        log.info("Click the count header...")
        checkme_site.click_the_counts_header()

        after_sorting_content = checkme_site.parse_table_content()
        log.info(f"Content after sorting: {after_sorting_content}")

        assert sorted(before_sortig_content, key=lambda x: x[1]) == after_sorting_content, log.error("Sorting by count works incorrectly after adding a record!")
        log.info("Sorting by count works correctly after adding a record.")

    def test_price_sorting_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        before_sortig_content = checkme_site.parse_table_content()
        log.info(f"Content before sorting: {before_sortig_content}")

        log.info("Click the price header ...")
        checkme_site.click_the_prices_header()

        after_sorting_content = checkme_site.parse_table_content()
        log.info(f"Content after sorting: {after_sorting_content}")

        assert sorted(before_sortig_content, key=lambda x: x[2]) == after_sorting_content, log.error("Sorting by price works incorrectly!")
        log.info("Sorting by price works correctly with original records.")

    def test_price_sorting_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        before_sortig_content = checkme_site.parse_table_content()
        log.info(f"Content before sorting: {before_sortig_content}")

        new_record = ('Joka', 200, 1000)
        log.info(f"Adding record {new_record} to the table ...")
        checkme_site.add_table_record(*new_record)

        log.info("Click the price header...")
        checkme_site.click_the_prices_header()

        after_sorting_content = checkme_site.parse_table_content()
        log.info(f"Content after sorting: {after_sorting_content}")

        assert sorted(before_sortig_content, key=lambda x: x[2]) == after_sorting_content, log.error("Sorting by price works incorrectly after adding a record!")
        log.info("Sorting by price works correctly after adding a record.")

    def test_delete_record_origin(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        del_index = 1

        table_content = checkme_site.parse_table_content()
        log.info(f"Original table content: {table_content}")

        table_content.pop(del_index)
        log.info(f"Expected table content after removing the record number {del_index+1}: {table_content}")

        checkme_site.click_the_delete_record(del_index+1)
        new_table_content = checkme_site.parse_table_content()
        log.info(f"Table content after removing the record number {del_index+1}: {new_table_content}")

        assert table_content == new_table_content, log.error("Record removing works incorrectly!")
        log.info("Record removing works correctly for original records.")

    def test_delete_record_add(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        del_index = 1

        new_record = ('Joka', 200, 1000)
        log.info(f"Adding record {new_record} to the table ...")
        checkme_site.add_table_record(*new_record)

        table_content = checkme_site.parse_table_content()
        log.info(f"Original table content: {table_content}")

        table_content.pop(del_index)
        log.info(f"Expected table content after removing the record number {del_index + 1}: {table_content}")

        checkme_site.click_the_delete_record(del_index + 1)
        new_table_content = checkme_site.parse_table_content()
        log.info(f"Table content after removing the record number {del_index + 1}: {new_table_content}")

        assert table_content == new_table_content, log.error("Record removing works incorrectly after adding a record!")
        log.info("Record removing works correctly after adding a record.")

    def test_delete_new_record(self, log, chrome_driver):
        checkme_site = CheckmeHelper(driver=chrome_driver)
        checkme_site.go_to_site()

        new_record = ('Joka', 200, 1000)
        log.info(f"Adding record {new_record} to the table ...")
        checkme_site.add_table_record(*new_record)

        table_content = checkme_site.parse_table_content()
        log.info(f"Original table content: {table_content}")

        del_index = len(table_content)

        table_content.pop(del_index-1)
        log.info(f"Expected table content after removing the record number {del_index}: {table_content}")

        checkme_site.click_the_delete_record(del_index)
        new_table_content = checkme_site.parse_table_content()
        log.info(f"Table content after removing the record number {del_index}: {new_table_content}")

        assert table_content == new_table_content, log.error("Record removing works incorrectly! "
                                                             "The new record hasn't been removed!")
        log.info("Record removing works correctly. The new record has been removed.")

