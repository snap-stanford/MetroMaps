#### Format of global.mm_standard_input

This JSON file that is considered standard input to metromaps (along with `doc_metadata`) contains four fields: global_counts maps stem-id to count; doc_counts maps doc-id to a dictionary containing how many times each stem-id appears there; global_tokens maps each stem to its stem-id; and representative-token gives each stem-id to all possible words it appears in and individual counts. 

    {"global_counts": {"1": 494, "2": 111, ...}, 
     
     "doc_counts": {"1": {"1": 14, "2": 9, "3": 12, "4": 2, "5": 1}, "2": {"1": 15, "2": 4, "3": 13, "4": 1, "6": 5}, ...}
     
     "global_tokens": {"radagast": 29, "sam": 5, "bilbo": 1, "denethor": 26, "arwen": 19, "wormtongue": 35, "treebeard": 33, "gandalf": 11,...}
     
     "representative_tokens": {"1": {"`Bilbo!'": 2, "'Bilbo": 4, "Bilbo's.": 2, "Bilbo": 254, "Bilbo)": 1, "Bilbo.": 79, "Bilbo,": 63, "Bilbo!'": 2, "Bilbo?'": 1, "'Bilbo!'": 2, "Bilbo,'": 10, "Bilbo;": 4, "Bilbo's": 70}, "2": {"Baggins!'": 1, "'Baggins": 1, "Baggins;": 4, "Baggins.'": 3, "BAGGINS,": 1, "Baggins,'": 4, "BAGGINS": 2, "\"Baggins": 2, "Baggins'": 3, "Baggins?\"": 2, "Baggins": 56, "Baggins?'": 2, "Baggins,": 15, "Baggins.": 15}, ...}
     }