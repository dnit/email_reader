This code hase been tested on Python 2.7

Following are the steps to setup a demo:

Assuming you have virtual environment setup, if not install it

    pip install virtualenv

Create a virtual environment

    virtualenv myenv
    source myenv/bin/activate

Install dependencies

    pip install -r requirements.txt

Getting started

    from email_reader.clients import GmailReader
    reader = GmailReader('yourgmailid', 'yourpassword')
    reader.select_category('inbox') #select category
    mail = reader.get_mail(mail_id) # eg reader.get_mail(100)

    mail.download_attachments()
    mail.get_downloaded_resources_path() # download resource path before downloading will return empty []
    mail.get_urls_from_body()
    mail.source_ip
