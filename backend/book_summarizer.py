#! /usr/bin/env python3
"""Summarize chapters and paragraphs of a book."""
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer
from transformers import pipeline

import util


#  Text-to-image model does not support more than 77 tokens (keras_cv.models.StableDiffusion)
def text_summarization(summarizer, text, min_length=5, max_length=77):
    """Summarize a given text to a provided length.

    Args:
        summarizer (Model): the summarization model in use
        text (string): the text to be summarized
        min_length (int, optional): the minimal length of the summarization. Defaults to 5.
        max_length (int, optional): the maximal length of the summarization. Defaults to 77.

    Returns:
        string: the summarized version of the text
    """
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
    text_len = len(tokens)
    summary = summarizer(text, min_length=min(min_length, text_len),
                         max_length=min(text_len, max_length), truncation=True)
    return summary[0]['summary_text']


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
        book_content = util.parse_json(input_file)
    elif input_file.suffix == ".epub":
        book_content = util.parse_epub(input_file)

    book = book_content["book"]
    summarized_book = book
    MODEL_ID = "sshleifer/distilbart-cnn-12-6"
    summarization_model = pipeline("summarization", model=MODEL_ID)
    chapter_summaries = []
    for ch_num, chapter in enumerate(book["chapters"]):
        paragraph_summaries = [text_summarization(
            summarization_model, paragraph) for paragraph in chapter["paragraphs"]]
        chapter_summary = text_summarization(
            summarization_model, ''.join(paragraph_summaries))
        summarized_book["chapters"][ch_num]["paragraph_summaries"] = paragraph_summaries
        summarized_book["chapters"][ch_num]["chapter_summary"] = chapter_summary
        chapter_summaries.append(chapter_summary)

    book_summary = text_summarization(
        summarization_model, ''.join(chapter_summaries))
    book["book_summary"] = book_summary
    with open(Path(output_dir, 'summarized.json'), 'w', encoding='utf-8') as f:
        json.dump({"book": book}, f)
