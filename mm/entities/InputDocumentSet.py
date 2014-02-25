class InputDocumentSet():


    def __init__(self, dirname, doc_metadata, input_helper_class, doc_class):
        self.dirname = dirname
        self.input_helper_class = input_helper_class
        self.doc_class = doc_class
        self.doc_list = os.listdir(dirname)


    @property
    def size(self):
        return len(doc_list)
