import subprocess
import requests
from bookimager.models.book import Book, CsvBookRequest
import os
import logging
import imgkit

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
        """Edits the html file to include the book's title and author.
        """

        with open('template.html', 'r') as f:
            template = f.read()

        template = template.replace(
            '"PATH"', f'"{file_path}"'
        )

        title_length = len(book.title)

        match title_length:

            case _ if 20 > title_length:
                template = template.replace('TITLE_FONT_SIZE', '50px')
                template = template.replace('AUTHOR_FONT_SIZE', '50px')

            case _ if 30 > title_length > 20:
                template = template.replace('TITLE_FONT_SIZE', '45px')
                template = template.replace('AUTHOR_FONT_SIZE', '40px')

            case _ if 40 > title_length > 30:
                template = template.replace('TITLE_FONT_SIZE', '35px')
                template = template.replace('AUTHOR_FONT_SIZE', '30px')

            case _ if 50 > title_length > 40:
                template = template.replace('TITLE_FONT_SIZE', '25px')
                template = template.replace('AUTHOR_FONT_SIZE', '20px')

            case _ if title_length > 50:
                template = template.replace('TITLE_FONT_SIZE', '20px')
                template = template.replace('AUTHOR_FONT_SIZE', '15px')

        template = template.replace('TITLE', book.title.upper())
        template = template.replace('AUTHOR', book.author.upper())

        with open('template.html', 'w') as f:
            f.write(template)

    def _convert_to_png(
        self,
        book: Book,
        html_template: str = 'template.html',
        save_path: str = './redacted_images',
        save_name: str = None
    ) -> None:
        """
        Converts the input file to a png file
        """
        path = f'{save_path}/{book.isbn}.png'

        if save_name:
            path = f'{save_path}/{save_name}'

        os.makedirs(save_path, exist_ok=True)

        imgkit.from_file(
                html_template,
                path,
                options = {
                'enable-local-file-access': None
            }
        )



    def _restore_template(
        self,
        input_file: str = 'template.html'
    ) -> None:
        """Restores the template file to its original state
        """
        with open(input_file, 'w') as f:
            with open('base_template.html', 'r') as base:
                f.write(base.read())
           
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
        input_file: str = 'template.html',
    ) -> None:
        """Constructs a png file from the input file"""
        self._download_image(book)
        self._draw_book(
            book,
            f"./generated_images/{book.isbn}.png"
        )
        self._convert_to_png(book)
        # os.remove(f'./generated_images/{book.isbn}.png')
        self._restore_template(input_file)

    def construct_scv_png(
        self,
        books: list[CsvBookRequest],
        csv_folder: str,
        input_file: str = 'template.html',
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

                # os.remove(
                #     f'{file}'
                # )
                self._restore_template(input_file)


if __name__ == '__main__':
    book = Book(
        '978-3-16-148410-0',
        'The Catcher in the Rye The Catcher in the Rye  The Catcher in the Rye The Catcher in the Rye The Catcher in the Rye  The Catcher in the Rye The Catcher in the Rye The Catcher in the Rye  The Catcher in the Rye',
        'J.D. Salinger',
        'https://covers.openlibrary.org/b/id/554615-L.jpg'
    )
    drawer = Drawer()
    drawer.construct_png(book)
    drawer._restore_template()
