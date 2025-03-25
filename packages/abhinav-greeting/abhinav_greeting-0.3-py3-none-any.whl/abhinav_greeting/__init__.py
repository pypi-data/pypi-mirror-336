def greeting(headers: dict):
    """
    This function returns a personalized greeting message
    based on the 'Name' header passed in the dictionary.

    :param headers: Dictionary containing the header information.
    :return: Greeting message based on the 'Name' key.
    """
    name = headers.get('Name', None)
    if name:
        return f"Hello {name}!, nice to meet you"
    else:
        return "No name provided inside header"
