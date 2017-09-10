import unittest
from parser import ReceivedHeaderParser, ReceivedHeader


class ParserTester(unittest.TestCase):
    def test_source_ip(self):
        header_parser = ReceivedHeaderParser()
        header_parser.push_header('from MTM0ODYxMA (115.114.61.139.static-Mumbai.vsnl.net.in [115.114.61.139]) by ismtpd0018p1sin1.sendgrid.net (SG) with HTTP id 2CAdZzmjSYqaj5-pIYcapA Sat, 27 May 2017 18:23:38.213 +0000 (UTC)')
        self.assertEqual(header_parser.get_source_ip(), ['115.114.61.139'])

    def test_source_ip1(self):
        header_parser = ReceivedHeaderParser()
        header_parser.push_header("""from mac.com ([10.13.11.252])\
         by ms031.mac.com (Sun Java System Messaging Server 6.2-8.04 (built Feb 28\
         2007)) with ESMTP id <0JMI007ZN7PETGC0@ms031.mac.com> for user@example.com; Thu,\
         09 Aug 2007 04:24:50 -0700 (PDT)""")
        self.assertEqual(header_parser.get_source_ip(), ['10.13.11.252'])


if __name__ == '__main__':
    pass