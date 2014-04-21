# Pipeline




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

