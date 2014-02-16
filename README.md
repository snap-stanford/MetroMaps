mm
==

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.

#Input Data

The input to Metromaps consists of several parts:

* global tokens : dictionary from "some word" : id
* global counts : dictionary from tokenID : total counts
* doc metadata : list, each element of which is
  * timestamp (string, that defines a strict ordering if the string is ordered like an int)
  * id
  * filename
*doc counts: dictionary from doc id -> tokenID(s) -> counts in the doc

The above fields are read (if available) from one file called "master_input.json" with the key of json data defined as above, but with spaces replaced by underscores ("global_tokens", "global_counts") and then replaced by any individual json files. 

# Output

