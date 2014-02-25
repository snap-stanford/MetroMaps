
import math
import json

class LegacyHelper:
    def __init__(self, legacy_helper_config_dict):
        def token_stats(doc_counts):
            token_max = {} # maps token_id -> max doc frequency
            num_docs_with_term = {}
            for doc_id,doc_data in doc_counts.iteritems():
                for token_id,count in doc_data.iteritems():
                    current_max = token_max.get(token_id, -1)
                    num_docs_with_term[token_id] = num_docs_with_term.get(token_id, 0) + 1
                    if count > current_max:
                        token_max[token_id] = count

            return token_max, num_docs_with_term



        self.data = {}
        with open(legacy_helper_config_dict['input_json_file']) as in_json:
            self.data = json.load(in_json)
        
        self.global_tokens = self.data['global_tokens']
        self.global_counts = self.data['global_counts']
        self.doc_counts = self.data['doc_counts']
        self.num_clusters = self.data['num_clusters']
        self.doc_metadata = self.data['doc_metadata']
        self.input_dir = self.data['input_dir']
        self.output_dir = self.data['output_dir']
        self.max_token_counts, self.num_docs_with_term = token_stats(self.doc_counts)
        self.num_docs = len(doc_counts)

    def tfidf(self, token_id, doc_id):
        if self.num_docs_with_term.get(token_id, 1) <= 1:
            '''do check so we do not divide by 0'''
            return 0
        max_count = self.max_token_counts(token_id)
        in_doc_count = self.doc_counts.get(doc_id,{}).get(token_id,0)
        total_count = self.global_counts.get(token_id, 0)
        tf = math.log(in_doc_count + 1)  #0.5 + 0.5 * in_doc_count / float(max_count)
        idf = math.log(float(self.num_docs)/float(num_docs_with_term[token_id]))
        return tf * idf

    def write(self):
        docs = sorted(self.doc_metadata, key= lambda x: int(x['timestamp']))

        clusters = [[]] * self.num_clusters
        ''' assign clusters to documents '''
        for i, doc in enumerate(docs):
            
            clusters[i / self.num_clusters].append(doc)
        
        def fakeDate(cluster_number, doc_number):
            assert (cluster_number >= 0 and cluster_number < 12)
            assert (doc_number >= 0 and doc_number < 30)
            return "%s%02i%02i" ("2013", cluster_number+1, doc_number+1)

        def write_docs_in_cluster(docs_in_cluster, ostream, cluster_date):
            for doc in docs_in_cluster:
                

                doc_id = doc['id']
                doc_name = doc.get('name', 'untitled')
                doc_link = doc.get('link', '#')
                doc_data = self.doc_counts[doc_id]
                doc_tokens = []
                tfidf_sum = 0
                for token_id, token_count in doc_data.iteritems():
                    tfidf_score = self.tfidf(token_id, doc_id)
                    doc_tokens += [(token_id, tfidf_score)]
                    tfidf_sum += tfidf_score

                tfidf_avg = float(tfidf_sum) / len(doc_data)
                doc_tokens.sort(key=get(1),reverse=True)


                ''' 1. write doc header
                    2. write doc tokens
                    3. write two new lines'''
                ostream.write('%s\t%f\n' % (doc_id, tfidf_avg))
                ostream.write('%s\t%s\t%s\t%s' % (doc_id, cluster_date, doc_link, doc_name))

                for token in doc_tokens:
                    ostream.write('%s\t%s\n' % (token[0], token[1]))
            ostream.write('\n\n')








