def ReadConfig(helper_configs):
    ''' Specify a dictionary with configurations '''
    input_helper_name = helper_configs['name']
    helper_module = __import__(input_helper_name, globals=globals())
    helper = helper_module.construct(helper_configs)
    return helper