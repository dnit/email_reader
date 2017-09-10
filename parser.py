import re

FROM_HEADER = 'from'
TO_HEADER = 'to'


class ReceivedHeader(object):
    from_pattern = r'^from (?P<source_info>.*) by (?P<hop_info>.*) with (?P<proto_details>.*)'
    to_pattern = r'by (?P<server>.*) with (?P<proto_details>.*)'

    def __init__(self, raw_header_value, time):
        self.time = time
        self.header_type = ''
        self.from_host = ''
        self.host = ''
        self.from_proto = ''
        self.host_proto = ''
        self.parse(raw_header_value)

    def parse(self, val):
        if val.startswith('from'):
            self.header_type = FROM_HEADER
            match = re.search(self.from_pattern, val)
            self.from_host = match.group('source_info')
            self.host = match.group('hop_info')
            self.host_proto = match.group('proto_details')

        elif val.startswith('to'):
            self.header_type = TO_HEADER
            match = re.search(self.from_pattern, val)
            self.host = match.group('server')
            self.host_proto = match.group('proto_details')
        else:
            Exception('Not a valid Received email header, must start with either `from` or `to`')


class ReceivedHeaderParser(object):
    """
    This object is to be used for header of same email only
    """
    IPv4_like_pattern_in_header = r'[\[\(](?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\]\)]'

    def __init__(self):
        self.headers = []

    def push_header(self, header):
        parts = header.split(';')
        data = parts[0]
        timeinfo = None
        if len(parts) > 1:
            timeinfo = parts[1]

        header = ReceivedHeader(data, timeinfo)
        self.headers.append(header)

    def get_source_ip(self):
        # last from header contains source ip
        # TODO: In future might get IPv6
        source_ip = ''
        for header in self.headers:
            if header.header_type == FROM_HEADER:
                source_ip = re.findall(self.IPv4_like_pattern_in_header, header.from_host)

        return source_ip
