import csv
from bookimager.models.book import CsvBookRequest
from bookimager.service.gener_integration import (
    ImageGeneratorProtocol,
    DALLERequest,
)
import asyncio

import time
import logging


logger = logging.getLogger(__name__)


# OPENAI API LIMIT IS 4 IMAGE GENERATIONS PER MINUTE
SEMAPHORE_LIMIT = 4


class CsvImageGenerator():
    """
    - Read the csv file
    - Handle the image generation
    - Download the images

    """

    def __init__(
        self,
        generator: ImageGeneratorProtocol,
        csv_path: str
    ):
        self.generator = generator
        self.csv_data: list[CsvBookRequest] | None = None
        self.semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
        self.csv_path: str = csv_path

    async def read_csv(self) -> list[CsvBookRequest]:
        """
        Read the csv file and return the data
        """

        logger.info('Reading csv file')

        with open(self.csv_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [CsvBookRequest(**row) for row in reader]
            self.csv_data = data
        return data

    async def handle_image_generation(
        self,
        data: list[CsvBookRequest]
    ) -> list[CsvBookRequest]:
        """
        Uses the csv data to request images
        """
        logger.info('Starting to request images from csv')

        tasks = [
            asyncio.create_task(self._request_image(book))
            for book in data for _ in range(int(book.number))
        ]
        results = await asyncio.gather(*tasks)

        results = await self._remove_duplicates(results)

        return results

    async def _request_image(self, row: CsvBookRequest) -> CsvBookRequest:
        """Requests an image from the image generator.
        """

        async with self.semaphore:
            start_time = time.time()

            image_url = await self.generator.generate_image(row.prompt)
            if not row.image_url:
                row.image_url = []
            row.image_url.append(image_url)
            end_time = time.time()

            generation_time = end_time - start_time

            # Only a certain number of requests can be made per minute
            if generation_time < 60:
                await asyncio.sleep(60 - generation_time)

        return row

    async def _remove_duplicates(self, results: list[CsvBookRequest]):
        """Removes duplicates"""

        logger.info('Removing duplicates')
        seen = set()
        unique_results = []
        for result in results:
            if id(result) not in seen:
                unique_results.append(result)
                seen.add(id(result))

        return unique_results


if __name__ == '__main__':

    generator = DALLERequest()
    csv_downloader = CsvImageGenerator(
        generator,
        'test.csv'
    )

    async def main():
        data = await csv_downloader.read_csv()
        results = await csv_downloader.handle_image_generation(data)
        print(results)

        # Save resutls to new csv
        with open('new_test.csv', 'w') as file:
            writer = csv.DictWriter(
                file, fieldnames=results[0].__dict__.keys())
            writer.writeheader()
            for row in results:
                writer.writerow(row.__dict__)

        # csv_downloader.request_images()
        # csv_downloader.download_images()
        # csv_downloader.slam_text()

    asyncio.run(main())
