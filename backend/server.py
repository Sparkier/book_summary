"""Server interface for the latent retrieval demo."""
import json
import os
import subprocess
from pathlib import Path
from flask import Flask, jsonify, send_file, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from ebooklib import epub
import time

app = Flask(__name__)
CORS(app)

OK_STATUS = 200
ERROR_STATUS = 400
TEXT_TYPE = {'ContentType': 'text/plain'}
JSON_TYPE = {'ContentType': 'application/json'}
DATA_DIR = Path('data')
UPLOAD_FOLDER = Path('data')
ALLOWED_EXTENSIONS = {'epub'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename: str):
    """Check if the file is a epub file

    Args:
        filename (str): Name of the file

    Returns:
        (Boolean): True or False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    """Generate an image on the server based on client input.

    Returns:
        Response: Status of the image generation.
    """
    data = request.get_json()
    src = data.get('src')

    try:
        # Extract book, chapter, paragraph, index from the src path
        _, _, route_type, book, *rest = src.split('/')

        if route_type == 'get_book_summary_image':
            index = int(rest[0])
            filename = Path(DATA_DIR, book, f"book_summary-{index:04d}.png")
        elif route_type == 'get_chapter_summary_image':
            chapter, index = map(int, rest)
            filename = Path(
                DATA_DIR, book, f"chapter-{chapter:03d}_chapter_summary-{index:04d}.png")
        elif route_type == 'get_paragraph_summary_image':
            chapter, paragraph = map(int, rest)
            filename = Path(
                DATA_DIR, book, f"chapter-{chapter:03d}_paragraph_summary-{paragraph:04d}.png")
        elif route_type == 'get_paragraph_image':
            chapter, paragraph = map(int, rest)
            filename = Path(
                DATA_DIR, book, f"chapter-{chapter:03d}_paragraph-{paragraph:04d}.png")
        else:
            return jsonify({'error': 'Unknown route type'}), ERROR_STATUS

        # Adjust the command based on your actual image generation script
        image_generator_command = [
            "python", "image_generator.py",
            "--text", data.get('text'),
            "--output_path", str(filename)
        ]
        subprocess.run(image_generator_command, check=True)
        return jsonify({'message': 'Image successfully generated'}), OK_STATUS
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error generating image: {e.stderr.decode()}'}), ERROR_STATUS


@app.route('/api/upload_book', methods=['POST'])
def upload_book():
    """Upload a book in EPUB format and create a folder with the book title.

    Returns:
        Response: Status der Upload-Anfrage.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), ERROR_STATUS

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), ERROR_STATUS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract the title from the EPUB metadata
        book = epub.read_epub(file_path)
        title = book.get_metadata('DC', 'title')
        title = title[0][0] if title else None

        if title:
            valid_title = ''.join(c if c.isalnum() or c in {
                                  ' ', '-', '_'} else '' for c in title)
            folder_path = os.path.join(
                app.config['UPLOAD_FOLDER'], valid_title)
            os.makedirs(folder_path, exist_ok=True)
            new_file_path = os.path.join(folder_path, filename)
            os.rename(file_path, new_file_path)
            summarizer_command = [
                "python", "book_summarizer.py",
                "--input_file", os.path.join(folder_path, filename),
                "--output_dir", folder_path
            ]
            subprocess.run(summarizer_command, check=False)

            return jsonify({'message': 'File successfully uploaded', 'title': title}), OK_STATUS
        return jsonify({'error': 'Failed to extract book title'}), ERROR_STATUS

    return jsonify({'error': 'Invalid file type'}), ERROR_STATUS


@app.route('/api/get_books', methods=['GET'])
def get_books():
    """Get list of books.

    Returns:
        Response<string[]>: book titles.
    """
    data = []
    for path in DATA_DIR.iterdir():
        if path.is_dir():
            data.append(path.stem)
    books = {
        'books': data
    }
    asd = jsonify(books)
    return asd


@app.route('/api/get_book/<book>')
def get_book(book):
    """Get summarized book information.

    Args:
        book (string): name of the book

    Returns:
        Response: summaries of the book, its chapters, and paragraphs.
    """
    path = Path(DATA_DIR, book, "summarized.json")
    if not path.exists():
        return jsonify({"book": []})
    return send_file(path, mimetype='application/json')


@app.route('/api/get_title/<book>')
def get_title(book):
    """Get book title.

    Args:
        book (string): name of the book

    Returns:
        string: book title.
    """
    with open(Path(DATA_DIR, book, 'summarized.json'), encoding='utf8') as json_file:
        data = json.load(json_file)["book"]["title"]
    return jsonify(data)


@app.route('/api/get_book_summary_image/<book>/<int:index>')
def get_book_summary_image(book, index: int):
    """Get image representation of the summarized book.

    Args:
        book (string): name of the book
        index (int): the index of the image representation.

    Returns:
        Response: book image representation.
    """
    filename = Path(DATA_DIR, book, f"book_summary-{index:04d}.png")
    return send_file(filename, mimetype='image/png')


@app.route('/api/get_chapter_summary_image/<book>/<int:chapter>/<int:index>')
def get_chapter_summary_image(book, chapter: int, index: int):
    """Get image representation of the summarized chapter.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        index (int): the index of the image representation.

    Returns:
        Response: chapter image representation.
    """
    filename = Path(
        DATA_DIR, book, f"chapter-{chapter:03d}_chapter_summary-{index:04d}.png")
    return send_file(filename, mimetype='image/png')


@app.route('/api/get_paragraph_summary_image/<book>/<int:chapter>/<int:paragraph>')
def get_paragraph_summary_image(book, chapter: int, paragraph: int):
    """Get image representation of the summarized paragraph.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): the paragraph index within the chapter.

    Returns:
        Response: paragraph image representation.
    """
    filename = Path(
        DATA_DIR, book, f"chapter-{chapter:03d}_paragraph_summary-{paragraph:04d}.png")
    return send_file(filename, mimetype='image/png')


@app.route('/api/get_paragraph_image/<book>/<int:chapter>/<int:paragraph>')
def get_paragraph_image(book, chapter: int, paragraph: int):
    """Get image representation of the full paragraph.

    Args:
        book (string): name of the book
        chapter (int): chapter index.
        paragraph (int): the paragraph index within the chapter.

    Returns:
        Response: paragraph image representation.
    """
    filename = Path(
        DATA_DIR, book, f"chapter-{chapter:03d}_paragraph-{paragraph:04d}.png")
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
