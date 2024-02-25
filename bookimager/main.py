import asyncio
from bookimager.config import CONFIG
from bookimager.models.book import Book
from bookimager.service.gener_integration import DALLERequest
from bookimager.service.drawer import Drawer
from bookimager.service.service import MainService
from bookimager.service.imagedown import ImageDownloader
from bookimager.service.csvimagener import CsvImageGenerator
from bookimager.service.csvcontroller import CsvController
from bookimager.discord_func.view_gen import create_view

import os

import discord
from discord.ext import commands
from discord.interactions import Interaction

import logging


logger = logging.getLogger(__name__)

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

description = 'Covers for books'


bot = commands.Bot(
    command_prefix="?",
    intents=intents,
)


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_group(name="bookimager")
    async def parent_command(self, ctx: commands.Context) -> None:
        """
        No idea.
        """
        ...

    @parent_command.command(name="send_csv")
    async def send_csv(
        self,
        ctx: commands.Context,
        csv: discord.Attachment
    ):
        """Takes the csv file and stars the process of generating the covers.
        """
        logger.info(f"Received a csv file {csv.filename}")
        if not os.path.exists('./redacted_images'):
            os.mkdir('./redacted_images')

        csv_path = f'./{csv.filename}'

        try:
            await csv.save(csv_path)
            logger.info(f"CSV file saved as {csv_path}")
        except Exception as e:
            logger.error(e)

        await ctx.defer()

        engine = DALLERequest()

        generator = CsvImageGenerator(
            engine,
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

        try:
            logger.info("Starting the generation process")
            await controller.run_generation(
                csv_path
            )

        except Exception as e:
            logger.error(e)
        await ctx.send("CSV file received")

    @parent_command.command(name="list_finished_csvs")
    async def list_scvs(self, ctx: commands.Context) -> None:
        """
        List the generated csvs
        """
        files = os.listdir('./redacted_images')
        directories = [f for f in files if os.path.isdir(
            f'./redacted_images/{f}'
        )]
        await ctx.send(directories)

    @parent_command.command(name="start_showcase")
    async def start_showcase(
        self,
        ctx: commands.Context,
        csv_name: str,
    ) -> None:
        """
        Start the showcase
        """

        isbns_count = 0
        logger.info(f"Starting the showcase for {csv_name}")

        if not os.path.exists(f'./redacted_images/{csv_name}'):
            await ctx.send("The csv does not exist")
            return

        view, files_list = create_view(
            csv_name,
            isbns_count
        )

        try:
            await ctx.send(
                f"Starting the showcase for {csv_name}",
                files=[
                    *files_list
                ],
                view=view

            )
        except Exception as e:
            print(e)

    @parent_command.command(name="cover")
    async def sub_command(
        self,
        ctx: commands.Context,
        prompt: str,
        title: str,
        author: str,
        isbn: str
    ) -> None:
        """
        Return a cover for a book

        Args:
            prompt (str): The prompt to generate the cover
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN of the book
        """
        book: Book = Book(isbn, title, author)
        drawer: Drawer = Drawer()
        ai: DALLERequest = DALLERequest()
        service: MainService = MainService(ai, drawer)

        await ctx.defer()

        try:
            await service.generate_image(book, prompt)
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while generating the cover.")
            return

        await ctx.send(
            f"Here's the cover for {title} by {author}",
            file=discord.File(f'./redacted_images/{isbn}.png')
        )


@bot.command()
async def test_wqqwrqwrtest(interaction: Interaction) -> None:
    await interaction.response.send_message(
        "This is a test",
        ephemeral=True
    )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))


@bot.event
async def on_button_click(interaction: Interaction) -> None:
    """Handles button clicks
    """


# @bot.event
# async def on_ready():
#     await bot.tree.sync()


async def main():

    await setup(bot)

    async with bot:

        logger.info("Bot started")
        await bot.start(CONFIG['DISCORD_BOT_TOKEN'])


if __name__ == '__main__':
    logger.info("Starting the bot")
    asyncio.run(main())
