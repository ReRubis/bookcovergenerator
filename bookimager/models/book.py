from dataclasses import dataclass


@dataclass
class Book():
    isbn: str
    title: str
    author: str
    image_url: str = None


if __name__ == '__main__':
    book = Book(
        '978-3-16-148410-0',
        'The Catcher in the Rye',
        'J.D. Salinger'
    )
