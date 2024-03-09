from bookimager.service.csvimagener import CsvImageGenerator
from bookimager.service.imagedown import ImageDownloader
from bookimager.service.gener_integration import DALLERequest
from bookimager.models.book import CsvBookRequest
from bookimager.service.drawertwo import Drawer
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

    async def run_generation(
        self,
        csv_path: str
    ) -> None:
        data = await self.handle_image_generation()
        await self.handle_image_download(data)
        self.draw_titles_on_images(
            data,
            csv_path
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
        # data = await controller.handle_image_generation()
        # await controller.handle_image_download(data)

        # print(data)


        data = [CsvBookRequest(isbn='978-0-307-95781-0', title='1984', author='George Orwell', prompt='dystopian future artwork', number='4', image_url=['https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-44oO1jOkVXDlmFtJZ7sfavm0.png?st=2024-03-09T21%3A29%3A29Z&se=2024-03-09T23%3A29%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T12%3A20%3A10Z&ske=2024-03-10T12%3A20%3A10Z&sks=b&skv=2021-08-06&sig=a7D2U7W9F2bZfFz%2B2Q6JsrAEc%2BMtbcFCQxVTh2LPG%2BI%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-Pa4bkROvkcVqH1T585gaxVYk.png?st=2024-03-09T21%3A29%3A29Z&se=2024-03-09T23%3A29%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A23%3A07Z&ske=2024-03-10T18%3A23%3A07Z&sks=b&skv=2021-08-06&sig=GBeKu%2BBuGTb%2BY/L6/U6/xI6bM5xbCefBd9linFnh0Ow%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-9OB6aS8fMJ2fQDxQGKm1ccj9.png?st=2024-03-09T21%3A29%3A29Z&se=2024-03-09T23%3A29%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T01%3A17%3A22Z&ske=2024-03-10T01%3A17%3A22Z&sks=b&skv=2021-08-06&sig=Kh2Qs5BL0BtixRkjPPZeggoIJkNrNOWXidnb3lfjKAI%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-khZ1eaXJ5JswYU3wkhxeQu4O.png?st=2024-03-09T21%3A29%3A29Z&se=2024-03-09T23%3A29%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A18%3A37Z&ske=2024-03-10T18%3A18%3A37Z&sks=b&skv=2021-08-06&sig=LI4gy3Rmu/Jaj7QnNjA9G926PiqEhOU203REm1raVmI%3D']), CsvBookRequest(isbn='978-0-553-21311-6', title='The Catcher in the Rye', author='J.D. Salinger', prompt='abstract representation of teenage angst', number='4', image_url=['https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-ktq11J35RUT4hBcoXdcLgYrA.png?st=2024-03-09T21%3A30%3A29Z&se=2024-03-09T23%3A30%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A19%3A22Z&ske=2024-03-10T18%3A19%3A22Z&sks=b&skv=2021-08-06&sig=JPMXuABEaIMPqwKbcWmrZ6xCV16SUDDgEQ9WgjLrU9o%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-OPgtOdYncHRH7QcD0d16PPFZ.png?st=2024-03-09T21%3A30%3A29Z&se=2024-03-09T23%3A30%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A21%3A34Z&ske=2024-03-10T18%3A21%3A34Z&sks=b&skv=2021-08-06&sig=X1jQpUIVzOjW0x9gNxr9TATMKpHgUbHZhthSSfHRJe8%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-buaBBBsfxzmudAhJWnpF3cJc.png?st=2024-03-09T21%3A30%3A29Z&se=2024-03-09T23%3A30%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A24%3A42Z&ske=2024-03-10T18%3A24%3A42Z&sks=b&skv=2021-08-06&sig=bV6pMnQ0gkc5TXSkRSh%2BifOC2YeduFrcSD2X7ryqqrg%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-jr5GSlpVs4ZU5BFXaERPglLG/user-bNWlfNfqUGs6tSgG9Cn5jZ9o/img-C9HJbYvHHcbuR2wKFrwlQwBC.png?st=2024-03-09T21%3A30%3A29Z&se=2024-03-09T23%3A30%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-09T18%3A20%3A31Z&ske=2024-03-10T18%3A20%3A31Z&sks=b&skv=2021-08-06&sig=Rx3iB9w7PvJwgoLRiQeZ7P7ln1jSVosBMNy0iN0pUIM%3D'])]
        controller.draw_titles_on_images(
            data,
            csv_path
        )

    asyncio.run(test())
