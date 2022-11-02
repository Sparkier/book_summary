# Book Summary

In this repository, we generate both textual summaries and image descriptions for written texts.

## Backend

In the backend folder, we generate the text summaries and images.
First generate text summaries based on json/epub content:
`python backend/book_summarizer.py --input_file "data/alice.json"`
Then generate image representations of the text. 
`python backend/generator.py --input_file "data/alice_summarized.json" --output_dir "results"`

Images are generated using a stable diffusion text to image model.

## Frontend

For now, the frontend only displays different levels of text summaries.

Images are only placeholders as of now.
