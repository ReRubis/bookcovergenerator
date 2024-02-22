from bookimager.models.book import Book
from bookimager.config import CONFIG
from typing import Protocol, Literal
import json
import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)


class ImageGeneratorProtocol(Protocol):
    """
    A protocol for the image generator
    """

    async def generate_image(
        self,
        prompt: str,
        version: Literal['dall-e-2', 'dall-e-3'] = 'dall-e-2',
    ) -> str:
        """
        Generate an image from a text prompt using the DALL-E model.

        args:
            prompt (str): The prompt to generate the image from.
            number (int): The number of images to generate.
            version (str): The version of the DALL-E model to use.

        returns:
            str: The URL of the generated image.
        """
        ...


class DALLERequest():
    def __init__(self):
        self.key = CONFIG['OPENAI_KEY']

    async def generate_image(
        self,
        prompt: str,
        version: Literal['dall-e-2', 'dall-e-3'] = 'dall-e-2',
    ) -> str:
        """
        Generate an image from a text prompt using the DALL-E model.

        args:
            prompt (str): The prompt to generate the image from.
            number (int): The number of images to generate.
            version (str): The version of the DALL-E model to use.

        returns:
            str: The URL of the generated image.
        """
        url = "https://api.openai.com/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": version,
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
        }

        async with aiohttp.ClientSession() as session:

            logger.info("Requesting image from DALL-E")

            async with session.post(
                url,
                headers=headers,
                data=json.dumps(data)
            ) as response:
                response_data = await response.json()
                return response_data['data'][0]['url']


if __name__ == "__main__":
    book = Book(
        "978-0-394-75856-7",
        "The Cat in the Hat",
        "Dr. Seuss"
    )
    dalle = DALLERequest()

    async def test_generate_image():
        book.image_url = await dalle.generate_image(
            "A cat in a hat sitting on a mat"
        )
        print(book.image_url)

    asyncio.run(test_generate_image())
