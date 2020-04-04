from literature.input_getters.iinput_getter import IInputGetter

class ConsoleInput(IInputGetter):
    def __init__(self):
        pass

    def parse(self, data):
        return data

    def get_input(self):
        return self.parse("got this from stdin")

        # this'll be what it is, but for testing see above
        # return self.parse(input()) 
