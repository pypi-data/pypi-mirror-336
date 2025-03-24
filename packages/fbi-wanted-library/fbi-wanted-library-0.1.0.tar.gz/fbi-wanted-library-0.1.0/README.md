# FBI Wanted Library

## Overview
The FBI Wanted Library is a Python package that provides an interface to search for wanted persons using the FBI's Wanted API. It allows users to filter search results based on various criteria such as name, race, hair color, eye color, sex, and field offices.

## Installation
You can install the library using pip. Run the following command in your terminal:

```
pip install fbi-wanted-library
```

## Usage
Here is a simple example of how to use the FBI Wanted Library:

```python
from fbi_wanted.fbi_wanted import FBIWanted

# Search for wanted persons with specific criteria
results = FBIWanted.search(hair_colour="Brown")

# Print the total number of results fetched
print(f"Total results fetched: {len(results)}")

# Print the first 5 results
for result in results[:5]:
    print(result)
```

## Methods
The `FBIWanted` class provides the following methods:

- `search(name: str, race: str, hair_colour: str, eye_colour: str, sex: str, field_offices: str) -> list`: Searches for wanted persons with optional filters.
- `_search(params: dict) -> list`: Fetches all paginated results from the FBI Wanted API with filters.
- `_get_results(params: dict, page: int) -> dict | None`: Fetches results for a specific page using requests.
- `_get_page(params: dict, page: int) -> dict | None`: Fetches a specific page of results.

## Contributing
Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request. Make sure to include tests for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.