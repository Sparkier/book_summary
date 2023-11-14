# Book Summary

## Intro

In this repository, we generate both textual summaries and image descriptions for written texts.

### Backend

In the backend folder, we generate the text summaries and images.
First generate text summaries based on json/epub content:
`python backend/book_summarizer.py --input_file "data/alice.json"`
Then generate image representations of the text. 
`python backend/generator.py --input_file "data/alice_summarized.json" --output_dir "results"`

Images are generated using a stable diffusion text to image model.

### Frontend

For now, the frontend only displays different levels of text summaries.

Images are only placeholders as of now.


## Getting started

Install Python and Node.js on your computer.<br>
Clone the Project from GitHub and open the book_summary folder.

As an example Visual Studio Code is used here. Check that you have the Python extension installed.


### General setup 
The general setup is only necessary the first time. 

#### Environment (Recommended, but optional)
 1. Install conda as Python environment (e.g. miniconda). 
 2. Press STRG + SHIFT + P and search for Python: Create Environment > Conda.

(Here you can find more information regarding environments `https://code.visualstudio.com/docs/python/environments`)

#### Interpreter
To select an interpreter, press STRG + SHIFT + P and search for Python: Select Interpreter. 

### How to setup Backend

 1. Open the terminal in VS Code and start a new command prompt. 
 2. Change the directory to the backend folder, (open requirements.txt and remove dependecies with version number to avoid version errors + save) and install the requirements with the following command: `pip install -r requirements.txt` <br>
 Then start the backend server using the command `python server.py`.

### How to setup Frontend

1. After the backend server is up and running, open a new command prompt go into the frontend folder and install npm: `npm i`
2. After that start the frontend using `npm run dev`. 

Now the application should be running at `http://localhost:5173/`.
