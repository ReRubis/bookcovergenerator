import csv
from bookimager.models.book import CsvBookRequest
from bookimager.service.gener_integration import (
    ImageGeneratorProtocol,
    DALLERequest
)
import asyncio
import aiohttp
import aiofiles
import uuid
import time
import logging
import os

logger = logging.getLogger(__name__)

# Number of files downloaded at once
SEMAPHORE_LIMIT = 10


class ImageDownloader:

    def __init__(
        self,
        csv_path: str
    ):
        self.csv_path: str = csv_path
        self.semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async def new_csv(
            self,
            data: list[CsvBookRequest],
    ) -> list[CsvBookRequest]:
        """Used to save the updated csv data to a new file.
        """
        name = os.path.basename(self.csv_path)
        extension = os.path.splitext(name)[1]
        new_name = f'new_{name[:-4:]}{extension}'

        with open(new_name, 'w') as file:
            writer = csv.DictWriter(
                file, fieldnames=data[0].__dict__.keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row.__dict__)

        return data

    async def download_images(self, data: list[CsvBookRequest]):
        """Uses the csv data to download images.
        """
        logger.info('downloading images from csv')
        for row in data:
            if not row.image_url:
                raise ValueError('Image URL not found')

        tasks = [
            asyncio.create_task(self._download_image(row.isbn, url))
            for row in data for url in row.image_url
        ]
        results = await asyncio.gather(*tasks)

    async def _download_image(self, isbn: str, url: str):
        """Downloads the image from the URL and saves it to the file system."""
        async with self.semaphore:

            async with aiohttp.ClientSession() as session:

                async with session.get(url) as response:
                    dir_path = f'generated_images/{self.csv_path[:-4:]}/{isbn}'
                    os.makedirs(dir_path, exist_ok=True)

                    async with aiofiles.open(f'{dir_path}/{uuid.uuid4()}.png', 'wb') as file:
                        await file.write(await response.read())


if __name__ == '__main__':
    print('hello')
