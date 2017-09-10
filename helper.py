import re
import os
import errno


def is_valid_ipv4(ip_string):
    if not re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_string):
        return False

    for num in ip_string.split('.'):
        if len(num) > 1 and num.startswith('0'):
            return False
        elif 0 <= int(num) <= 255:
            continue
        else:
            return False

    return True


class FileSaver(object):
    base_dir = os.path.join(os.getcwd(), 'attachments')

    def __init__(self):
        self.resources_path = []

    def download(self, filename, foldername, content, overwrite=True):
        folderpath = os.path.join(self.base_dir, foldername)

        filepath = os.path.join(folderpath, filename)

        if os.path.exists(filepath) and not overwrite:
            return

        try:
            os.makedirs(folderpath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        with open(filepath, 'wb') as fp:
            fp.write(content)

        self.resources_path.append(filepath)


if __name__ == '__main__':
    pass
