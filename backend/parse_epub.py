import ebooklib
from ebooklib import epub

def parse_chapter(ch_num, chapter):
    from bs4 import BeautifulSoup
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
    book = epub.read_epub(path)
    
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    epub_chapters = [item for item in items if item.is_chapter()]
    chapters = [parse_chapter(ch_num, chapter) for ch_num, chapter in enumerate(epub_chapters)]        

    return {"title": book.get_metadata('DC', 'title')[0], "chapters": chapters}
