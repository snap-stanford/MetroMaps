# This is the glue of the application

import argparse
import sys
import config_handler


def Main(args, ch):
    InputDataHandler = config.

if __name__=="__main__":
    parser = argparse.ArgumentParser("Glue of the Metromaps application")
    parser.add_argument("--config_file")
    if args.config_file:
        config_file = args.config_file
    else:
        config_file = None
    ch = config_handler.Config(config_file)
    Main(sys.args, ch)
