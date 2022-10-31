#! /usr/bin/env python3
"""Using Stable Diffusion to generate images from a prompt."""
import argparse
from pathlib import Path

import keras_cv
from PIL import Image

import util


def to_safe_filename(string):
    """Convert a string to a safe filename.

    Args:
        string (string): the string to be converted to a safe filename

    Returns:
        string: the save filename after conversion
    """
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def generate_image_from_text(model, output_dir, text, text_idx):
    """Generating an image from a text segment using a diffusion model.

    Args:
        model (Model): the ml diffusion model used to generate the image
        output_dir (Path): where to save the generated image
        text (string): the prompt for which an image is to be generated
        text_idx (string): the index of the prompt within the level
    """
    print(output_dir, text_idx)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating image for text:", text)
    # Model does not support more than 77 tokens
    max_length = 77
    generated_images = model.text_to_image(text[:max_length], batch_size=1)
    diffusion_image = Image.fromarray(generated_images[0])
    # Windows does not support too long filenames
    file_name_max_length = 250
    file_name = output_dir / \
        f"{text_idx}-{to_safe_filename(text[:file_name_max_length])}.png"
    diffusion_image.save(file_name)


def iterate_level(model, output_dir, content_in_level):
    """Iterate all the content of a level to create images for the texts.

    Args:
        model (Model): the diffusion model to create images with
        output_dir (string): where to write the resulting images
        content_in_level (List[string]): the content of the current level
    """
    for idx, text in enumerate(content_in_level):
        if not to_safe_filename(text):
            continue
        generate_image_from_text(model, output_dir, text, idx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Book to images')
    parser.add_argument('--input_file', type=str, help='input json/epub file')
    parser.add_argument('--output_dir', type=str, help='output dir')
    args = parser.parse_args()

    target_dir = Path(args.output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    input_file = Path(args.input_file)
    if input_file.suffix == ".json":
        book_content = util.parse_json(input_file)
    book = book_content["book"]

    diffusion_model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

    book_dir = Path(target_dir / to_safe_filename(book["title"]))
    for chapter in book["chapters"]:
        ch_num = chapter['num']

        iterate_level(diffusion_model, Path(book_dir, "chapters", str(ch_num),
                      "paragraphs"), chapter["paragraphs"])
        iterate_level(diffusion_model, Path(book_dir, "chapters", str(ch_num),
                      "paragraph_summaries"), chapter["paragraph_summaries"])
        iterate_level(diffusion_model, Path(book_dir, "chapters", str(ch_num),
                      "chapter_summary"), [chapter["chapter_summary"]])

    iterate_level(diffusion_model, Path(book_dir, "book_summary"),
                  [book["book_summary"]])
