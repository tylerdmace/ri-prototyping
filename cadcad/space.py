from cadcad.point import Point

class Space():
    def __new__(cls, name, dims = {}, metrics = {}, constraints = {}):
        cls.name = name
        cls.dimensions = dims
        cls.metrics = metrics
        cls.constraints = constraints
        
        return type(name, (), {})
    
    @classmethod
    def create_point(cls, data):
        return Point(cls, data)
    
Bit = Space("Bit", {"b": bool})

#Int = Space("Integer", {"i": int})

#Real = Space("Real", {"r": float})

class Bit(metaclass=Space)