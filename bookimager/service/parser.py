import csv
from bookimager.models.book import Book, CsvBookRequest
from bookimager.service.imagegener import ImageGeneratorProtocol, DALLERequest
import asyncio


class CsvImageDownloader():
    """
    - Read the csv file
    - Handle the image generation
    - Download the image

    """

    def __init__(self, generator: ImageGeneratorProtocol):
        self.generator = generator
        self.data: list[CsvBookRequest] | None = None

    async def read_csv(self, file_path: str) -> list:
        """
        Read the csv file and return the data
        """
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [CsvBookRequest(**row) for row in reader]
            self.data = data
        return data

    async def request_images():
        ...

    async def download_images():
        ...

    async def slam_text():
        ...


if __name__ == '__main__':

    generator = DALLERequest()
    csv_downloader = CsvImageDownloader(generator)

    async def main():
        data = await csv_downloader.read_csv('test.csv')
        print(data)

        # csv_downloader.request_images()
        # csv_downloader.download_images()
        # csv_downloader.slam_text()

    asyncio.run(main())
