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
        return self.space.point_add(self.data, other.data)
    
    def __and__(self, other):
        return self.space.point_and(self.data, other.data)
    
    def __floordiv__(self, other):
        return self.space.point_floordiv(self.data, other.data)
    
    def __iadd__(self, other):
        return self.space.point_iadd(self.data, other.data)
    
    def __imul__(self, other):
        return self.space.point_imul(self.data, other.data)
    
    def __invert__(self, other):
        return self.space.point_invert(self.data, other.data)
    
    def __ipow__(self, other):
        return self.space.point_ipow(self.data, other.data)
    
    def __isub__(self, other):
        return self.space.point_isub(self.data, other.data)
    
    def __mod__(self, other):
        return self.space.point_mod(self.data, other.data)
    
    def __mul__(self, other):
        return self.space.point_mul(self.data, other.data)
    
    def __or__(self, other):
        return self.space.point_or(self.data, other.data)
    
    def __pow__(self, other):
        return self.space.point_pow(self.data, other.data)
    
    def __radd__(self, other):
        return self.space.point_radd(self.data, other.data)
    
    def __repr__(self):
        return f'Point(space = {self.space}, data = {self.data})'
    
    def __rmod__(self, other):
        return self.space.point_rmod(self.data, other.data)
    
    def __rmul__(self, other):
        return self.space.point_rmul(self.data, other.data)
    
    def __rpow__(self, other):
        return self.space.point_rpow(self.data, other.data)
    
    def __rsub__(self, other):
        return self.space.point_rsub(self.data, other.data)
    
    def __sub__(self, other):
        return self.space.point_sub(self.data, other.data)

    def __truediv__(self, other):
        return self.space.point_truediv(self.data, other.data)

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
    def __new__(cls, name, dimensions = {}, metrics = {}, constraints = {}, projections = {}):
        return type(name, (cls, ), {"name": name, "dimensions": dimensions, "metrics": metrics, "constraints": constraints, "projections": projections})
    
    @classmethod
    def cartesian(cls, name, other):
        dimensions = cls.dimensions.copy()
        dimensions.update(other.dimensions)
        return type(name, (cls, ), {"name": name, "dimensions": dimensions})

    @classmethod
    def add_constraint(cls, block):
        if type(block) != Block:
            raise Exception("Constraint is not a block")
            
        cls.constraints[block.name] = block
    
    @classmethod
    def add_metric(cls, block):
        if type(block) != Block:
            raise Exception("Metric is not a block")
            
        cls.metrics[block.name] = block
    
    @classmethod
    def add_projection(cls, block):
        if type(block) != Block:
            raise Exception("Projection is not a block")
            
        cls.projections[block.name] = block
        
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
        cls.point_add = fn
        
    @classmethod
    def define_and(cls, fn):
        cls.point_and = fn
        
    @classmethod
    def define_floordiv(cls, fn):
        cls.point_floordiv = fn
        
    @classmethod
    def define_iadd(cls, fn):
        cls.point_iadd = fn
        
    @classmethod
    def define_imul(cls, fn):
        cls.point_imul = fn
        
    @classmethod
    def define_inv(cls, fn):
        cls.point_invert = fn
        
    @classmethod
    def define_ipow(cls, fn):
        cls.point_ipow = fn
        
    @classmethod
    def define_isub(cls, fn):
        cls.point_isub = fn
       
    @classmethod
    def define_mod(cls, fn):
        cls.point_mod = fn
    
    @classmethod
    def define_mul(cls, fn):
        cls.point_mul = fn
        
    @classmethod
    def define_or(cls, fn):
        cls.point_or = fn
        
    @classmethod
    def define_pow(cls, fn):
        cls.point_pow = fn
        
    @classmethod
    def define_radd(cls, fn):
        cls.point_radd = fn
        
    @classmethod
    def define_rmod(cls, fn):
        cls.point_rmod = fn
        
    @classmethod
    def define_rmul(cls, fn):
        cls.point_rmul = fn
        
    @classmethod
    def define_rpow(cls, fn):
        cls.point_rpow = fn
        
    @classmethod
    def define_rsub(cls, fn):
        cls.point_rsub = fn
        
    @classmethod
    def define_sub(cls, fn):
        cls.point_sub = fn
        
    @classmethod
    def define_truediv(cls, fn):
        cls.point_truediv = fn

# Primitive Spaces
Bit = Space("Bit", {"bit": bool})
Int = Space("Integer", {"int": int})
Real = Space("Real", {"real": float})