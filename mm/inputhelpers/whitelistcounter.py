import json
import utils

class WhiteListCounter():
    def __init__(self, whitelist):
        self.whitelist = whitelist
        self.token_to_id = {}
        self.docname_to_id = {}
        self.total_counts = {}
        self.doc_counts = {}

    def toJSON(stream, tokenToID={}, docnameToID={}):
        # returns four fields : "total_counts", "doc_counts", and "token_to_id" and "docname_to_id"

        next_key_id = max(tokenToID.values())+1 if len(tokenToID) > 0 else 0
        next_doc_id = max(docnameToID.values()+1 if len(docnameToID) > 0 else 0)
        def next_key_id():
            nk = next_key_id
            next_key_id += 1
            return nk
        def next_doc_id():
            nd = next_doc_id
            next_doc_id += 1

        out_total_counts = {}
        for key in self.total_counts:
            key_id = tokenToID.get(key)
            if not key_id:
                key_id = next_key_id()
                tokenToID[key] = key_id

            current_count = out_total_counts.get(key_id) 
            out_total_counts[key_id] = current_count + 1 if current_count else 1

        out_doc_counts = {}
        for key in self.doc_counts:


        
    def run_filename(filename):
        with open(filename) as fi:
            for line in fi:
                for word in line.split():

        pass
    def run_dir():
        pass

    
