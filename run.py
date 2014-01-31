import argparse
from ConfigParser import ConfigParser
import 
def RunInputHelper():


def Main(config_filename):
    configs = ConfigParser()
    configs.read(config_filename)
    config_sections = configs._sections
    input_helper = inputhelper.ReadConfig(config_sections.get('input_helper'))
    input_helper.run()



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Run Metromaps by specifying a config file (e.g. default.ini)')
    parser.add_argument('config_file', help='See default.ini for configurations')
    args = parser.parse_args()
    Main(args.config_file)
    print args.config_file