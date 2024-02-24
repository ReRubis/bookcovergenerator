import asyncio
from bookimager.config import CONFIG
from bookimager.models.book import Book
from bookimager.service.gener_integration import DALLERequest
from bookimager.service.drawer import Drawer
from bookimager.service.service import MainService

import os

import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
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

    @commands.hybrid_group(name="get")
    async def parent_command(self, ctx: commands.Context) -> None:
        """
        No idea.
        """
        ...

    @parent_command.command(name="list_generated_csvs")
    async def list_scvs(self, ctx: commands.Context) -> None:
        """
        List the generated csvs
        """
        scvs = os.listdir('./generated_csvs')
        await ctx.send(scvs)

    @parent_command.command(name="start_showcase")
    async def start_showcase(
        self,
        ctx: commands.Context,
        csv_name: str,
    ) -> None:
        """
        Start the showcase
        """
        if not os.path.exists(f'./generated_csvs/{csv_name}'):
            await ctx.send("The csv does not exist")
            return

        await ctx.send("Starting the showcase")

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
            service.generate_image(book, prompt)
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while generating the cover.")
            return

        await ctx.send(
            f"Here's the cover for {title} by {author}",
            file=discord.File(f'./redacted_images/{isbn}.png')
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))


# @bot.event
# async def on_ready():
#     await bot.tree.sync()


async def main():

    await setup(bot)

    async with bot:

        await bot.start(CONFIG['DISCORD_BOT_TOKEN'])


if __name__ == '__main__':
    asyncio.run(main())
