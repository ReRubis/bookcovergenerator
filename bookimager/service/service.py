from bookimager.models.book import Book
from bookimager.service.imagegener import DALLERequest
from bookimager.service.drawer import Drawer
import os


class MainService():
    def __init__(
        self,
        generator: DALLERequest,
        drawer: Drawer,
    ):
        self.dalle = generator
        self.drawer = drawer

    def generate_image(self, book: Book, prompt: str) -> None:
        """Generate an image for a book.

        args:
            book (Book): The book to generate an image for.

        returns:
            str: The URL of the generated image.
        """
        image_url = self.dalle.generate_image(
            f"NO TEXT, NO SYMBOLS {prompt}"
        )

        new_book = Book(
            book.isbn,
            book.title,
            book.author,
            image_url
        )

        self.drawer.construct_png(new_book)

    def save_image(self, isbn: str) -> str:
        """Save the image to a file.

        Changes the directory of the image from redacted_images to saved_images
        """
        old_path = f'./redacted_images/{isbn}.png'

        if not os.path.exists(old_path):
            raise FileNotFoundError(f"File {old_path} not found")

        new_path = f'./saved_images/{isbn}.png'
        os.rename(old_path, new_path)


if __name__ == '__main__':
    book = Book(
        isbn="978-0-394-2222-7",
        title="Invisible man",
        author="Ralph Ellison",
    )

    prompt = 'Invisible man grotesque and dark'

    dalle = DALLERequest()
    drawer = Drawer()
    service = MainService(dalle, drawer)

    service.generate_image(book, prompt)
