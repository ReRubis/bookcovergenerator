import subprocess
from bookimager.models.book import Book
import os


def draw_book(book: Book) -> None:
    with open('template.svg', 'r') as f:
        template = f.read()

    template = template.replace('TITLE', book['title'])
    template = template.replace('AUTHOR', book['author'])

    with open('template.svg', 'w') as f:
        f.write(template)


def convert_to_png(
    input_file: str = 'template.svg', 
    output_file: str = 'output.png'
) -> None:
    """
    Converts the input file to a png file
    """
    subprocess.run(['inkscape', '-z', input_file, f'--export-png={output_file}'])


def construct_png(book: dict[str, str]) -> None:
    draw_book(book)
    convert_to_png()