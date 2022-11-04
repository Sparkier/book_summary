"""Server interface for the latent retrieval demo."""
import json
from pathlib import Path

from flask import Flask, jsonify, send_file

app = Flask(__name__)
OK_STATUS = 200
ERROR_STATUS = 400
TEXT_TYPE = {'ContentType': 'text/plain'}
JSON_TYPE = {'ContentType': 'application/json'}
DATA_DIR = Path('data')


@app.route('/api/get_books', methods=['GET'])
def get_books():
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
    path = Path(DATA_DIR, book, "summarized.json")
    if not path.exists():
        return jsonify({"book": []})
    return send_file(path, mimetype='application/json')


@app.route('/api/get_title/<book>')
def get_title(book):
    with open(Path(DATA_DIR, book, 'summarized.json'), encoding='utf8') as json_file:
        data = json.load(json_file)["book"]["title"]
    return jsonify(data)


@app.route('/api/get_book_summary_image/<book>')
def get_book_summary_image(book):
    imgs_dir = Path(DATA_DIR, book, "book_summary")
    filePaths = [file for file in imgs_dir.iterdir() if file.name.startswith('0')]
    return send_file(filePaths[0], mimetype='image/png')


@app.route('/api/get_chapter_summary_image/<book>/<chapter>/<index>')
def get_chapter_summary_image(book, chapter, index):
    imgs_dir = Path(DATA_DIR, book, "chapters", chapter, "chapter_summary")
    filePaths = [file for file in imgs_dir.iterdir() if file.name.startswith(index)]
    return send_file(filePaths[0], mimetype='image/png')


@app.route('/api/get_paragraph_summary_image/<book>/<chapter>/<index>')
def get_paragraph_summary_image(book, chapter, index):
    imgs_dir = Path(DATA_DIR, book, "chapters", chapter, "paragraph_summaries")
    filePaths = [file for file in imgs_dir.iterdir() if file.name.startswith(index)]
    return send_file(filePaths[0], mimetype='image/png')


@app.route('/api/get_paragraph_image/<book>/<chapter>/<index>')
def get_paragraph_image(book, chapter, index):
    imgs_dir = Path(DATA_DIR, book, "chapters", chapter, "paragraphs")
    filePaths = [file for file in imgs_dir.iterdir() if file.name.startswith(index)]
    return send_file(filePaths[0], mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
