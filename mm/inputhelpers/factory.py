
# def __get_assert_value(configs, value):
#     if value not in configs:
#         print 'Field %s not in configs' % value
#         raise ValueError
#     return configs.get(value)


def ReadConfig(configs):
    ''' Specify a dictionary with configurations '''
    input_helper_configs = configs['input_helper']
    input_helper_name = input_helper_configs['name']
    helper_module = __import__(input_helper_name, globals=globals())
    helper = helper_module.construct(input_helper_configs)
    helper.run()
    print helper
