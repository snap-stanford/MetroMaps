import string

class StringProcessor():

    def __init__(self, in_encoding='UTF-8', encoding='UTF-8'):
        self.encoding = encoding
        self.in_encoding = in_encoding


    def encode(self, raw_string):
        if isinstance(raw_string, str):
            return unicode(raw_string.decode(self.in_encoding).encode(self.encoding),self.encoding)
        if isinstance(raw_string, unicode):
            return raw_string


    def clean(self, raw_string):
        encoded_string = self.encode(raw_string)
        encoded_string = encoded_string.lower()
        encoded_string = encoded_string.replace("'s", '')
        translate_table = {ord(char): None for char in string.punctuation + string.digits + string.whitespace}
        #import pdb; pdb.set_trace()
        encoded_string = encoded_string.translate(translate_table)
        return encoded_string
