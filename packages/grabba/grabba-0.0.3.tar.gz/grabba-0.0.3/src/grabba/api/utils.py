import re

def camel_to_snake(name: str) -> str:
    """Convert camelCase string to snake_case"""
    # Handle acronyms (e.g., 'JSONData' → 'json_data')
    name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Handle normal camelCase (e.g., 'camelCase' → 'camel_case')
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def to_camel_case(snake_str):
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])

def dict_to_camel_case(data):
    """Recursively convert dictionary keys to camelCase"""
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = to_camel_case(key)
            new_dict[new_key] = dict_to_camel_case(value)
        return new_dict
    elif isinstance(data, list):
        return [dict_to_camel_case(item) for item in data]
    else:
        return data
    
def dict_to_snake_case(data):
    """Recursively convert all dictionary keys from camelCase to snake_case"""
    if isinstance(data, dict):
        return {
            camel_to_snake(key): dict_to_snake_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [dict_to_snake_case(item) for item in data]
    return data  # Return unchanged for non-dict/list values