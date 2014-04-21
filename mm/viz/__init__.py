def ReadConfig(configs):
    ''' Specify a dictionary with configurations '''
    input_helper_name = configs['name']
    helper_module = __import__(input_helper_name, globals=globals())
    helper = helper_module.construct(configs)
    return helper