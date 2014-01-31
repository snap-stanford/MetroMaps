
class StringProcessor():

    def __init__(self, encoding='UTF-8'):
        self.encoding = encoding



    def clean(self, raw_string):
        raw_string = raw_string.lower()
        if isinstance(raw_string, str):
            return unicode(raw_string, self.encoding)
        if isinstance(raw_string, unicode):
            return raw_string


    def clean_string(str):

        exclude = []