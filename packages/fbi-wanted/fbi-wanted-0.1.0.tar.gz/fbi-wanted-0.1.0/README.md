# FBI Wanted

## Overview
The FBI Wanted is a Python package that provides an interface to the FBI's Wanted API. It allows users to search for wanted persons with various filters such as name, race, hair color, eye color, sex, and field offices. The library handles pagination and retrieves all relevant results asynchronously.

## Installation
You can install the FBI Wanted Library using pip. Run the following command in your terminal:

```
pip install fbi-wanted
```

## Usage
Here is a simple example of how to use the FBI Wanted Library:

```python
from fbi_wanted.fbi_wanted import FBIWanted

# Search for wanted persons by name
results = FBIWanted.search(name="John Doe")

# Print the results
for person in results:
    print(person)
```

## Features
- Search for wanted persons with optional filters.
- Asynchronous fetching of paginated results.
- Easy integration with Python applications.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.