#! /usr/bin/env python3
"""Summarize chapters and paragraphs of a book."""
import argparse
import json
from pathlib import Path
from transformers import pipeline
from tokenizers import Tokenizer
import torch.cuda

from semantic_text_splitter import TextSplitter

import util


# MODEL_ID = "facebook/bart-large-cnn"
MODEL_ID = "pszemraj/led-large-book-summary"


def split_text(text, max_tokens):
    """Split text into chunks accoding to https://github.com/benbrandt/text-splitter. (v0.12.3)

    Args:
        text (string): the text to be chunked
        max_tokens (int): maximal length of a chunk

    Returns:
        list: chunks (strings) of text
    """
    tokenizer = Tokenizer.from_pretrained(MODEL_ID)
    splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens)
    chunks = splitter.chunks(text)
    return chunks


def text_summarization(summarizer, text, min_length=32, max_length=512):
    """Summarize a given text to a provided length.

    Args:
        summarizer (Model): the summarization model in use
        text (string): the text to be summarized
        min_length (int, optional): the minimal length of the summarization. Defaults to 5.
        max_length (int, optional): the maximal length of the summarization. Defaults to 77.

    Returns:
        string: the summarized version of the text
    """
    tokenizer = summarizer.tokenizer
    tokens = tokenizer.tokenize(text)
    number_tokens = len(tokens)
    summary = summarizer(
        text,
        min_length=min(min_length, number_tokens),
        max_length=min(number_tokens, max_length),
        # truncation=True,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=3,
        repetition_penalty=3.5,
        num_beams=4,
        early_stopping=True,
    )

    return summary[0]["summary_text"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarize book, chapters and paragraphs"
    )
    parser.add_argument("--input_file", type=str, help="input json/epub file")
    parser.add_argument(
        "--output_dir",
        type=str,
        help="output dir. Same as input if unspecified",
        default=None,
    )
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

    book: dict = book_content["book"]

    summarization_model = pipeline(
        "summarization",
        model=MODEL_ID,
        device=0 if torch.cuda.is_available() else -1,
    )

    model_max_length = summarization_model.tokenizer.model_max_length
    print(f"Model max length: {model_max_length}")

    print(summarization_model.tokenizer)

    chapter_summaries: list = []

    for ch_num, chapter in enumerate(book["chapters"]):

        print(f"Summarizing Chapter {ch_num}")

        # Clean paragraphs
        characters_to_replace = [" \n", "*", "\xa0", "\u2009", '""']
        paragraphs_clean: list = [s.replace("\n", " ") for s in chapter["paragraphs"]]
        for i, s in enumerate(paragraphs_clean):
            for char in characters_to_replace:
                paragraphs_clean[i] = paragraphs_clean[i].replace(char, " ")

        print(f"Chapter {ch_num}: ")

        chapter_text: str = "\n".join(paragraphs_clean)
        chapter_chunks: list = split_text(chapter_text, model_max_length)
        chunk_summaries: list = [
            text_summarization(summarization_model, chunk) for chunk in chapter_chunks
        ]

        print(f"Chapter text: {chapter_text}")
        print(f"Chunk summaries: {chunk_summaries}")

        chapter_summary_text: str = "\n".join(chunk_summaries)
        book["chapters"][ch_num]["chapter_summary"] = chapter_summary_text
        chapter_summaries.append(chapter_summary_text)

    chapter_summaries_text = "".join(chapter_summaries)
    chapter_summary_chunks: list = split_text(
        "".join(chapter_summaries_text), model_max_length
    )
    chapter_chunk_summaries: list = [
        text_summarization(summarization_model, chunk)
        for chunk in chapter_summary_chunks
    ]
    book_summary_text: str = "\n".join(chapter_chunk_summaries)
    book["book_summary"] = book_summary_text

    print(f"Book summary: {book_summary_text}")

    output_name = (
        input_file.stem + "_summ_(" + MODEL_ID.replace("_", "-").replace("/", "_") + ")"
    )
    with open(Path(output_dir, output_name + ".json"), "w", encoding="utf-8") as f:
        json.dump({"book": book}, f)
