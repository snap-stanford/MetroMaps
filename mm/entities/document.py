class Document:
    def __init__(self):
        self.name = 'untitled'
        self.link = '#'
        self.id = 0
        self.timestamp = 0

    @property
    def tfidf(self):
        pass

    def toJSON(self):
        raise NotImplemented

    def fromJSON(self):
        raise NotImplemented