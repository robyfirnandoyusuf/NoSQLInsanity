import requests
import random
import string
from collections.abc import MutableMapping
from urllib.parse import urlencode, unquote
import urllib.parse
from urllib.parse import unquote
import socket
import csv

class Switch:
    def __init__(self, value):
        self.value = value
        self._entered = False
        self._broken = False
        self._prev = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False # Allows a traceback to occur

    def __call__(self, *values):
        if self._broken:
            return False
        
        if not self._entered:
            if values and self.value not in values:
                return False
            self._entered, self._prev = True, values
            return True
        
        if self._prev is None:
            self._prev = values
            return True
        
        if self._prev != values:
            self._broken = True
            return False
        
        if self._prev == values:
            self._prev = None
            return False
    
    @property
    def default(self):
        return self()
    
class WebAppTester:
    def __init__(self, url):
        self.url = url
    
    def is_up(self):
        """ This function checks to see if a host name has a DNS entry by checking
        for socket info. If the website gets something in return, 
            we know it's available to DNS.
        """
        try:
            requests.get(self.url)
            return True
        except requests.exceptions.ConnectionError:
            return False


class Str:
    def __enter__(self):
        return self
    # @staticmethod
    def randStr(length):
        if (length is None):
            length = 6
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
    def http_build_query(params):
        """
        Converts a dictionary of parameters to a URL-encoded string.
        """
        return unquote(urllib.parse.urlencode(params))
        # parsed_url = urlparse(params)
        # return parse_qs(parsed_url.query)
        
    def iterateParam(form_data, val):
        for element in form_data:
                if "$regex" in element:
                    form_data[element] = val
                    
class CsvWriter:
    def __init__(self, file_path, header=None):
        self.file_path = file_path
        self.header = header
        
        # Write header row if file is empty and header is provided
        if self.header is not None:
            with open(self.file_path, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                with open(self.file_path, 'r', newline='') as csv_file_read:
                    csv_reader = csv.reader(csv_file_read)
                    if not any(csv_reader):
                        csv_writer.writerow(self.header)

    def append_row(self, content):
        with open(self.file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
            
    def writeCsv(nsi, value, isKnownValue=False):
        headers = []
        knownValue = ""
        rows = []
        
        if (isKnownValue):
            for item in nsi.params:
                headers.append(item.split(':')[0].replace('*', ''))
                if (":" in item):
                    knownValue = item.split(':')[1]
                    rows.append(knownValue)
                else:
                    rows.append(value)
        else:
            for item in nsi.params:
                if ("*" in item):
                    headers.append(item.split(':')[0].replace('*', ''))
                    rows.append(value)
        
        csv_writer = CsvWriter('my_file.csv', headers)
        csv_writer.append_row(rows)