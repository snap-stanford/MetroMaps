#!/usr/local/bin/python2.7

import argparse
import mm.inputhelpers
import mm.inputhelpers.factory
import mm.input
import mm.mapgen
import logging
import yaml
import yaml.composer



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
    Run_map_generator(configs)





if __name__=='__main__':
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Run Metromaps by specifying a config file')
    parser.add_argument('config_file', help='See default.yaml for configuration options')
    parser.add_argument('--defaults', default='mm/default.yaml', help='the default values get preloaded from this yaml configuration file')
    args = parser.parse_args()
    config_dict = {}

    with open(args.defaults) as df:
        try: 
            config_dict = yaml.load(df)
        except yaml.composer.ComposerError:
            logging.error('ERROR in yaml-reading the default config file')
            raise
    sections = config_dict.keys()
    with open(args.config_file) as cf:
        try: 
            new_config = yaml.load(cf)
            for section in sections:
                sec_dict = new_config.get(section, {})
                config_dict.get(section).update(sec_dict)
        except yaml.composer.ComposerError:
            logging.error('ERROR in reading the input config file')
            raise
    logging.debug('final configuration: %s' % (str(config_dict)))
    Main(config_dict)
    
