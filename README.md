# NewsScraper Project

This project orchestrates a pipeline to extract stock ticker symbols from PDF documents, fetch relevant financial news for those tickers, and then evaluate the PDF documents based on predefined prompts using Google Gemini, generating a consolidated summary report.

## Project Workflow

The `main.py` script orchestrates the following steps:

1.  **Extract Ticker Symbols**: `sym_extract.py` processes PDF files in the `files/` directory to identify and extract company stock ticker symbols using Google Gemini's Generative AI.
2.  **Gather News**: `scraper.py` takes the extracted ticker symbols and fetches relevant financial news from various sources, summarizing the articles. The news summary is saved to `files/NewsSummary_MMDDYYYY.txt`.
3.  **Evaluate Prompts and Generate Report**: `prompt_evaluator.py` uploads all files in the `files/` directory to Gemini, evaluates them against prompts defined in `prompts.txt`, and generates a PDF report (`PromptSummary_MMDDYYYY.pdf`) in the `files/` directory.

## Setup and Running the Project

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/jaxdaddy/NewsScraper.git
    cd NewsScraper
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Gemini API Key**:
    *   Obtain your Google Gemini API key from [Google AI Studio](https://ai.google.dev/).
    *   Open the `.env` file in the project root.
    *   Replace `your_api_key_here` with your actual Gemini API key:
        ```
        GEMINI_API_KEY=your_api_key_here
        ```

4.  **Place PDF Files**:
    *   Place your PDF documents (e.g., financial reports, filings) into the `files/` directory.

5.  **Define Prompts**:
    *   Open the `prompts.txt` file in the project root.
    *   Add the prompts you want Gemini to evaluate, one prompt per line.

6.  **Run the Main Script**:
    ```bash
    python3 main.py
    ```

## Generated Reports

*   **News Summary**: `files/NewsSummary_MMDDYYYY.txt` - Contains summarized financial news for the extracted tickers.
*   **Prompt Evaluation Report**: `files/PromptSummary_MMDDYYYY.pdf` - Contains the evaluation of your PDF files by Gemini based on the prompts in `prompts.txt`.

## Project Structure

```
.
├── main.py                 # Orchestrates the workflow
├── sym_extract.py          # Extracts ticker symbols from PDFs
├── scraper.py              # Fetches and summarizes financial news
├── prompt_evaluator.py     # Evaluates files with Gemini and generates PDF report
├── requirements.txt        # Python dependencies
├── .env                    # Stores Gemini API key (ignored by Git)
├── .gitignore              # Specifies files/ and .env to be ignored
├── files/                  # Directory for PDF input and generated reports
│   ├── your_document.pdf
│   ├── another_document.pdf
│   ├── NewsSummary_MMDDYYYY.txt
│   └── PromptSummary_MMDDYYYY.pdf
└── prompts.txt             # Prompts for Gemini evaluation
```