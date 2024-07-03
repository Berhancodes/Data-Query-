# Data-Query-


This project uses a language model to read data from a CSV and a PDF file and respond to user queries. The project is designed to be general so anyone can adapt it to their own data files.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file based on the provided `.env.example`:
    ```bash
    cp .env.example .env
    ```
   Modify the `.env` file to specify your own CSV and PDF files if needed.
5. Place your data files in the `data` directory.
6. **Important**: You need an OpenAI ChatGPT account and an API key. Set the `OPENAI_API_KEY` in your `.env` file with your OpenAI API key.

## Usage

Run the `main.py` file:
```bash
python main.py

