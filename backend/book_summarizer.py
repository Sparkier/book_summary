"""Module for book summarization functionality."""

import asyncio
from typing import Callable
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer, pipeline
import torch.cuda

from semantic_text_splitter import TextSplitter

import util


class BookSummarizer:
    """
    Summarizes a book given its input file and saves the
    summarized content to the specified output directory.
    """

    def __init__(self, model_id="pszemraj/led-large-book-summary"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.summarizer = pipeline("summarization", model=model_id, device=0 if torch.cuda.is_available() else -1)
        self.model_id = model_id

    def semantic_text_split(self, text, max_tokens):
        """Split text into chunks accoding to https://github.com/benbrandt/text-splitter. (v0.12.3)

        Args:
            text (string): the text to be chunked
            max_tokens (int): maximal length of a chunk

        Returns:
            list: chunks (strings) of text
        """
        splitter = TextSplitter.from_huggingface_tokenizer(self.tokenizer, max_tokens)
        chunks = splitter.chunks(text)
        return chunks

    def text_summarization(self, text, min_length=32, max_length=77):
        """
        Summarize a given text to a provided length.

        Args:
            text (string): the text to be summarized
            min_length (int, optional): the minimal length of the summarization. Defaults to 5.
            max_length (int, optional): the maximal length of the summarization. Defaults to 77.

        Returns:
            string: the summarized version of the text
        """
        tokens = self.tokenizer.tokenize(text)

        num_tokens = len(tokens)
        summary = self.summarizer(
            text,
            min_length=min(min_length, num_tokens),
            max_length=min(num_tokens, max_length),
            # truncation=True,
            no_repeat_ngram_size=3,
            encoder_no_repeat_ngram_size=3,
            repetition_penalty=3.5,
            num_beams=4,
            early_stopping=True,
        )
        return summary[0]["summary_text"]
    
    def clean_text(self, text):
        characters_to_replace = [" \n", "*", "\xa0", "\u2009", '""']

    async def summarize_book(
        self,
        input_file: Path,
        output_dir: Path,
        progress_callback: Callable[[int, int], None] = None,
    ):
        """
        Summarizes a book given its input file and saves the
        summarized content to the specified output directory.

        Args:
            input_file (str): The path to the input JSON or EPUB file
              containing the book content.
            output_dir (str): The path to the output directory where
            the summarized content will be saved. If unspecified,
            the output directory will be the same as the input file's parent directory.
            progress_callback (Callable[[int, int], None]): Called with number of processed 
            items and total items as arguments if not None.

        Returns:
            bool: True if the book is successfully summarized and saved
        """
        # pylint: disable=too-many-locals
        output_dir.mkdir(parents=True, exist_ok=True)


        book_content = util.parse_book(input_file)

        book: dict = book_content["book"]
        summarized_book = book
        chapter_summaries = []

        num_paragraphs_per_chapter = [
            len(chapter["paragraphs"]) for chapter in book["chapters"]
        ]
        num_paragraphs = sum(num_paragraphs_per_chapter)
        num_chapters = len(book["chapters"])
        num_book = 1
        total_to_process = num_book + num_chapters + num_paragraphs

        num_processed = 0

        def increment_progress(inc: int):
            nonlocal num_processed
            num_processed += inc
            if progress_callback:
                progress_callback(num_processed, total_to_process)

        # Initiate 0% progress
        increment_progress(0)

        for ch_num, chapter in enumerate(book["chapters"]):
            translation_table = dict.fromkeys(map(ord, '\n*\xa0\u2009""'), None)
            # Clean paragraphs
            clean_paragraphs = [paragraph.translate(translation_table) for paragraph in chapter["paragraphs"]]

            chapter_text: str = "\n".join(clean_paragraphs)
            chapter_chunks: list = self.semantic_text_split(chapter_text, self.summarizer.tokenizer.model_max_length)
            chapter_chunk_summaries: list = [
                self.text_summarization(chunk) for chunk in chapter_chunks
            ]
            summarized_book["chapters"][ch_num][
                "paragraph_summaries"
            ] = chapter_chunk_summaries

            chapter_summary: str = "\n".join(chapter_chunk_summaries)
            increment_progress(1)

            summarized_book["chapters"][ch_num]["chapter_summary"] = chapter_summary
            chapter_summaries.append(chapter_summary)

        chapter_summary_chunks: list = self.semantic_text_split(
        "".join(chapter_summaries), self.summarizer.tokenizer.model_max_length)
        chapter_chunk_summaries: list = [
            self.text_summarization(chunk)
            for chunk in chapter_summary_chunks
        ]
        book_summary = self.text_summarization("\n".join(chapter_chunk_summaries))
        increment_progress(1)

        book["book_summary"] = book_summary
        output_name = (
            input_file.stem + "_summ_(" + self.model_id.replace("_", "-").replace("/", "_") + ").json"
        )
        with open(Path(output_dir, output_name), "w", encoding="utf-8") as f:
            json.dump({"book": book}, f)

        return True


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
    with tqdm(desc="Summarizing book") as pbar:

        def print_progress(progress, total):
            """Log progress bar"""
            if progress == 0:
                pbar.reset(total)
            else:
                pbar.update(1)

        out_dir = (
            Path(args.output_dir) if args.output_dir else Path(args.input_file).parent
        )

        Booksummarizer = BookSummarizer()
        asyncio.run(
            Booksummarizer.summarize_book(
                Path(args.input_file), out_dir, print_progress
            )
        )
