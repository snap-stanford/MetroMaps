class NewsHelper():

    def __init__(self, whitelist, name='new_helper'):
        pass

    def run(self):
        print 'running'

    def save(self):
        print 'saving'

    def __str__(self):
        return 'this is a newshelper'

def construct(configs):
    return NewsHelper(**configs)