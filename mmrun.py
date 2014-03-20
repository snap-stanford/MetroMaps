#!/usr/local/bin/python2.7

import argparse
import mm.inputhelpers
import mm.inputhelpers.factory
import mm.input
import mm.mapgen
import logging
import yaml



def Run_input_handler(configs):
    input_helper_configs = configs.get('input_helper')
    if (input_helper_configs.get('mode')):
        logging.debug(input_helper_configs)
        logging.info("Running input handler")
        handler_input = mm.inputhelpers.factory.ReadConfig(configs.get('input_helper'))
        handler_input.run()
        handler_input.save()
    else:
        logging.info("Skipping input handler")

def Run_scoring_handler(configs):
    scoring_handler_configs = configs.get('scoring_handler',{})
    if (scoring_handler.get('mode')):
        logging.info("Running scoring function (getting tfidf)")
        scoring_handler = mm.input.ScoringHandler(scoring_handler_configs)

def Run_legacy_handler(configs):
    legacy_configs = configs.get('legacy_helper')
    if (legacy_configs.get('mode')):
        logging.info("Converting to legacy format")

        legacy_handler = mm.input.LegacyHandler(legacy_configs)
        legacy_handler.write()
        logging.info("Legacy format written to %s" %(configs.get('legacy_helper').get('output_dir')))

def Run_clustering_handler(configs):
    clustering_configs = configs.get('clustering',{})
    if (clustering_configs.get('mode')):
        logging.info("Running clustering handler")
        clustering_handler = mm.mapgen.cluster_generator.ClusterGenerator(configs.get('clustering'))
        clustering_handler.run()
        clustering_handler.write()

def Run_map_generator(configs):
    map_gen_configs = configs.get('mapgen')
    if (map_gen_configs.get('mode')):
        logging.info("Running map generation")
        mapgen_handler = mm.mapgen.legacy_generator.LegacyGenerator(map_gen_configs)
        mapgen_handler.run()
    else:
        logging.info('Skipping map generator')

def Main(configs):
    Run_input_handler(configs)    
    Run_legacy_handler(configs)
    Run_clustering_handler(configs)
    # Run_clustering_handler(configs)
    Run_map_generator(configs)





if __name__=='__main__':
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Run Metromaps by specifying a config file (e.g. default.ini)')
    parser.add_argument('config_file', help='See default.ini for configurations')
    args = parser.parse_args()
    config_dict = {}
    with open(args.config_file) as cf:
        config_dict = yaml.load(cf)
    Main(config_dict)
    
