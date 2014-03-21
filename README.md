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

#Handling Input

MM is customized by specifying a configuration file at input. The fields that can be edited are in `mm/default.yaml`.

#Writing your own `input_handler:`
Make sure that your input handler returns the following fields:

    * 'doc_counts' (docid -> [(token_id -> count), (token_id -> count))
    * 'global_counts' (token_id -> global_count)
    * 'global_tokens' (word -> token_id) # good idea to use the same id for words with the same stem
    * 'representative_tokens' (token_id -> {'plaintext': count}) # the dictionary may contain several plainwords with respective counts. 

Additionally you must create a `doc_metadata.json` file that is a list of dictionaries with the following fields:
	[{
        "id": "1",
        "name": "1.txt",
        "timestamp": "1"
    },...]
Specify this file in `legacy helper:` under the key `doc_metadata` (see default.yaml for an example)


