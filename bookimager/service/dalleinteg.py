from bookimager.models.book import Book
from bookimager.config import CONFIG
from openai import OpenAI


class DALLERequest():
    def __init__(self):
        self.client = OpenAI(
            api_key=CONFIG['OPENAI_KEY']
        )

    def generate_image(self, prompt: str) -> str:
        """Make a request to the OpenAI API to generate an image using DALL-E.

        args: 
            prompt (str): The text prompt to generate an image from.

        returns:
            str: The URL of the generated image.
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url


if __name__ == "__main__":
    book = Book(
        "978-0-394-75856-7",
        "The Cat in the Hat",
        "Dr. Seuss"
    )
    dalle = DALLERequest()
    book.image_url = dalle.generate_image(
        f"Book cover for {book.title} by {book.author}"
    )
    print(book.image_url)
