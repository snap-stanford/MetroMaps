
class StringProcessor():

    def __init__(self, encoding='UTF-8'):
        self.encoding = encoding



    def clean(self, raw_string):
        isinstance(raw_string, str):
            return unicode(raw_string, self.encoding)
        isinstance(raw_string, unicode):
            return raw_string


    def clean_string(str):

        exclude = []