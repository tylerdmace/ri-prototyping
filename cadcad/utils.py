def convert_data(data):
    converted = {}
    
    for key, value in data.items():
        if type(value) == dict:
            converted[key] = convert_data(value)
        else:
            converted[key] = type(value)
    
    return converted

def expand_data(data):
    expanded = {}
    
    for key, value in data.items():
        if type(value) == dict:
            expanded[key] = expand(value)
        elif hasattr(value, "dimensions"):
            expanded[key] = expand_data(value.dimensions)
        else:
            expanded[key] = value
    
    return expanded