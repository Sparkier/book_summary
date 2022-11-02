"""Providing utility functitons for the backend."""
import json

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def parse_json(file_name):
    """Parsing a json file.

    Args:
        file_name (Path): the local file to be parsed

    Returns:
        json: the parsed json file
    """
    with open(file_name, encoding="utf8") as json_file:
        return json.load(json_file)


def parse_chapter(ch_num, chapter):
    """Parse an individual chapter of an epub file.

    Args:
        ch_num (int): the chapter to parse by its number
        chapter (object): the chapter object that is to be parsed

    Returns:
        _type_: _description_
    """
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    headings = soup.find_all('h1')
    if headings:
        title = headings[0].text
    else:
        headings = soup.find_all('h2')
        if headings:
            title = headings[0].text
        else:
            title = ""
    title = title.strip()

    # Extract paragraphs.
    # Some will start/end with newlines (strip fixes this)
    # Some contain '\n     ' (for formating purposes?). Replace those.
    paragraphs = [para.get_text().replace('\n     ', '').strip() for para in soup.find_all('p')]
    return {"num": ch_num, "title": chapter.title, "paragraphs": paragraphs}


def parse_epub(path):
    """Parse an epub into individual chapters.

    Args:
        path (string): where to find the epub file to be parsed

    Returns:
        object: the parsed book with title and chapters
    """
    book = epub.read_epub(path)

    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    epub_chapters = [item for item in items if item.is_chapter()]
    chapters = [parse_chapter(ch_num, chapter) for ch_num, chapter in enumerate(epub_chapters)]

    return {"book": {"title": book.get_metadata('DC', 'title')[0][0], "chapters": chapters}}
