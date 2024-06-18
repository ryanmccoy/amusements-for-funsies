def get_dict_schema(data, parent_key=''):
    """
    Traverses a nested structure composed of dicts, lists, and sets, and returns a schema of keys.

    :param data: The nested structure to traverse.
    :param parent_key: The accumulated path to the current item.
    :return: A set containing the schema of keys.
    """
    schema = set()

    if isinstance(data, dict):
        for key, value in data.items():
            # Construct the full path for this key
            full_key = f"{parent_key}.{key}" if parent_key else key
            schema.add(full_key)
            # Recursively accumulate the schema from the nested structure
            schema |= get_dict_schema(value, full_key)
    elif isinstance(data, (list, set)):
        for item in data:
            if isinstance(item, (dict, list, set)):
                # For items in a list or set, we do not append an index to the path
                schema |= get_dict_schema(item, parent_key)
    # For other types, we do not need to accumulate anything more

    return schema

def parse_json_structure(json_obj):
    """
    Recursively parses a JSON object and returns a skeleton that represents
    the structure of the JSON object with the data types of the values.

    Args:
        json_obj (dict or list): The JSON object to parse.

    Returns:
        dict or list: A simplified structure of the JSON object with types as values.
    """
    if isinstance(json_obj, dict):
        return {k: parse_json_structure(v) for k, v in json_obj.items()}
    elif isinstance(json_obj, list):
        # If list is not empty, take the type of the first item as representative for all items
        return [parse_json_structure(json_obj[0])] if json_obj else []
    else:
        # Return the type of the value
        return type(json_obj).__name__
