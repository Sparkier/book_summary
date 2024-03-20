"""Server interface for the latent retrieval demo."""
import json
import asyncio
import uuid
from pathlib import Path
from flask import Flask, jsonify, send_file, request
from ebooklib import epub
from image_generator import generate_image_from_text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
OK_STATUS = 200
ERROR_STATUS = 400
TEXT_TYPE = {'ContentType': 'text/plain'}
JSON_TYPE = {'ContentType': 'application/json'}
DATA_DIR = Path('data')
UPLOAD_FOLDER = Path('data')
ALLOWED_EXTENSIONS = {'.epub'}

def allowed_file(filename: str):
    """Check if the file is an epub file

    Args:
        filename (str): Name of the file

    Returns:
        (Boolean): True or False
    """
    return Path(filename).suffix in ALLOWED_EXTENSIONS


@app.route('/api/image', methods=['POST'])
async def generate_image():
    """Generate an image on the server based on client input.

    Returns:
        Response: Status of the image generation.
    """
    data = request.get_json()
    src = data.get('src')
    try:
        parts = src.split('/')
        book = parts[3]
        filename = None

        if '/images' in src:
            filename = DATA_DIR / book / "book_summary-version-.png"
        if '/chapters' in src:
            chapter = int(parts[5])
            filename = DATA_DIR / book / \
                f"chapter-{chapter:03d}_chapter_summary-version-.png"
        if '/summarized_paragraphs' in src:
            chapter = int(parts[5])
            paragraph = int(parts[7])
            filename = DATA_DIR / book / \
                f"chapter-{chapter:03d}_paragraph_summary-{paragraph:04d}-version-.png"
        if '/paragraphs' in src:
            chapter = int(parts[5])
            paragraph = int(parts[7])
            filename = DATA_DIR / book / \
                f"chapter-{chapter:03d}_paragraph-{paragraph:04d}-version-.png"

        if filename is None:
            return jsonify({'error': 'Unknown route type'}), ERROR_STATUS

        counter = 1
        text = data.get('prompt')
        basefilename = filename
        while filename.exists():
            # If the file exists, generate a new filename with an incrementing counter
            filename = basefilename.with_stem(
                f"{basefilename.stem}{counter}")
            counter += 1
        output_path = str(filename)
        await asyncio.create_subprocess_exec(generate_image_from_text(text, output_path))
        return jsonify({'message': 'Image successfully generated'}), OK_STATUS

    except (FileNotFoundError, ValueError) as e:
        return jsonify({'error': f'Error generating image: {str(e)}'}), ERROR_STATUS


