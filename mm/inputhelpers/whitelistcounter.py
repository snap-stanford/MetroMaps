import json
from stringprocessor import StringProcessor
import os
import os.path
import logging



class WhiteListCounter():
    def __init__(self,mode, whitelist,out_config,input_directory,threads=1,name='whitelistcounter',in_encoding='UTF-8', encoding='UTF-8'):
        self.sp = StringProcessor(in_encoding, encoding)
        self.out_config = out_config
        self.input_directory = input_directory
        self.token_to_id = {}
        self.docname_to_id = {}
        self.total_counts = {}
        self.doc_counts = {}
        self.plainword_counts = {}
        self.whitelist = self._read_whitelist(whitelist)
        self.synonyms = {} # id to {word: count}
        self._next_token_id = 1
        self._next_doc_id = 1


    def _read_whitelist(self, whitelist_filename):
        l = []
        with open(whitelist_filename) as f:
            for line in f:
                l += [self.sp.clean(line)]
        return set(l)


    def _count_word(self, word_id,  doc_id=None, word_plain=None,):
        current_count = self.total_counts.get(word_id, 0)
        self.total_counts[word_id] = current_count + 1
        if doc_id:
            current_doc_counts = self.doc_counts.get(doc_id, {})
            current_word_in_doc = current_doc_counts.get(word_id, 0)
            current_doc_counts[word_id] = current_word_in_doc + 1
            self.doc_counts[doc_id] = current_doc_counts
        if word_plain:
            synonym_counts = self.synonyms.get(word_id,{})
            current_count_count = synonym_counts.get(word_plain,0)
            synonym_counts[word_plain] = current_count_count + 1
            self.synonyms[word_id] = synonym_counts
            
            



    def run_filename(self, filename):
        with open(filename) as fi:
            doc_id = self._get_doc_id(filename)
            for line in fi:
                line = line.strip()
                for dirty_word in line.split():
                    
                    word = self.sp.clean(dirty_word)
                    if word in self.whitelist:
                        word_id = self._get_token_id(word)
                        self._count_word(word_id, doc_id, dirty_word)
    def run(self):

        filenames = os.listdir(self.input_directory)
        logging.debug('Processing %i files' % (len(filenames)))
        for filename in filenames:
            full_path = os.path.join(self.input_directory, filename)
            self.run_filename(full_path)

    def _get_representative_tokens(self):
        # reverse token_to_id with the counts from global counts


        return {v: k for k,v in self.token_to_id.items()}
    
    def save(self):
        together = self.out_config.get("together", {})
        separated = self.out_config.get("separated", {})
        legacy = self.out_config.get("legacy", {})
        
        

        if together.get('mode',None)==True:
           # return all of the data into one big dictionary
            together_out = together["outfile"]
            with open(together_out,'w') as out_file:
                d={}
                d['global_tokens'] = self.token_to_id
                d['global_counts'] = self.total_counts
                d['representative_tokens'] = self.synonyms
                d['doc_counts'] = self.doc_counts
                json.dump(d, out_file)
        if separated.get('mode', None)==True:
            separated_tokens_out = separated['outfile_global_tokens']
            separated_global_counts_out = separated['outfile_global_counts']
            separated_doc_counts = separated['outfile_doc_counts']
            separated_representative_tokens = separated['outfile_representative_tokens']

            with open(separated_tokens_out,'w') as out_file:
                json.dump(self.token_to_id, out_file)
            with open(separated_global_counts_out,'w') as out_file:
                json.dump(self.total_counts, out_file)
            with open(separated_doc_counts,'w') as out_file:
                json.dump(self.doc_counts, out_file)
            with open(separated_representative_tokens, 'w') as out_file:
                json.dump(self.synonyms, out_file)
        logging.debug('WhiteList Counter: Dump of data complete')
            

    def _get_token_id(self, token, fail_on_none=False):
        token_id = self.token_to_id.get(token)
        if not token_id:
            token_id = self._next_token_id
            self.token_to_id[token] = token_id
            self._next_token_id += 1
        return token_id

    

    def _get_doc_id(self, doc, fail_on_none=False):
        doc_id = self.docname_to_id.get(doc)
        if not doc_id:
            doc_id = self._next_doc_id
            self._next_doc_id += 1
        return doc_id

    '''
    def run(self):
        if self.input_directory:
            self.run_dir(self.input_directory)
    '''
    '''
    def run_filename(self, filename):
        # Specify filename to count tokens in that file. 
        with open(filename) as fi:
            doc_id = _get_doc_id(filename)
            for line in fi:
                for word in line.split():
                    if word == "Bilbo":
                        print 'hoorah'
                        print self.sp.clean(word)
                    word = self.sp.clean(word)
                    word_id = self._get_token_id(self, word)
                    _count_word(word_id, 
    '''              
    '''j
    def run_dir(self, dirname):
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            self.run_filename(full_path)
   ''' 
def construct(config):
    return WhiteListCounter(**config)
