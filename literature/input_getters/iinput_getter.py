import enum

class IInputGetter():
    def __init__(self):
        pass
    
    # want all InputGetters to have a get_input, but don't want
    # and IInputGetter to exist on its own
    def get_input(self):
        raise NotImplementedError()
    def parse(self, data):
        raise NotImplementedError()
