"""
Null mapping to python None globally unique object
"""


class Null(object):
    
    def __init__(self):
        pass
    
    def __eq__(self, comparable):
        return NotImplemented
