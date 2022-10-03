#! /usr/bin/env python3
"""Summarize chapters and paragraphs of a book."""
import json
import argparse
from pathlib import Path

from parse_epub import parse_epub

from transformers import pipeline

#  Text-to-image model does not support more than 77 tokens (keras_cv.models.StableDiffusion)
def text_summarization(summarizer, text, min_length=5, max_length=77):
    text_len = len(text)
    summary = summarizer(text, min_length=min(min_length, text_len),
                         max_length=min(text_len, max_length), truncation=True)
    return summary[0]['summary_text']


def parse_json(file_name):
    with open(file_name, encoding="utf8") as f:
        return json.load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Summarize book, chapters and paragraphs')
    parser.add_argument('--input_file', type=str, help='input json/epub file')
    parser.add_argument('--output_dir', type=str,
                        help='output dir. Same as input if unspecified', default=None)
    args = parser.parse_args()
    if args.output_dir is None:
        output_dir = Path(args.input_file).parent
    else:
        output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_file = Path(args.input_file)
    if input_file.suffix == ".json":
        book_content = parse_json(input_file)
    elif input_file.suffix == ".epub":
        book_content = parse_epub(input_file)

    book = book_content["book"]
    summarized_book = book
    model_id = "sshleifer/distilbart-cnn-12-6"
    summarizer = pipeline("summarization", model=model_id)
    chapter_summaries = []
    for ch_num, chapter in enumerate(book["chapters"]):
        paragraph_summaries = [text_summarization(
            summarizer, paragraph) for paragraph in chapter["paragraphs"]]
        chapter_summary = text_summarization(
            summarizer, ''.join(paragraph_summaries))
        summarized_book["chapters"][ch_num]["paragraph_summaries"] = paragraph_summaries
        summarized_book["chapters"][ch_num]["chapter_summary"] = chapter_summary
        chapter_summaries.append(chapter_summary)

    book_summary = text_summarization(summarizer, ''.join(chapter_summaries))
    book["book_summary"] = book_summary
    with open(Path(output_dir, input_file.stem + '_summarized.json'), 'w', encoding='utf-8') as f:
        json.dump({"book": book}, f)
