import json
from stringprocessor import StringProcessor

class WhiteListCounter():

    # @classmethod
    # def FactoryFromConfig(cls, config):
    #     whitelist = config.get('whitelist')
    #     if not whitelist:
    #         raise ConfigParser.NoOptionError('whitelist','input_helper')


    #     total_counts_filename = config.get('total_counts_filename')
    #     docname_to_id_filename = config.get('doc_counts_filename')
    #     token_to_id_filename = config.get('token_to_id_filename')

    #     total_counts_json = {}
    #     docname_to_id_json = {}
    #     token_to_id_json = {}
    #     if total_counts_filename:
    #         with open(total_counts_filename) as f:
    #             total_counts_json = json.load(f)
    #     if docname_to_id_filename:
    #         with open(docname_to_id_json) as f:
    #             docname_to_id_json = json.load(f)
    #     if token_to_id_filename:
    #         with open(token_to_id_filename) as f:
    #             token_to_id_json = json.load(f)
        
    #     return WhiteListCounter(whitelist.get('whitelist'), total_counts=total_counts_json.get('total_counts', {}), ...
    #         docname_to_id=docname_to_id_json.get('docname_to_id',{}), token_to_id_json.get('token_to_id', {}), config=config)

    def _read_whitelist(self, whitelist_filename):
        l = []
        with open(whitelist_filename) as f:
            for line in f:
                l += [line.strip().lower()]
        return set(l)

    # def __get_default_out_format(self):
    #     formats = {
    #         "global_tokens" : 'global_tokens.json'
    #         "representative_tokens" : 'representative_tokens.json'
    #         "stem_doc_counts" : 'stem_doc_counts'

    #     }
        

    def __init__(self,whitelist,out_formats,input_directory,threads=1,name='whitelistcounter',encoding='UTF-8'):
        self.whitelist = self._read_whitelist(whitelist)
        self.out_formats = out_formats
        self.input_directory = input_directory
        self.token_to_id = {}
        self.docname_to_id = {}
        self.total_counts = {}
        self.doc_counts = {}
        self.stringprocessor = StringProcessor(encoding)
    
    def run_filename(self, filename):
        with open(filename) as fi:
            for line in fi:
                line = line.strip()
                
                for word in line.split():
                    word = self.stringprocessor.clean(word)
                    word_id = _get_token_id(self, word)
                        
    def run(self):
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            self.run_filename(full_path)

    def toJSON(self, stream):
        # returns four fields : "total_counts", "doc_counts", and "token_to_id" and "docname_to_id"
        raise NotImplementedError('to json not yet supported')

    def _get_token_id(self, token, fail_on_none=False):
        token_id = self.token_to_id.get(token)
        if not token_id:
            token_id = self._next_token_id
            self.token_to_id_filename[token] = token_id
            self._next_token_id += 1

        return token_id

    def _count_word(self, word_id, doc_id=None):
        current_count = self.total_counts.get(word_id, 0)
        self.total_counts[word_id] = current_count + 1
        if doc_id:
            current_doc_counts = self.doc_counts.get(doc_id, {})
            current_word_in_doc = current_doc_counts.get(word_id, 0)
            current_doc_counts[word_id] = current_word_in_doc + 1
            self.doc_counts[doc_id] = current_doc_counts

    def _get_doc_id(self, doc, fail_on_none=False):
        doc_id = self.docname_to_id.get(token)
        if not doc_id:
            doc_id = self._next_doc_id
            self._next_doc_id += 1
        return doc_id

    def run(self):
        if self.config.get('input_file'):
            self.run_filename(self.config.get('input_file'))

        if self.config.get('input_dir'):
            self.run_dir(self.config.get('input_dir'))

    def run_filename(self, filename):
        # Specify filename to count tokens in that file. 
        with open(filename) as fi:
            for line in fi:
                line_enc = unicode(line, "UTF-8")
                for word in line.split():
                    word = self.stringprocessor.clean(word)
                    word_id = _get_token_id(self, word)
                    


        pass
    def run_dir(self, dirname):
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            run_filename(full_path)
    
def construct(config):
    return WhiteListCounter(**config)