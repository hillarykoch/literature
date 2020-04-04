from literature.comms.icomms import IComms

class ConsoleComms(IComms):
    def __init__(self):
        pass

    def parse(self, data):
        return data

    def get_data(self):
        return self.parse("got this from stdin")

        # this'll be what it is, but for testing see above
        # return self.parse(input()) 
    def send_data(self, data):
        return f"sent {data} over stdin"
