mm
==

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.


#Configuration Specs
##Legacy Helper

Config file contains few field `input_json_file:`, `doc_metadata`, `output_dir`, `num_clusters`

    * `global_tokens` (name -> id)
    * `global_counts` (id -> counts)
    * `doc_counts` (docid -> [(token_id -> count), (token_id -> count))



self.global_tokens = self.data['global_tokens']
        self.global_counts = self.data['global_counts']
        self.doc_counts = self.data['doc_counts']
        self.num_clusters = self.data['num_clusters']
        self.doc_metadata = self.data['doc_metadata']
        self.max_token_counts, self.num_docs_with_term = token_stats(self.doc_counts)
        self.num_docs = len(doc_counts)

#Input Data

The input to Metromaps consists of several parts:

* global tokens : dictionary from "some word" : id
* global counts : dictionary from tokenID : total counts
* doc metadata : list, each element of which is
  * timestamp (string, that defines a strict ordering if the string is ordered like an int)
  * id
  * filename
* doc counts: dictionary from doc id -> tokenID(s) -> counts in the doc

The above fields are read (if available) from one file called "master_input.json" with the key of json data defined as above, but with spaces replaced by underscores ("global_tokens", "global_counts") and then replaced by any individual json files. 

# Output
