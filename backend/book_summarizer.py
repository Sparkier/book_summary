"""Module for book summarization functionality."""

import asyncio
from typing import Callable
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer, pipeline
from tqdm import tqdm
import util


class BookSummarizer:
    """
    Summarizes a book given its input file and saves the
    summarized content to the specified output directory.
    """

    def __init__(self, model_id="sshleifer/distilbart-cnn-12-6"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.summarizer = pipeline("summarization", model=model_id)

    def text_summarization(self, text, min_length=5, max_length=77):
        """
        Summarize a given text to a provided length.

        Args:
            text (string): the text to be summarized
            min_length (int, optional): the minimal length of the summarization. Defaults to 5.
            max_length (int, optional): the maximal length of the summarization. Defaults to 77.

        Returns:
            string: the summarized version of the text
        """
        tokens = self.tokenizer.tokenize(
            self.tokenizer.decode(self.tokenizer.encode(text))
        )
        text_len = len(tokens)
        summary = self.summarizer(
            text,
            min_length=min(min_length, text_len),
            max_length=min(text_len, max_length),
            truncation=True,
        )
        return summary[0]["summary_text"]

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

        Returns:
            bool: True if the book is successfully summarized and saved
        """
        # pylint: disable=too-many-locals
        output_dir.mkdir(parents=True, exist_ok=True)

        input_file = Path(input_file)
        if input_file.suffix == ".json":
            book_content = util.parse_json(input_file)
        elif input_file.suffix == ".epub":
            book_content = util.parse_epub(input_file)

        book = book_content["book"]
        summarized_book = book
        chapter_summaries = []
        num_processed = 0

        num_paragraphs_per_chapter = [
            len(chapter["paragraphs"]) for chapter in book["chapters"]
        ]
        num_paragraphs = sum(num_paragraphs_per_chapter)
        num_chapters = len(book["chapters"])
        num_book = 1
        total_to_process = num_book + num_chapters + num_paragraphs
        if progress_callback:
            progress_callback(0, total_to_process)
        for ch_num, chapter in enumerate(book["chapters"]):
            paragraph_summaries = []

            for paragraph in chapter["paragraphs"]:
                paragraph_summaries.append(self.text_summarization(paragraph))
                num_processed += 1
                if progress_callback:
                    progress_callback(num_processed, total_to_process)

            chapter_summary = self.text_summarization("".join(paragraph_summaries))
            num_processed += 1
            if progress_callback:
                progress_callback(num_processed, total_to_process)

            summarized_book["chapters"][ch_num][
                "paragraph_summaries"
            ] = paragraph_summaries
            summarized_book["chapters"][ch_num]["chapter_summary"] = chapter_summary
            chapter_summaries.append(chapter_summary)

        book_summary = self.text_summarization("".join(chapter_summaries))
        num_processed += 1
        if progress_callback:
            progress_callback(num_processed, total_to_process)

        book["book_summary"] = book_summary
        with open(Path(output_dir, "summarized.json"), "w", encoding="utf-8") as f:
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
    t = tqdm(desc="Summarizing book")

    def print_progress(progress, total):
        """Log progress bar"""
        if progress == 0:
            t.reset(total)
        t.update(progress)

    Booksummarizer = BookSummarizer()
    asyncio.run(
        Booksummarizer.summarize_book(
            Path(args.input_file), Path(args.output_dir), print_progress
        )
    )
