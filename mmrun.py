import argparse
import mm.inputhelpers
import mm.inputhelpers.factory
import yaml



def Run_input_handler(configs):
    print configs
    handler_input = mm.inputhelpers.factory.ReadConfig(configs)
    # handler_input.run()
    # handler_input.save()




def Main(configs):
    Run_input_handler(configs)    
    # Run_clustering_handler(configs)





if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Run Metromaps by specifying a config file (e.g. default.ini)')
    parser.add_argument('config_file', help='See default.ini for configurations')
    args = parser.parse_args()
    config_dict = {}
    with open(args.config_file) as cf:
        config_dict = yaml.load(cf)
    Main(config_dict)
    
