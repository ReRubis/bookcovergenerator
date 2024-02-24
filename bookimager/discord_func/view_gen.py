

import discord
from discord.ui import Button, View
import os


class CoverSelectPanel(View):

    async def interaction_check(self, interaction: discord.Interaction):
        """Reacts to the button clicks

        Saves the cover and updates the view

        """
        csv_name, isbn, isbn_count, cover = interaction.data['custom_id'].split(
            '+'
        )

        print(csv_name, isbn, isbn_count, cover)

        if cover == 'stop':
            await interaction.response.send_message(
                "The showcase has been stopped",
                ephemeral=True
            )
            return

        if cover == 'discard_all':
            await interaction.response.send_message(
                "All covers have been discarded",
                ephemeral=True
            )

        if not os.path.exists(f'./redacted_images/{csv_name}/{isbn}/{cover}'):
            await interaction.response.send_message(
                "The cover does not exist",
                ephemeral=True
            )

        if cover != 'discard_all':
            os.rename(
                f'./redacted_images/{csv_name}/{isbn}/{cover}',
                f'./saved_images/{isbn}.png'
            )

        files = os.listdir(f'./redacted_images/{csv_name}/{isbn}')
        for file in files:
            os.remove(f'./redacted_images/{csv_name}/{isbn}/{file}')

        try:
            view, files_list = create_view(
                csv_name,
                int(isbn_count)+1
            )
        except Exception as e:
            print(e)

        if view is None:
            await interaction.response.send_message(
                f'Cover {isbn_count} for {isbn} has been saved \n' +
                'There are no more covers to show',
            )
            files = os.listdir(f'./redacted_images/{csv_name}/')
            for file in files:
                os.rmdir(f'./redacted_images/{csv_name}/{file}')
            os.rmdir(f'./redacted_images/{csv_name}')
            return

        try:
            await interaction.message.edit()
            await interaction.response.send_message(
                f'Cover {isbn_count} for {isbn} has been saved',
                files=[*files_list],
                view=view
            )
        except Exception as e:
            print(e)


def create_view(
    csv_name: str,
    isbn_count: int
) -> tuple[View, list[discord.File]]:

    isbns = os.listdir(f'./redacted_images/{csv_name}')
    isbns.sort()

    if len(isbns) == isbn_count:
        return None, None

    redacted_covers = os.listdir(
        f'./redacted_images/{csv_name}'
        + f'/{isbns[isbn_count]}'
    )

    buttons = []
    files_list = []
    count = 1

    for cover in redacted_covers:
        try:
            new_button = Button(
                label=f'Cover {count}',
                style=discord.ButtonStyle.primary,
                custom_id=f'{
                    csv_name}+{isbns[isbn_count]}+{str(isbn_count)}+{cover}'
            )

            new_file = discord.File(
                f'./redacted_images/{csv_name}/{
                    isbns[isbn_count]}/{cover}'
            )
        except Exception as e:
            print(e)
        buttons.append(new_button)
        files_list.append(new_file)
        count += 1

    finish_button = Button(
        label='Stop',
        style=discord.ButtonStyle.gray,
        custom_id='stop'
    )

    discard_all_button = Button(
        label='Discard all',
        style=discord.ButtonStyle.red,
        custom_id='discard_all'
    )

    buttons.append(finish_button)
    buttons.append(discard_all_button)

    view = CoverSelectPanel()
    for button in buttons:
        view.add_item(button)

    return view, files_list
