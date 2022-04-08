import unittest
from s3_object import S3_object
from s3_object import outcome

class Test_Upload_S3(unittest.TestCase):

    def setUp(self) -> None:
        self.s3_object = S3_object(test=True)

    def test_missing_asset(self):
        with self.assertRaises(FileNotFoundError):
            self.s3_object.upload_s3('bogus', 'bogus')

    def test_directory_only(self):
        with self.assertRaises(KeyError):
            self.s3_object.upload_s3('./tests/test_data', 'bogus')

    def test_directory_with_files(self):
        self.assertEquals(outcome.SINGLETARGET, self.s3_object.upload_s3('./tests/test_data/test_file.csv', 'bogus'))

    def test_director_with_wild_card(self):
        self.assertEquals(outcome.MULTITARGET, self.s3_object.upload_s3('./tests/test_data/*.csv', 'bogus'))
    


if __name__ == '__main__':
    unittest.main()