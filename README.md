Metromaps
=========

Welcome to Metromaps, an innovative way of extracting story-lines from your chronological text domain.
README updated to reflect v0.2.1

# Version notes

Git history is tagged with each version starting on v0.2.0

- **v0.2.1** 
    - The configuration file now contains a `global` field. See `mm/default.yaml` to see which fields are modifiable. 
    - Renamed `legacy_helper` to `slicing` in the configuration file. 
    - You can now choose `blacklistcounter` in addition to `whitelistcounter` to choose which input handler to run. If chosen, it requires `blacklist` and `discard_frequency` to be added. See below for notes on how to specify these.

- v0.2.0. Working visualization of clusters. No mapping back to articles, as of yet 

- v0.1.2. Updgrade to SNAP.PY instead of networkx



# Install

Metromaps is fueled by Python 2.7. If you are running on MAC OS X, make sure you have the [brew version] of Python. 

You will need [SNAP.PY]. SNAP.PY is not yet in the Python Package Index (pip), so please install following the instructions on the website. 

Once you have these packages, just clone this github repository! Write to us if you have any problems.

[networkx]: http://networkx.github.io/
[SNAP.PY]: http://snap.stanford.edu/snappy/index.html
[nltk]: http://www.nltk.org/
[brew version]: http://docs.python-guide.org/en/latest/starting/install/osx/

I also included a `requirements.txt` by doing a freeze on my current `pip` package manager. This list contains all of the 
requirement packages and more. So if you fulfill those requirements, you are good to go.

Best way to install these packages is use virtualenv (which creates a sandbox python environment). To get started, here is a [very good link].

[very good link]: http://simononsoftware.com/virtualenv-tutorial/

# Running MetroMaps
Each domain requires its own configuration file. Even though this guide is pretty long -- don't worry, writing configurations is really easy. Follow the next section's guide for how to write your own configuration. Once you have it written, 

	python2.7 mmrun.py configuration.yaml

The sample [lotr.yaml] configuration works on the Lord of the Rings domain. To run Metromaps on the LOTR domain, do

    python2.7 mmrun.py lotr.yaml

[lotr.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/lotr.yaml

# Writing your own configuration file

Running Metromaps on any domain requires the configuration file. This section describes how to modify existing configuration files and write your own configuration to apply Metromaps to your own unique domain. Happy mapping! 

The configuration file is organized to reflect that Metromaps is a pipeline of several, mostly independent, processes (click to jump): 

- [`input_helper`](#input_handler): translates your domain into MM format
- [`slicing`](#slicing): slices the data into timeslices
- [`clustering`](#clustering): produces clusters from each timeslice
- [`mapgen`](#mapgen): generates the MetroMap
- [`vizbuilder`](#vizbuilder): builds the HTML/Javascript visualization rendered in your favorite browser

The configuration file contains a field for each of the processes (with the same name as the process) and a [`global`](#global) field for resources shared among all of the processes. The following sections go through parameters for each section. 

All of the defaults are set in [mm/default.yaml] and overwritten in your own configuration. So if you are confused about some field, you can just not include it in your configuration and the default value will be used.

[mm/default.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/mm/default.yaml

<a name="global"></a>
#### Section `global:`
The fields in this section are accessible to all other sections. We include three fields here:
- log_level: `debug` or `info` based on your desired level of verbosity
- **doc_metadata**: relative path to your document metadata file, e.g. `domains/lotr/doc_meta.json`. The format should mimic [LOTR metadata].
- mm_standard_input: name of a json file to which the standard input will be written to. Unless you want to save this file in a permanent place, _you can leave this field blank_ and view temporary output in `/tmp/mm_input.json` if needed.

[LOTR metadata]: https://github.com/snap-stanford/MetroMaps/blob/master/domains/lotr/data/doc_meta.json



<a name="input_helper"></a>
#### Section `input_helper:`

This part of the pipeline is responsible for taking raw text data as input
and producing the JSON file specified in `global.mm_standard_input`. This file, along with `doc_metadata` is considered the standard input to MetroMaps. The output JSON format is documented in [docs/formats/mm_standard_input_json.md]. 

[docs/formats/mm_standard_input_json.md]: https://github.com/snap-stanford/MetroMaps/blob/master/docs/formats/mm_standard_input_json.md

In the `name` field, you should specify which helper you want to run. There are two options:

- [`whitelistcounter`] This keeps track of words specified 
- [`blacklistcounter`]

There is currently only one input-helper available, called `whitelistcounter`. 
This input-helper only considers tokens that appear on the whitelist. You are encouraged to write your own input_helper for your own domain, just make sure
it creates the fields above. If you write your own input-helper place it in the `mm/inputhelpers` directory. Specify the input-helper you wish to use by using its filename in the `name:` field in the input_helper section of the configuration file. Any other fields specified in this section get sent to your input helper as a dictionary on instantiation.

###### `name: whitelisthelper`
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
The important fields here are `chosen_lines` and `chosend_lines_json`. The others are temporary files.
    mode: "on" or "off" to run it or not
    cluster_dir: /tmp/clusters
    raw_lines: /tmp/raw_lines
    line_descriptions: /tmp/line_descriptions
    chosen_lines: final_map.mm (human readable )
    chosen_lines_json: chosen_lines.json
    
##vizbuilder:

In design, `vizbuilder` is similar to `input_helper` in that you choose which visualization builder to run (by specifying the name field). Currently there is only one option, but I am working hard to increase this number. The only one currently available is `clusterdescription` which labels each cluster with the words describing the cluster. 

    mode: "on" or "off"
    name: clusterdescription 
    input_lines_json: same as the 'chosen_lines_json' field above
    final_map_viz_json: online-visualization friendly json stored here
    producehtml: "on" or "off" whether to render the html page 
    website_output_dir: directory where web pages will be stored to
    webpage_name: Metromaps.html (name of the html file in the "website_output_dir")



[mm/default.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/mm/default.yaml
