from literature.comms.icomms import IComms 

class GUIComms(IComms):
    def __init__(self):
        pass 

    def parse(self, data):
        return data

    def get_data(self):
        return self.parse("got this from the network") # testing

    def send_data(self, data):
        return f"sent {data} over network"
