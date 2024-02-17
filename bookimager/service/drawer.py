import subprocess
import requests
from bookimager.models.book import Book
import time
import os


class Drawer():
    """A class to handle drawing text on a book cover
    """

    def __init__(self):
        return None

    def _draw_book(self,  book: Book) -> None:
        """Edits the svg file to include the book's title and author"""
        with open('template.svg', 'r') as f:
            template = f.read()

        template = template.replace(
            'ISBN', f'"./generated_images/{book.isbn}.png"'
        )
        template = template.replace('TITLE', book.title)
        template = template.replace('AUTHOR', book.author)

        with open('template.svg', 'w') as f:
            f.write(template)

    def _convert_to_png(
        self,
        book: Book,
        svg_template: str = 'template.svg',
    ) -> None:
        """
        Converts the input file to a png file
        """
        subprocess.run([
            'inkscape',
            '-z',
            svg_template,
            f'--export-png=./redacted_images/{book.isbn}.png'
        ])

    def _restore_template(
        self,
        input_file: str = 'template.svg'
    ) -> None:
        """Restores the template file to its original state
        """
        with open(input_file, 'w') as f:
            f.write(
                '<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
                '<image xlink:href=ISBN x="0" y="0" width="1024" height="1024"/>'
                '<rect x="112" y="700" width="800" height="250" fill="black" fill-opacity="0.45"/>'
                '<text x="512" y="900" font-family="Arial" font-size="70" fill="white" text-anchor="middle">AUTHOR</text>'
                '<text x="512" y="800" font-family="Arial" font-size="70" fill="white" text-anchor="middle">TITLE</text>'
                '</svg>'
            )

    def _download_image(
        self,
        book: Book,
    ):
        """Downloads the image from the URL"""
        response = requests.get(book.image_url)
        with open(f'./generated_images/{book.isbn}.png', 'wb') as f:
            f.write(response.content)

    def construct_png(
        self,
        book: Book,
        input_file: str = 'template.svg',
    ) -> None:
        """Constructs a png file from the input file"""
        self._download_image(book)
        self._draw_book(book)
        self._convert_to_png(book)
        time.sleep(1)
        os.remove(f'./generated_images/{book.isbn}.png')
        self._restore_template(input_file)


if __name__ == '__main__':
    book = Book(
        '978-3-16-148410-0',
        'The Catcher in the Rye',
        'J.D. Salinger',
        'https://covers.openlibrary.org/b/id/554615-L.jpg'
    )
    drawer = Drawer()
    # drawer.construct_png(book)
    drawer._restore_template()
