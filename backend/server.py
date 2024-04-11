"""Server interface for the latent retrieval demo."""
import json
import asyncio
from pathlib import Path
from flask import Flask, jsonify, send_file, request
from werkzeug.utils import secure_filename
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

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)

        # Extract the title from the EPUB metadata
        book = epub.read_epub(file_path)
        title = book.get_metadata('DC', 'title')
        title = title[0][0] if title else None

        if title:
            valid_title = ''.join(c if c.isalnum() or c in {
                                  ' ', '-', '_'} else '' for c in title)
            folder_path = UPLOAD_FOLDER / valid_title
            folder_path.mkdir(parents=True, exist_ok=True)
            new_file_path = folder_path / filename
            file_path.rename(new_file_path)
            summarizer_command = [
                "python", "book_summarizer.py",
                "--input_file", str(folder_path / filename),
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
            data.append(path.stem)
    books = {'books': data}
    return jsonify(books)


@app.route('/api/books/<book>')
def get_book(book):
    """Get summarized book information.

    Args:
        book (string): name of the book

    Returns:
        Response: summaries of the book, its chapters, and paragraphs.
    """
    path = DATA_DIR / book / "summarized.json"
    if not path.exists():
        return jsonify({"book": []})
    return send_file(path, mimetype='application/json')


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


@app.route('/api/books/<book_uuid>/images/selected')
def get_selected_images(book_uuid):
    """Get selected images of a book.

    Args:
        book_uuid (string): UUID of the book

    Returns:
        Response: selected image ids of the book, its chapters, and paragraphs.
    """
    path = DATA_DIR / book_uuid / "selected_images.json"

    if not path.exists():
        generate_selected_images(book_uuid)
    return send_file(path, mimetype='application/json')


def generate_selected_images(book_uuid):
    """Generate selected images JSON data for a book and save it to a file.

    Args:
        book_uuid (string): UUID of the book.

    Returns:
        dict: Selected image data for the book.
    """
    json_file_path = DATA_DIR / book_uuid / 'summarized.json'

    with open(json_file_path, encoding='utf8') as json_file:
        data = json.load(json_file)
        chapters = data["book"]["chapters"]

        new_json_data = {
            "bookImageIndex": 0,
            "chapters": []
        }

        for chapter in chapters:
            paragraph_count = len(chapter["paragraphs"])
            new_chapter = {
                "imageIndex": 0,
                "paragraphs": [0] * paragraph_count
            }
            new_json_data["chapters"].append(new_chapter)

    save_path = DATA_DIR / book_uuid / "selected_images.json"
    with open(save_path, 'w', encoding='utf-8') as json_output_file:
        json.dump(new_json_data, json_output_file,
                  ensure_ascii=False, indent=4)

    return new_json_data


@app.route('/api/books/<book_uuid>/images/selected/update', methods=['POST'])
def update_selected_images(book_uuid):
    """Update selected images of a book.

    Args:
        book_uuid (string): UUID of the book

    Returns:
        Response: Message indicating success or failure of the update.
    """
    try:
        updated_selected_images = request.json
        json_file_path = DATA_DIR / book_uuid / 'selected_images.json'

        if not json_file_path.exists():
            generate_selected_images(book_uuid)

        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(updated_selected_images, json_file,
                      ensure_ascii=False, indent=4)

        return jsonify({"message": "Selected images updated successfully."}), 200
    except (FileNotFoundError, ValueError) as e:
        return jsonify({"message": f"Error updating selected images: {str(e)}"}), 500


@app.route('/api/books/<book_uuid>/characters', methods=['POST'])
def save_characters(book_uuid):
    """Save characters of a book.

    Args:
        book_uuid (string): UUID of the book

    Returns:
        Response: Message indicating success or failure of the update.
    """
    try:
        characters_data = request.json
        json_file_path = DATA_DIR / book_uuid / 'characters.json'

        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(characters_data, json_file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Characters updated successfully."}), 200
    except (FileNotFoundError, ValueError) as e:
        return jsonify({"message": f"Error updating characters: {str(e)}"}), 500


@app.route('/api/books/<book_uuid>/characters')
def get_characters(book_uuid):
    """Get characters of a book.

    Args:
        book_uuid (string): UUID of the book

    Returns:
        Response: JSON with characters or an empty list if the file does not exist.
    """
    try:
        json_file_path = DATA_DIR / book_uuid / 'characters.json'

        if not json_file_path.exists():
            return jsonify([])

        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            characters_data = json.load(json_file)

        return jsonify(characters_data)
    except (FileNotFoundError, ValueError) as e:
        return jsonify({"error": f"Error loading characters: {str(e)}"}), 500


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
