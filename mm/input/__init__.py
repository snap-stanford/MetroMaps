from .legacy_handler import LegacyHandler


def ReadConfig(configs):
    ''' Specify a dictionary with configurations '''
    input_helper_configs = configs['scoring_helper']
    input_helper_name = input_helper_configs['name']
    helper_module = __import__(input_helper_name, globals=globals())
    helper = helper_module.construct(input_helper_configs)
    return helper