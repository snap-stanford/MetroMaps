import string

class StringProcessor():

    def __init__(self, encoding='UTF-8'):
        self.encoding = encoding



    def encode(self, raw_string):
        
        if isinstance(raw_string, str):
            return unicode(raw_string, self.encoding)
        if isinstance(raw_string, unicode):
            return raw_string


    def clean(raw_string):
        encoded_string = encode(raw_string)
        exclude = string.punctuation + string.digits
        encoded_string = encoded_string.lower()
        encoded_string = encoded_string.replace("'s", '')
        encoded_string = encoded_string.translate(None, exclude)
        return encoded_string