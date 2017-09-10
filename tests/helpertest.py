import unittest
from helper import is_valid_ipv4, FileSaver


class IPv4Test(unittest.TestCase):

    def test_invalid(self):
        invalid_ips = ['0.0.0.a.', '1.1.1.01', '.1.1.1', '257.1.1.1']

        for ip in invalid_ips:
            self.assertFalse(is_valid_ipv4(ip))

    def test_valid(self):
        valid_ips = ['255.255.255.255', '19.0.1.3', '0.0.0.0']
        for ip in valid_ips:
            self.assertTrue(is_valid_ipv4(ip))


class FileSavingTest(unittest.TestCase):

    def test_downloader(self):
        # with open('/home/nitesh/Desktop/fcm_test.py', 'r') as f:

        filesaver = FileSaver()
        content = b'jjj'

        filesaver.download('new', 'tt', content)
        self.assertEquals(filesaver.resources_path[0].split('/')[-1], 'new')

        # should not overwrite
        filesaver1 = FileSaver()
        filesaver1.download('new', 'tt', content, overwrite=False)
        self.assertEquals(filesaver1.resources_path, [])
