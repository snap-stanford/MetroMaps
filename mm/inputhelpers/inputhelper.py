import whitelistcounter
import newshelper



def ReadConfig(input_helper_config):
    sih = section_input_helper
    helper = sih.get('helper')
    h = helper.lower()
    return {
        'whitelistcounter' : whitelistcounter.FactoryFromConfig(input_helper_config),
        'newshelper': newshelper.FactoryFromConfig(),
    }[h]