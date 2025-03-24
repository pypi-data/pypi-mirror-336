import numpy as np 

class Tensor (object):
    def __init__(self, data, creators=None , creation_op=None):
        self.data = np.array(data)
        self.creators = creators
        self.creation_op = creation_op
        self.grad = None

    def __add__(self, other):
        return Tensor(self.data + other.data, creators=[self, other], creation_op="add")
    
    def __repr__(self):
        return str(self.data.__repr__())
    
    def __str__(self):
        return str(self.data.__str__())