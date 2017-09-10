import unittest
from clients import MailObject


class MailTest(unittest.TestCase):
    content = """Return-path: <user@example.com>
Received: from mac.com ([10.13.11.252]) by ms031.mac.com (Sun Java System Messaging Server 6.2-8.04 (built Feb 28  2007)) with ESMTP id <0JMI007ZN7PETGC0@ms031.mac.com> for user@example.com; Thu,  09 Aug 2007 04:24:50 -0700 (PDT)
Received: from mail.dsis.net (mail.dsis.net [70.183.59.5]) by mac.com (Xserve/smtpin22/MantshX 4.0) with ESMTP id l79BOnNS000101 for <user@example.com>; Thu, 09 Aug 2007 04:24:49 -0700 (PDT)
Received: from [192.168.2.77] (70.183.59.6) by mail.dsis.net with ESMTP (EIMS X 3.3.2) for <user@example.com>; Thu, 09 Aug 2007 04:24:49 -0700
Date: Thu, 09 Aug 2007 04:24:57 -0700
From: Frank Sender <sender@example.com>
Subject: Test
To: Joe User <user@example.com>
Message-id: <61086DBD-252B-46D2-A54C-263FE5E02B41@example.com>
MIME-version: 1.0 (Apple Message framework v752.2)
X-Mailer: Apple Mail (2.752.2)
Content-type: text/plain; charset=US-ASCII; format=flowed
Content-transfer-encoding: 7bit"""
    mail = MailObject(mail_id=1, data=content)

    def test_source_ip(self):
        self.assertIn('70.183.59.6', self.mail.source_ip)

    def test_source_ip2(self):
        mail = MailObject(mail_id=1, data=self.content.replace('70.183.59.6', ''))

        self.assertIn('192.168.2.77', mail.source_ip)
        self.assertEqual(1, len(mail.source_ip))

