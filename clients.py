import email
import imaplib
import re
from helper import FileSaver
from parser import ReceivedHeaderParser


class MailObject(object):

    def __init__(self, mail_id, data):
        self.mail_id = mail_id
        self.data = email.message_from_string(data)
        self._source_ip = None
        self._embedded_urls = None
        self._downloaded_resources = None
        self.downloader = FileSaver()
        self.received_parser = ReceivedHeaderParser()

    @property
    def source_ip(self):
        if self._source_ip is None:
            for header, val in self.data._headers:
                if header == 'Received':
                    self.received_parser.push_header(val)
            self._source_ip = self.received_parser.get_source_ip()

        return self._source_ip

    def get_urls_from_body(self):
        if self._embedded_urls is None:
            url_pattern = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]?'
            urls = []
            if self.data.is_multipart():
                for msg in self.data.get_payload():
                    content = msg.get_payload(decode=True)
                    if content:
                        urls.extend(re.findall(url_pattern, content))
            else:
                msg = self.data.get_payload(decode=True)
                urls.extend(re.findall(url_pattern, msg))
            self._embedded_urls = urls

        return self._embedded_urls

    def download_attachments(self):
        for part in self.data.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()

            if file_name:
                self.downloader.download(file_name, str(self.mail_id), part.get_payload(decode=True))

    def get_downloaded_resources_path(self):
        return self.downloader.resources_path


class MailReader(object):
    status_ok = 'OK'

    def __init__(self, smtp_server, email_id, password, smtp_class=imaplib.IMAP4_SSL, *args, **kwargs):
        self.smtp_server = smtp_server
        self.mail_class = smtp_class
        self.mailer = None
        self.args = args
        self.kwargs = kwargs
        self.login(email_id, password)

    def login(self, email_id, password):
        try:
            mailer = self.mail_class(self.smtp_server)
            mailer.login(email_id, password)
        except Exception as e:
            raise e
        else:
            self.mailer = mailer

    def select_category(self, cat):
        self.mailer.select(cat)

    def get_mail(self, mail_id):
        status, data = self.mailer.fetch(mail_id, '(RFC822)')
        if status == self.status_ok and data:
            return MailObject(mail_id=mail_id, data=data[0][1])
        # TODO : handle data for invalid status
        return MailObject(mail_id=mail_id, data='')

    def valid_email_ids(self):
        status, data = self.mailer.search(None, 'ALL')
        mail_ids = data[0]
        return mail_ids.split()


class GmailReader(MailReader):
    def __init__(self, emailid, password):
        super(GmailReader, self).__init__(smtp_server='imap.gmail.com', email_id=emailid, password=password)


if __name__ == '__main__':
    pass
