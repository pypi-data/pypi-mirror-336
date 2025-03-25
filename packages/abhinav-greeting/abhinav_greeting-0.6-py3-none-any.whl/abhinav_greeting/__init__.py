from  logging import basicConfig, INFO, getLogger

logger = getLogger("abhinav.py")
basicConfig(filename="abhinav.log", level=INFO, format="%(asctime)s - %(levelname)s - %(message)s - %(lineno)d - %(name)s")


def greeting(headers: dict):
    """
    This function returns a personalized greeting message
    based on the 'Name' header passed in the dictionary.

    :param headers: Dictionary containing the header information.
    :return: Greeting message based on the 'Name' key.
    """
    logger.info("Fetching the headers")
    name = headers.get('Name', None)
    logger.info("Fetch the name")
    if name:
        logger.info("Executing the function")
        return f"Hello {name}! nice to meet you"
    else:
        logger.critical("No name provided, please try again.")
        return "No name provided inside header"
