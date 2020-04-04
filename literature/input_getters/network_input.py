from literature.input_getters.iinput_getter import IInputGetter

class NetworkInput(IInputGetter):
    def __init__(self):
        pass 

    def parse(self, data):
        return data

    def get_input(self):
        return self.parse("got this from the network") # testing
