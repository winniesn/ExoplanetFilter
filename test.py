import unittest
import TestSheet.drop_duplicates as ed


class WinnieTestCase(unittest.TestCase):

    dd = ed.DropDuplicates()

    def test_step1(self):
        self.dd.make_histogram()

    def test_step2(self):
        self.dd.random_stuff()

    def test_step3(self):
        self.dd.drop_missing()

    def test_step4(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()

    def test_step5(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()
        self.dd.convert_to_dt()

    def test_step6(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()
        self.dd.convert_to_dt()
        self.dd.sort_data()

    def test_step7(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()
        self.dd.convert_to_dt()
        self.dd.sort_data()
        self.dd.store_duplicates()

    def test_step8(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()
        self.dd.convert_to_dt()
        self.dd.sort_data()
        self.dd.store_duplicates()
        self.dd.drop_duplicates()

    def test_step9(self):
        self.dd.drop_missing()
        self.dd.drop_bad_data()
        self.dd.convert_to_dt()
        self.dd.sort_data()
        self.dd.store_duplicates()
        self.dd.drop_duplicates()
        self.dd.show_de_duped_data()