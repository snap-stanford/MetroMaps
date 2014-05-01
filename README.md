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
- mm_standard_input: name of a json file to which the standard input will be written to. Unless you want to save this file in a permanent place, _you can leave this field blank_ and view temporary output in `/tmp/mm_input.json` if needed. The required JSON fields of this file are described in [docs/formats/mm_standard_input.md]

[LOTR metadata]: https://github.com/snap-stanford/MetroMaps/blob/master/domains/lotr/data/doc_meta.json



<a name="input_helper"></a>
#### Section `input_helper:`

This part of the pipeline is responsible for taking raw text data as input
and producing the JSON file specified in `global.mm_standard_input`. This file, along with `doc_metadata` is considered the standard input to MetroMaps. The output JSON format is documented in [docs/formats/mm_standard_input_json.md]. 

[docs/formats/mm_standard_input_json.md]: https://github.com/snap-stanford/MetroMaps/blob/master/docs/formats/mm_standard_input_json.md

In the `name` field, you should specify which helper you want to run. There are two options:

- [`whitelistcounter`] This keeps track of words specified in the file under `whitelist:`
- [`blacklistcounter`] This keeps track of all words that do not appear in the file listed under `blacklist:` and appear more frequently than the number specified in `discard_frequency` 

There is currently only one input-helper available, called `whitelistcounter`. 
This input-helper only considers tokens that appear on the whitelist. You are encouraged to write your own input_helper for your own domain, just make sure
it creates the fields listed below. If you write your own input-helper place it in the `mm/inputhelpers` directory. Specify the input-helper you wish to use by using its filename in the `name:` field in the input_helper section of the configuration file. Any other fields specified in this section get sent to your input helper as a dictionary on instantiation.

Example (including fields for both whitelistcounter and blacklistcounter): 
    mode: "on" or "off" specifies whether to run the input_helper or not
    name: whitelistcounter or blacklistcounter
    encoding: UTF-8 # output encoding of tokens and ids
    in_encoding: cp1252 #input encoding (encoding used on your input files)
    whitelist: filename (newline separated white-list tokens) 
    blacklist: filename (newline spearated)
    discard_frequency: 2 (if word appears this number of times or less, it's discarded when blacklistcounter is used)
    input_directory: directory in which input files are stored 
    outfile: output JSON files with the required fields

<a name="slicing"></a>
#### Section `slicing`
Contains the following fields. 

    mode: "on" or "off" whether to run this or not
    input_json_file: *input_out #your_output_from_above FILL OUT HERE
    output_dir: /tmp/query_result 
    doc_metadata: Specify your metadata here
    num_timeslices: 20
    output_json: &score_JSON /tmp/legacy_handler_out.json
    choose_representative_token: on
    
The important field to specify here is `doc_metadata` which contains a list of document metadata, with each document having `name`, `id`, and `timestamp`.

<a name="clustering"></a>
#### Section `clustering:`

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

<a name="clustering"></a>
#### Section `mapgen:`
The important fields here are `chosen_lines` and `chosend_lines_json`. The others are temporary files.
    mode: "on" or "off" to run it or not
    cluster_dir: /tmp/clusters
    raw_lines: /tmp/raw_lines
    line_descriptions: /tmp/line_descriptions
    chosen_lines: final_map.mm (human readable )
    chosen_lines_json: chosen_lines.json
    
<a name="vizbuilder"></a>
#### Section `vizbuilder:`

In design, `vizbuilder` is similar to `input_helper` in that you choose which visualization builder to run (by specifying the name field). Currently there is only one option, but I am working hard to increase this number. The only one currently available is `clusterdescription` which labels each cluster with the words describing the cluster. 

    mode: "on" or "off"
    name: clusterdescription 
    input_lines_json: same as the 'chosen_lines_json' field above
    final_map_viz_json: online-visualization friendly json stored here
    producehtml: "on" or "off" whether to render the html page 
    website_output_dir: directory where web pages will be stored to
    webpage_name: Metromaps.html (name of the html file in the "website_output_dir")



[mm/default.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/mm/default.yaml

### Example Configurations:

- [lotr.yaml] 
- [default.yaml] - values are populated from this file if not mentioned in yours

[lotr.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/lotr.yaml
[default.yaml]: https://github.com/snap-stanford/MetroMaps/blob/master/mm/default.yaml



### Common Problem with SNAP.PY installation:

Here is what someone suggested to do in the CS224W class that extensively used SNAP and SNAP.PY:

    Christoph E. Wertz 6 minutes ago
    [christoph@hazel] $ otool -L snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so 
    snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so:
    _snap.so (compatibility version 0.0.0, current version 0.0.0)
    /System/Library/Frameworks/Python.framework/Versions/2.7/Python (compatibility version 2.7.0, current version 2.7.1)
    /usr/lib/libstdc++.6.dylib (compatibility version 7.0.0, current version 52.0.0)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 159.1.0)
     
     
    Tue Sep 24 23:27:28 : ~/Development/stanford/cs224w
    [christoph@hazel] $ install_name_tool -change /System/Library/Frameworks/Python.framework/Versions/2.7/Python /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Python snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so 
     
    Tue Sep 24 23:34:54 : ~/Development/stanford/cs224w
    [christoph@hazel] $ otool -L snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so 
    snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so:
    _snap.so (compatibility version 0.0.0, current version 0.0.0)
    /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Python (compatibility version 2.7.0, current version 2.7.1)
    /usr/lib/libstdc++.6.dylib (compatibility version 7.0.0, current version 52.0.0)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 159.1.0)
     
     
    Tue Sep 24 23:38:14 : ~/Development/stanford/cs224w
    [christoph@hazel] $ cp snap-0.7-dev-macosx10.7.5-x64-py2.7/snap.py .
    Tue Sep 24 23:38:24 : ~/Development/stanford/cs224w
    [christoph@hazel] $ cp snap-0.7-dev-macosx10.7.5-x64-py2.7/_snap.so .
    Tue Sep 24 23:38:32 : ~/Development/stanford/cs224w
    [christoph@hazel] $ python quick_test.py 
    SUCCESS, your version of Snap.py is 0.7
    Tue Sep 24 23:38:38 : ~/Development/stanford/cs224w
    [christoph@hazel] $ 
     
     
     
    Christoph E. Wertz 1 minute ago 
    [christoph@hazel] $ ll /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_snap.so 
    -rwxr-xr-x  1 root  admin  26767992 Sep 22 19:38 /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_snap.so
    Tue Sep 24 23:43:05 : ~/Development/stanford/cs224w/snap-0.7-dev-macosx10.7.5-x64-py2.7
    [christoph@hazel] $ sudo cp _snap.so !$
    sudo cp _snap.so /usr/local/Cellar/python/2.7.5/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_snap.so
     
     
    Christoph E. Wertz 1 minute ago 
    [christoph@hazel] $ python quick_test.py 
    SUCCESS, your version of Snap.py is 0.7
    Tue Sep 24 23:44:16 : ~/Development/stanford/cs224w
    [christoph@hazel] $ 
