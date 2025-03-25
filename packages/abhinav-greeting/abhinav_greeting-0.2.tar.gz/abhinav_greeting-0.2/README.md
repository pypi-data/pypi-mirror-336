# abhinav_greetings

`abhinav_greetings` is a simple Python package that provides a greeting function to personalize messages. This package allows users to easily generate personalized greetings based on the provided headers.

## Installation

To install `abhinav_greetings`, use the following command with `pip`:

```bash
pip install abhinav_greetings
```

## Usage
To use the greeting function from the package, you need to import it and call it with a dictionary containing your personal information (e.g., name). Below is an example of how to use the greeting function:

```python
from abhinav_greetings import greeting

# Define headers with personal details
headers = {'Name': 'Abhinav'}

# Print the greeting message
print(greeting(headers))
```

## Example Output:
```txt
Hello, Abhinav! Welcome to the world of Python.
```