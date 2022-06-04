from unittest import TestCase

import import_from_root
from src.file_reader import FileReader


class TestFileReader(TestCase):
    def test_add_file(self):
        f = FileReader('pins', 'test_file.json')
        f.add_file('cos', 'test_file.json')
        obj = {'pins': 'test_file.json', 'cos': 'test_file.json'}
        self.assertEqual(f.get_files_dictionary(), obj)
        self.assertRaises(Exception, f.add_file, 'file')

    def test_del_file(self):
        f = FileReader('pins', 'test_file.json')
        f.del_file('pins')
        self.assertEqual(f.get_files_dictionary(), {})
        f.add_file('cos1', 'test_file.json')
        f.add_file('cos2', 'test_file.json')
        f.del_file('cos1')
        self.assertEqual(f.get_files_dictionary(), {'cos2': 'test_file.json'})
        self.assertRaises(KeyError, f.del_file, 'cos3')

    def test_get_data(self):
        f = FileReader('pins', 'test_file.json')
        obj = {'pin1': 1, 'pin2': 2, 'pin3': 3}
        self.assertEqual(f.get_data('pins'), obj)
        self.assertRaises(KeyError, f.get_data, 'file')
