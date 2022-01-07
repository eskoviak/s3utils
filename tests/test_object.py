import unittest
import object
from pathlib import Path

class Test_Upload_S3(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()


    def test_missing_asset(self):
        with self.assertRaises(FileExistsError):
            object.upload_s3('bogus', 'bogus')

    def test_directory(self):
        #file_list = (object.upload_s3('~/iCloud/Downloads/Weight History', None))
        #self.assertIsNotNone((object.upload_s3('~/iCloud/Downloads/Weight History', None))) 
        self.assertIsNotNone((object.upload_s3('~/iCloud/Downloads/Empty', None))) 

    #def test_directory_with_files(self):
    #    self.assertEqual(2, object.upload_s3('~/iCloud/Downloads/Weight History/*.csv', None))


if __name__ == '__main__':
    unittest.main()