# PyCalibre

PyCalibre is a Python library designed to facilitate interaction with a Calibre ebook library. It provides a set of classes and methods to manage ebooks, their metadata, and the library structure efficiently.

## Features

- Load and manage your Calibre library.
- Add and remove books from the library.
- Search and retrieve book information.
- Handle ebook metadata with ease.

## Installation

To install PyCalibre, you can use Poetry. First, ensure you have Poetry installed, then run:

```bash
poetry install
```

## Usage

To use PyCalibre, you can start by importing the library and initializing your Calibre library instance. Here’s a simple example:

```python
from pycalibre import Library

with Library("path/to/library") as library:
  # Do stuff here
```

The `Library` class acts as a context manager, so you don't need to worry about cleaning up.

You can then easily find books in your library by different criteria:

```python
# ... within a Library context
books = library.find_books(author="Austen")
for book in books:
  print(book.title)
```

Updating books is straightforward as well:

```python
book.update(title="New title", add_tags=["New Tag"], remove_tags=["Old Tag"])
```

You can work with custom columns as if they were native ones:

```python
print(book.my_custom_column)
book.update(my_custom_column="Hello")
```

You can also get all the formats of a book:

```python
for fmt in book.get_formats():
  with open(fmt.file_path, 'rb') as f:
    contents = f.read()
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes. My main motivation in making this package is to help me write maintenance and analysis scripts for my Calibre library, but I am happy for it to be extended to support the needs of others.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.