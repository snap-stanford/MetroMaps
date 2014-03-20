Metromaps
=========

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.

# Version
0.1.1


# Install
Metromaps is fueled by Python 2.7. If you are running on MAC OS X, make sure you have the [brew version] of Python. 

You will need [networkx], soon to be migrated to [SNAP] in 1.0.0(stay tuned). You might also want to get [nltk] but it's not required for basic functionality.	

Once you have these packages, just clone this github repository! Write to us if you have any problems.

[networkx]: http://networkx.github.io/
[SNAP]: http://snap.stanford.edu/snap/index.html
[nltk]: http://www.nltk.org/
[brew version]: http://docs.python-guide.org/en/latest/starting/install/osx/

#Configuration Specs

##Legacy Helper

Config file contains few fields, `mode` (on or off), `input_json_file`, `doc_metadata`, `output_dir`, `num_clusters`. 

`input_json_file` should contain:

    * `global_tokens` (name -> id)
    * `global_counts` (id -> counts)
    * `doc_counts` (docid -> [(token_id -> count), (token_id -> count))
    * `representative_tokens` {id -> {synonym: count, synonym2:count }}

Legacy Helper outputs JSON in the following format:

     [{"cluster_end_date":'date', "cluster_start_date", "doc_data": [{"doc_metadata": "id", "name", "timestamp"}, "tokens": [{"id", "plaintext", "score", "token_doc_count"}]]


##Clustering





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


