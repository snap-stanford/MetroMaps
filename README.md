Metromaps
=========

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.

# Version
0.1.2. Changes from 0.1.1:

- updgrade to SNAP.PY instead of networkx



# Install
Metromaps is fueled by Python 2.7. If you are running on MAC OS X, make sure you have the [brew version] of Python. 

You will need [SNAP.PY]. You might also want to get [nltk] but it's not required for basic functionality. 

Once you have these packages, just clone this github repository! Write to us if you have any problems.

[networkx]: http://networkx.github.io/
[SNAP.PY]: http://snap.stanford.edu/snappy/index.html
[nltk]: http://www.nltk.org/
[brew version]: http://docs.python-guide.org/en/latest/starting/install/osx/

# Running MetroMaps
Each domain requires its own configuration file (see docs/ for some tips). Once you have your configuration ready, run it with:

	python2.7 mmrun.py configuration.yaml

Default `lotr.yaml` configuration works on the Lord of the Rings domain, and outputs the final MetroMap into `lotr.mm`

# Writing your own configuration file

Metromaps is a pipeline of several, mostly independent, processes: 

- `input_helper`: translates your domain into MM format
- `legacy_helper`: slices the data into timeslices
- `clustering`: produces clusters from each timeslice
- `mapgen`: generates the MetroMap

Each process gets its own field in the configuration file with 
fields customized for your specific domains. In the following section
I describe what each field means and then provide an example
of running MetroMaps on a book domain. 

## `input_helper`

This part of the pipeline is responsible for taking raw text data as input
and producing a JSON file with the following fields:

- `doc_counts`: "doc_id" -> {"token_id" : count}
- `global_counts`: "token_id" -> total_count
- `global_tokens`: "clean_plaintext_token" -> id
- `representative_tokens`: "token_id" -> {"Plaintext_instance": total_count}

There is currently only one input-helper available, called `whitelistcounter`. 
This input-helper only considers tokens that appear on the whitelist. You are encouraged to write your own input_helper for your own domain, just make sure
it creates the fields above. If you write your own input-helper place it in the `mm/inputhelpers` directory. Specify the input-helper you wish to use by using its filename in the `name:` field in the input_helper section of the configuration file. Any other fields specified in this section get sent to your input helper as a dictionary on instantiation.

### `whitelisthelper`
A sample input-helper. Counts tokens that appear in the whitelist (file specified under `whitelist` in which tokens are separated with new-lines).

    mode: "on" or "off" specifies whether to run the input_helper or not
    name: whitelistcounter 
    encoding: UTF-8 # output encoding of tokens and ids
    in_encoding: cp1252 #input encoding (encoding used on your input files)
    whitelist: filename (newline separated white-list tokens) 
    input_directory: directory in which input files are stored 
    outfile: output JSON files with the required fields


## `legacy_helper`
Contains the following fields. 

    mode: "on" or "off" whether to run this or not
    input_json_file: *input_out #your_output_from_above FILL OUT HERE
    output_dir: /tmp/query_result 
    doc_metadata: Specify your metadata here
    num_timeslices: 20
    output_json: &score_JSON /tmp/legacy_handler_out.json
    choose_representative_token: on
    
The important field to specify here is `doc_metadata` which contains a list of document metadata, with each document having `name`, `id`, and `timestamp`.

##clustering:

    mode: "on" or "off" to run or not
    input_json: *score_JSON 
    similarity_merge: 1 # <intersection> / <small size> above this limit merges
    dilution_merge: 0 # only <= below this number is merged. This is percentage of new terms that can be added
    output_json: &clusters_JSON /tmp/clusters.json
    graphing: off
    out_graph_dir: /tmp/timeslice_graphs/
    # Remove the following when cleaning project
    out_legacy_dir: /tmp/clusters/clusters

Clustering is done through clique-perculation and communities are combined depending on the similarity and dilution_merge fields specify the parameters that create clusters. 

##mapgen:

    mode: "on" or "off" to run it or not
    cluster_dir: /tmp/clusters
    raw_lines: /tmp/raw_lines
    line_descriptions: /tmp/line_descriptions
    chosen_lines: final_map.mm
    
    




