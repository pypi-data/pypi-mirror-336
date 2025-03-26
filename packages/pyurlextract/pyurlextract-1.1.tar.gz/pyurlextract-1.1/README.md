# pyurlextract

**pyurlextract** is a Python library that extracts all possible links and redirections from any shortened URL. It helps in expanding short links to reveal their full URLs and potential redirections.

## Links
**PyPI:** [https://pypi.org/project/pyurlextract/](https://pypi.org/project/pyurlextract/)

## Installation

Install the library using pip:

```sh
pip install pyurlextract
```

## Usage

Here's how you can use **pyurlextract** to extract links from a shortened URL:

```python
from pyurlextract import extract_shorturl

short_url = "link"  # Replace with the actual short URL
full_link, all_links = extract_shorturl(short_url)

if full_link is None:
    print("Failed to expand the URL")
    print("Details:", all_links)
else:
    print("Original URL:", short_url)
    print("Full Link:", full_link)
    print("All Possible Redirections:", all_links)
    print(extract_shorturl(short_url))
```

## Parameters
- `short_url` *(str)*: The shortened URL that needs to be expanded.

## Returns
- `full_link` *(str | None)*: The fully expanded URL or `None` if extraction fails.
- `all_links` *(list)*: A list of all possible redirections found.

## Example Output
```
Original URL: https://bit.ly/example
Full Link: https://example.com/page
All Possible Redirections: ['https://example.com/page', 'https://redirect.example.com']
```

## Features
- Expands shortened URLs from various services.
- Extracts all possible redirections from a given URL.
- Easy-to-use Python interface.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the [MIT License](https://github.com/Deadpool2000/pyurlextract/blob/main/LICENSE).


