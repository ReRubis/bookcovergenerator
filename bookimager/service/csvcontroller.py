from bookimager.service.csvimagener import CsvImageGenerator
from bookimager.service.imagedown import ImageDownloader
from bookimager.service.gener_integration import DALLERequest
from bookimager.models.book import CsvBookRequest
from bookimager.service.drawer import Drawer
import asyncio
import os


class CsvController:
    def __init__(
        self,
        generator: CsvImageGenerator,
        downloader: ImageDownloader,
        drawer: Drawer,
    ):
        self.generator = generator
        self.downloader = downloader
        self.drawer = drawer

    async def handle_image_generation(
        self,
    ) -> list[CsvBookRequest]:
        """Uses the csv data to request images.
        """
        data = await self.generator.read_csv()
        return await self.generator.handle_image_generation(data)

    async def handle_image_download(
        self,
        data: list[CsvBookRequest]
    ) -> list[CsvBookRequest]:
        """Uses the csv data to download images.
        """
        data = await self.downloader.new_csv(data)
        return await self.downloader.download_images(data)

    def draw_titles_on_images(
        self,
        data: list[CsvBookRequest],
        csv_path: str,
    ) -> None:
        """Draws the titles on the images.
        """
        name = os.path.basename(csv_path)[:-4:]
        self.drawer.construct_scv_png(
            data,
            name
        )


if __name__ == "__main__":

    csv_path = "test.csv"

    generator_engine = DALLERequest()

    generator = CsvImageGenerator(
        generator_engine,
        csv_path
    )
    downloader = ImageDownloader(
        csv_path
    )
    drawer = Drawer()
    controller = CsvController(
        generator,
        downloader,
        drawer
    )

    async def test():
        data = await controller.handle_image_generation()
        await controller.handle_image_download(data)

        controller.draw_titles_on_images(
            data,
            csv_path
        )

    asyncio.run(test())