@app.route('/api/book', methods=['POST'])
async def upload_book():
    """Upload a book in EPUB format and create a folder with the book title.

    Returns:
        Response: Status of the upload request.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), ERROR_STATUS

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), ERROR_STATUS

    if file and allowed_file(file.filename):
        folder_path = UPLOAD_FOLDER / uuid.uuid4().__str__()
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / 'book.epub'
        file.save(file_path)

        # Extract the title from the EPUB metadata
        book = epub.read_epub(file_path)
        title = book.get_metadata('DC', 'title')
        title = title[0][0] if title else None

        if title:
            book_metadata = {
                'title': title
            }
            with open(folder_path / 'metadata.json', 'w') as file:
                json.dump(book_metadata, file)
            summarizer_command = [
                "python", "book_summarizer.py",
                "--input_file", str(file_path),
                "--output_dir", str(folder_path)
            ]
            await asyncio.create_subprocess_shell(' '.join(summarizer_command))

            return jsonify({'message': 'File successfully uploaded', 'title': title}), OK_STATUS
        return jsonify({'error': 'Failed to extract book title'}), ERROR_STATUS

    return jsonify({'error': 'Invalid file type'}), ERROR_STATUS


@app.route('/api/books', methods=['GET'])
def get_books():
    """Get list of books.

    Returns:
        Response<string[]>: book titles.
    """
    data = []
    for path in DATA_DIR.iterdir():
        if path.is_dir():
            title = ''
            with open(path / 'metadata.json', encoding='utf8') as json_file:
                title = json.load(json_file)["title"]
            data.append({
                'uuid': path.stem,
                'title': title
            })
    
    return jsonify(data)


@app.route('/api/books/<book>')
def get_book(book):
    """Get summarized book information.

    Args:
        book (string): uuid of the book

    Returns:
        Response: summaries of the book, its chapters, and paragraphs.
    """
    path = DATA_DIR / book / "summarized.json"
    if not path.exists():
        return jsonify({'error': 'Book not found'}), ERROR_STATUS
    with open(path, encoding='utf8') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route('/api/books/<book>/metadata')
def get_book_metadata(book):
    """Get book metadata.

    Args:
        book (string): uuid of the book

    Returns:
        Response: book metadata.
    """
    with open(DATA_DIR / book / 'metadata.json', encoding='utf8') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route('/api/books/<book>/title')
def get_title(book):
    """Get book title.

    Args:
        book (string): name of the book

    Returns:
        string: book title.
    """
    with open(DATA_DIR / book / 'summarized.json', encoding='utf8') as json_file:
        data = json.load(json_file)["book"]["title"]
    return jsonify(data)


@app.route('/api/books/<book>/images/<int:version>')
def get_book_summary_image(book, version):
    """Get image representation of the summarized book.

    Args:
        book (string): name of the book
        version (int): version number (default: None).

    Returns:
        Response: book image representation.
    """

    filename = DATA_DIR / book / \
        f"book_summary-version-{version}.png"

    return send_file(filename, mimetype='image/png')


@app.route('/api/books/<book>/chapters/<int:chapter>/images/<int:version>')
def get_chapter_summary_image(book, chapter: int, version):
    """Get image representation of the summarized chapter.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        version (int): version number (default: None).

    Returns:
        Response: chapter image representation.
    """

    filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_chapter_summary-version-{version}.png"

    return send_file(filename, mimetype='image/png')


@app.route('/api/books/<book>/chapters/<int:chapter>/'
           'summarized_paragraphs/<int:paragraph>/images/<int:version>')
def get_paragraph_summary_image(book, chapter: int, paragraph: int, version):
    """Get image representation of the summarized paragraph.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): the paragraph index within the chapter.
        version (int): version number (default: None).

    Returns:
        Response: paragraph image representation.
    """

    filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_paragraph_summary-{paragraph:04d}-version-{version}.png"

    return send_file(filename, mimetype='image/png')


@app.route('/api/books/<book>/chapters/<int:chapter>/'
           'paragraphs/<int:paragraph>/images/<int:version>')
def get_paragraph_image(book, chapter: int, paragraph: int, version):
    """Get image representation of the full paragraph.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): the paragraph index within the chapter.
        version (int): version number (default: None).

    Returns:
        Response: paragraph image representation.
    """

    filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_paragraph-{paragraph:04d}-version-{version}.png"

    return send_file(filename, mimetype='image/png')


@app.route('/api/books/<book>/image/versions')
def get_num_book_summary_images(book):
    """Get the number of versions for a book summary image.

    Args:
        book (string): name of the book

    Returns:
        Response: JSON with the number of versions.
    """
    counter = 0
    base_filename = DATA_DIR / book / "book_summary.png"
    while (base_filename.with_name(f"{base_filename.stem}-version-{counter}.png")).exists():
        counter += 1
    return jsonify({'versions': counter})


@app.route('/api/books/<book>/chapters/<int:chapter>/image/versions')
def get_num_chapter_summary_images(book, chapter):
    """Get the number of versions for a chapter summary image.

    Args:
        book (string): name of the book
        chapter (int): chapter index.

    Returns:
        Response: JSON with the number of versions.
    """
    counter = 0
    base_filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_chapter_summary.png"
    while (base_filename.with_name(f"{base_filename.stem}-version-{counter}.png")).exists():
        counter += 1
    return jsonify({'versions': counter})


@app.route('/api/books/<book>/chapters/<int:chapter>'
           '/summarized_paragraphs/<int:paragraph>/image/versions')
def get_num_paragraph_summary_images(book, chapter, paragraph):
    """Get the number of versions for a paragraph summary image.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): paragraph index within the chapter.

    Returns:
        Response: JSON with the number of versions.
    """
    counter = 0
    base_filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_paragraph_summary-{paragraph:04d}.png"
    while (base_filename.with_name(f"{base_filename.stem}-version-{counter}.png")).exists():
        counter += 1
    return jsonify({'versions': counter})


@app.route('/api/books/<book>/chapters/<int:chapter>/paragraphs/<int:paragraph>/image/versions')
def get_num_paragraph_images(book, chapter, paragraph):
    """Get the number of versions for a paragraph image.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): paragraph index within the chapter.

    Returns:
        Response: JSON with the number of versions.
    """
    counter = 0
    base_filename = DATA_DIR / book / \
        f"chapter-{chapter:03d}_paragraph-{paragraph:04d}.png"
    while (base_filename.with_name(f"{base_filename.stem}-version-{counter}.png")).exists():
        counter += 1
    return jsonify({'versions': counter})


if __name__ == '__main__':
    app.run(debug=True)
