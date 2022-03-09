import skrf as rf

class File:
    """
    A wrapper class for rf.Network that extracts and stores data from the file name. 
    """
    def __init__(self, fname):
        self.fname = fname
        self.network = rf.Network(fname)
        self.parse_fname


    def parse_fname(self):
        #assume fname of the form [Model]_[Serial Number]_VNA_[number] e.g. DXM20AF_U00173_VNA_01.s2p
        items = self.fname.split("_")
        self.model = items[0]
        self.serial_no = items[1]
        self.test_num = int(items[4])

class Unit
    """
    Represents an individual unit of some device model. Unit has a list of .s2p files.
    """
    def __init__(self, file_list):
        self.files = []
        for file in file_list:
            self.files.append(File(file))
