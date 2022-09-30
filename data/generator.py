#! /usr/bin/env python3
"""Using Stable Diffusion to generate images from a prompt."""
import re
import json
import argparse
from pathlib import Path
import keras_cv
from PIL import Image


def to_safe_filename(string):
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c==' ']).rstrip()


def parse_json(file_name):
    with open(file_name) as f:
        return json.load(f)


def generate_image_from_text(model, output_dir, text, book_title, level, paragraph_idx, sentence_idx):
    print(book_title, level, paragraph_idx, sentence_idx)
    output_dir = Path(output_dir / to_safe_filename(book_title) / level)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating image for text:", text)

    generated_images = model.text_to_image(text, batch_size=1)
    im = Image.fromarray(generated_images[0])

    file_name = output_dir / f"{paragraph_idx}-{sentence_idx}-{to_safe_filename(text)}.png"
    im.save(file_name)


def iterate_level(mode, output_dir, book_title, level, content_in_level):
    for paragraph_idx, paragraph in enumerate(content_in_level):
        for sentence_idx, sentence in enumerate(re.split('[.?]', paragraph)):
            generate_image_from_text(model, output_dir, sentence, book_title, level, paragraph_idx, sentence_idx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Json to images')
    parser.add_argument('--input_file', type=str, help='input json file')
    parser.add_argument('--output_dir', type=str, help='output dir')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    book_content = parse_json(Path(args.input_file))
    book = book_content["book"]

    model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

    for level in ["1"]:
        iterate_level(model, output_dir, book["title"], level, book[level])
