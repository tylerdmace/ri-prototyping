from cadcad.utils import expand_data, convert_data

class Point():
    def __init__(self, space, data = {}):
        print(space, data)
        self.space = space
        
        expanded = expand_data(space.dimensions)
        converted = convert_data(data)
        
        if converted != expanded:
            raise Exception(f'Dimension mismatch: expected\r\n{expanded}, was given \r\n{converted}')
            
        self.data = data
        
    def __repr__(self):
        return f'Point(space = {self.space}, data = {self.data})'
        