"""Module for book summarization functionality."""
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer, pipeline
from tqdm import tqdm
import util

MODEL_ID = "sshleifer/distilbart-cnn-12-6"


class BookSummarizer:
    """
    Summarizes a book given its input file and saves the 
    summarized content to the specified output directory.
    """

    def __init__(self):
        self.summarized_paragraphs_count = 0
        self.total_paragraphs = 0

    def text_summarization(self, summarizer, text, min_length=5, max_length=77):
        """
        Summarize a given text to a provided length.

        Args:
            summarizer (Model): the summarization model in use
            text (string): the text to be summarized
            min_length (int, optional): the minimal length of the summarization. Defaults to 5.
            max_length (int, optional): the maximal length of the summarization. Defaults to 77.

        Returns:
            string: the summarized version of the text
        """
        tokenizer = AutoTokenizer.from_pretrained(
            "sshleifer/distilbart-cnn-12-6")
        tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
        text_len = len(tokens)
        summary = summarizer(text, min_length=min(min_length, text_len),
                             max_length=min(text_len, max_length), truncation=True)
        self.summarized_paragraphs_count += 1
        return summary[0]['summary_text']

    def get_summarization_progress(self):
        """
        Get the summarization progress.
        """
        if self.total_paragraphs == 0:
            return 0
        progress_percentage = (
            self.summarized_paragraphs_count / self.total_paragraphs) * 100
        return progress_percentage

    async def summarize_book(self, input_file, output_dir):
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
        if output_dir is None:
            output_dir = Path(input_file).parent
        else:
            output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        input_file = Path(input_file)
        if input_file.suffix == ".json":
            book_content = util.parse_json(input_file)
        elif input_file.suffix == ".epub":
            book_content = util.parse_epub(input_file)

        book = book_content["book"]
        summarized_book = book
        summarization_model = pipeline("summarization", model=MODEL_ID)
        chapter_summaries = []

        for ch_num, chapter in enumerate(tqdm(book["chapters"], desc="Summarizing chapters")):
            self.total_paragraphs += len(chapter["paragraphs"])
            paragraph_summaries = []

            for paragraph in tqdm(chapter["paragraphs"], desc="Summarizing paragraphs"):
                paragraph_summaries.append(
                    self.text_summarization(summarization_model, paragraph))
            chapter_summary = self.text_summarization(
                summarization_model, ''.join(paragraph_summaries))
            summarized_book["chapters"][ch_num]["paragraph_summaries"] = paragraph_summaries
            summarized_book["chapters"][ch_num]["chapter_summary"] = chapter_summary
            chapter_summaries.append(chapter_summary)

        book_summary = self.text_summarization(
            summarization_model, ''.join(chapter_summaries))
        book["book_summary"] = book_summary
        with open(Path(output_dir, 'summarized.json'), 'w', encoding='utf-8') as f:
            json.dump({"book": book}, f)
        self.total_paragraphs = 0
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Summarize book, chapters and paragraphs')
    parser.add_argument('--input_file', type=str, help='input json/epub file')
    parser.add_argument('--output_dir', type=str,
                        help='output dir. Same as input if unspecified', default=None)
    args = parser.parse_args()

    Booksummarizer = BookSummarizer()
    Booksummarizer.summarize_book(args.input_file, args.output_dir)
