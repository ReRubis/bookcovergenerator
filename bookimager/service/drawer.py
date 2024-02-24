import subprocess
import requests
from bookimager.models.book import Book, CsvBookRequest
import os
import logging


logger = logging.getLogger(__name__)


class Drawer():
    """A class to handle drawing text on a book cover
    """

    def __init__(self):
        return None

    def _draw_book(
            self,
            book: Book,
            file_path: str,
    ) -> None:
        """Edits the svg file to include the book's title and author.
        """

        with open('template.svg', 'r') as f:
            template = f.read()

        template = template.replace(
            'PATH', f'"{file_path}"'
        )

        title_length = len(book.title)

        match title_length:

            case _ if 20 > title_length:
                template = template.replace('FONT_SIZE_TITLE', '"60"')
                template = template.replace('FONT_SIZE_AUTHOR', '"55"')

            case _ if 30 > title_length > 20:
                template = template.replace('FONT_SIZE_TITLE', '"50"')
                template = template.replace('FONT_SIZE_AUTHOR', '"45"')

            case _ if 40 > title_length > 30:
                template = template.replace('FONT_SIZE_TITLE', '"40"')
                template = template.replace('FONT_SIZE_AUTHOR', '"35"')

            case _ if 50 > title_length > 40:
                template = template.replace('FONT_SIZE_TITLE', '"30"')
                template = template.replace('FONT_SIZE_AUTHOR', '"25"')

            case _ if title_length > 50:
                template = template.replace('FONT_SIZE_TITLE', '"20"')
                template = template.replace('FONT_SIZE_AUTHOR', '"15"')

        template = template.replace('TITLE', book.title.upper())
        template = template.replace('AUTHOR', book.author.upper())

        with open('template.svg', 'w') as f:
            f.write(template)

    def _convert_to_png(
        self,
        book: Book,
        svg_template: str = 'template.svg',
        save_path: str = './redacted_images',
        save_name: str = None
    ) -> None:
        """
        Converts the input file to a png file
        """
        path = f'--export-png={save_path}/{book.isbn}.png'

        if save_name:
            path = f'--export-png={save_path}/{save_name}'

        os.makedirs(save_path, exist_ok=True)

        subprocess.run([
            'inkscape',
            '-z',
            svg_template,
            path
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
                '<image xlink:href=PATH x="0" y="0" width="1024" height="1024"/>'
                '<rect x="112" y="700" width="800" height="250" fill="black" fill-opacity="0.85"/>'
                '<text x="512" y="900" font-family="League Spartan" font-weight="bold" font-size=FONT_SIZE_AUTHOR fill="white" text-anchor="middle">AUTHOR</text>'
                '<text x="512" y="800" font-family="League Spartan" font-weight="bold" font-size=FONT_SIZE_TITLE fill="white" text-anchor="middle">TITLE</text>'
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
        self._draw_book(
            book,
            f"./generated_images/{book.isbn}.png"
        )
        self._convert_to_png(book)
        os.remove(f'./generated_images/{book.isbn}.png')
        self._restore_template(input_file)

    def construct_scv_png(
        self,
        books: list[CsvBookRequest],
        csv_folder: str,
        input_file: str = 'template.svg',
    ) -> None:
        """Constructs a png file from the input file"""

        logger.info(
            f'Starting to draw titles on covers in folder {csv_folder}')

        for book in books:
            folder = f'./generated_images/{csv_folder}/{book.isbn}'
            list_of_files = []
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    list_of_files.append(file_path)

            for file in list_of_files:
                self._draw_book(
                    book,
                    file_path=file
                )
                self._convert_to_png(
                    book,
                    input_file,
                    f'./redacted_images/{csv_folder}/{book.isbn}',
                    os.path.basename(file)
                )

                # os.remove(f'./generated_images/{csv_folder}/{book.isbn}/{file}')
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
