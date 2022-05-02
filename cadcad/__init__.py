from cadcad.utils import expand_data, convert_data

class Point():
    def __init__(self, space, data = {}):
        self.space = space
        
        expanded = expand_data(space.dimensions)
        converted = convert_data(data)
        
        if converted != expanded:
            raise Exception(f'Dimension mismatch: expected\r\n{expanded}, was given \r\n{converted}')
            
        self.data = data
        
    def __add__(self, other):
        return self.space.__add__(self.data, other.data)
    
    def __and__(self, other):
        return self.space.__and__(self.data, other.data)
    
    def __floordiv__(self, other):
        return self.space.__floordiv__(self.data, other.data)
    
    def __iadd__(self, other):
        return self.space.__iadd__(self.data, other.data)
    
    def __imul__(self, other):
        return self.space.__imul__(self.data, other.data)
    
    def __invert__(self, other):
        return self.space.__invert__(self.data, other.data)
    
    def __ipow__(self, other):
        return self.space.__ipow__(self.data, other.data)
    
    def __isub__(self, other):
        return self.space.__isub__(self.data, other.data)
    
    def __mod__(self, other):
        return self.space.__mod__(self.data, other.data)
    
    def __mul__(self, other):
        return self.space.__mul__(self.data, other.data)
    
    def __or__(self, other):
        return self.space.__or__(self.data, other.data)
    
    def __pow__(self, other):
        return self.space.__pow__(self.data, other.data)
    
    def __radd__(self, other):
        return self.space.__radd__(self.data, other.data)
    
    def __repr__(self):
        return f'Point(space = {self.space}, data = {self.data})'
    
    def __rmod__(self, other):
        return self.space.__rmod__(self.data, other.data)
    
    def __rmul__(self, other):
        return self.space.__rmul__(self.data, other.data)
    
    def __rpow__(self, other):
        return self.space.__rpow__(self.data, other.data)
    
    def __rsub__(self, other):
        return self.space.__rsub__(self.data, other.data)
    
    def __sub__(self, other):
        return self.space.__sub__(self.data, other.data)

    def __truediv__(self, other):
        return self.space.__trudiv__(self.data, other.data)

class Block():
    def __init__(self, name, domains = [], codomains = [], fn = None):
        self.name = name
        self.domains = domains
        self.codomains = codomains
        self.fn = fn
        
        for d in domains:
            if Space not in d.__bases__:
                raise Exception("Domain is not a space")
                
        for c in codomains:
            if Space not in d.__bases__:
                raise Exception("Codomain is not a space")
    
    def __repr__(self):
        return f'Block(name = {self.name}, domains = {self.domains}, codomains = {self.codomains}, fn = {self.fn})'
                
    def map(self, points):
        if len(self.domains) != len(points):
            raise Exception("Points length does not match domain length")
            
        new_points = self.fn(self, (points, ))
        
        if len(self.codomains) != len(new_points):
            raise Exception("Block function produced points length that do not match codomain length")
            
        return new_points

class Space():
    def __new__(cls, name, dimensions = {}, metrics = {}, constraints = {}):
        return type(name, (cls, ), {"name": name, "dimensions": dimensions, "metrics": metrics, "constraints": constraints})
    
    @classmethod
    def add_constraint(cls, block):
        if type(block) != Block:
            raise Exception("Constraint is not a block")
            
        cls.constraints[block.name] = block
    
    @classmethod
    def add_metric(cls, block):
        pass
    
    @classmethod
    def add_projection(cls, block):
        pass
        
    @classmethod
    def add_point(cls, point):
        pass
        
    @classmethod
    def create_constraint(cls, name, domains, fn):
        block = Block(name, domains, [Bit], fn)
        cls.constraints[name] = block
    
    @classmethod
    def create_metric(cls, fn):
        pass
    
    @classmethod
    def create_projection(cls, fn):
        pass
    
    @classmethod
    def create_point(cls, data):
        for c in cls.constraints:
            if len(cls.constraints[c].domains) != len(data):
                raise Exception("Length of points does not match length of domains")
            
            result = cls.constraints[c].map(data)
            
            if result[0].data["bit"] is False:
                raise Exception("Supplied data failed constraint:", c)
                
        return Point(cls, data)
    
    @classmethod
    def define_add(cls, fn):
        cls.__add__ = fn
        
    @classmethod
    def define_and(cls, fn):
        cls.__and__ = fn
        
    @classmethod
    def define_floordiv(cls, fn):
        cls.__floordiv__ = fn
        
    @classmethod
    def define_iadd(cls, fn):
        cls.__iadd__ = fn
        
    @classmethod
    def define_imul(cls, fn):
        cls.__imul__ = fn
        
    @classmethod
    def define_inv(cls, fn):
        cls.__invert__ = fn
        
    @classmethod
    def define_ipow(cls, fn):
        cls.__ipow__ = fn
        
    @classmethod
    def define_isub(cls, fn):
        cls.__isub__ = fn
        
    @classmethod
    def define_mod(cls, fn):
        cls.__mod__ = fn
    
    @classmethod
    def define_mul(cls, fn):
        cls.__mul__ = fn
        
    @classmethod
    def define_or(cls, fn):
        cls.__or__ = fn
        
    @classmethod
    def define_pow(cls, fn):
        cls.__pow__ = fn
        
    @classmethod
    def define_radd(cls, fn):
        cls.__radd__ = fn
        
    @classmethod
    def define_rmod(cls, fn):
        cls.__rmod__ = fn
        
    @classmethod
    def define_rmul(cls, fn):
        cls.__rmul__ = fn
        
    @classmethod
    def define_rpow(cls, fn):
        cls.__rpow__ = fn
        
    @classmethod
    def define_rsub(cls, fn):
        cls.__rsub__ = fn
        
    @classmethod
    def define_sub(cls, fn):
        cls.__sub__ = fn
        
    @classmethod
    def define_truediv(cls, fn):
        cls.__truediv__ = fn

# Primitive Spaces
Bit = Space("Bit", {"bit": bool})
Int = Space("Integer", {"int": int})
Real = Space("Real", {"real": float})