# abhinav_greeting

`abhinav_greeting` is a simple Python package that provides a greeting function to personalize messages. This package allows users to easily generate personalized greeting based on the provided headers.

## Installation

To install `abhinav_greeting`, use the following command with `pip`:

```bash
pip install abhinav_greeting
```

## Usage
To use the greeting function from the package, you need to import it and call it with a dictionary containing your personal information (e.g., name). Below is an example of how to use the greeting function:

```python
from abhinav_greeting import greeting

# Define headers with personal details
headers = {'Name': 'Abhinav'}

# Print the greeting message
print(greeting(headers))
```

## Example Output:
```txt
Hello, Abhinav! nice to meet you.
```