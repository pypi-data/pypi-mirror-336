# Abhinav Greetings

A simple Python package that returns personalized greeting messages.

## Installation

To install this package, use pip:

## Usage

Here's an example of how to use the `greeting` function:

```python
from abhinav_greetings import greeting

headers = {'Name': 'John'}
print(greeting(headers))
```

## Output
Hello John, nice to meet you

<p>If no name is provided in the headers:

headers = {}
print(greeting(headers))

<p>No name provided inside header
