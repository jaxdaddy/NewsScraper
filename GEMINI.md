# NewsScraper Project - Gemini Context

This document provides a comprehensive overview of the NewsScraper project, designed to serve as instructional context for future interactions with the Gemini AI agent.

## Project Overview

The NewsScraper project is a Python-based pipeline that automates the extraction of stock ticker symbols from PDF documents, fetches relevant financial news for those tickers, and then evaluates the PDF documents based on predefined prompts using Google Gemini's Generative AI, generating a consolidated summary report.

**Key Features:**

*   **Ticker Extraction**: Identifies and extracts stock ticker symbols from PDF financial documents.
*   **News Scraping**: Gathers and summarizes financial news articles related to the extracted tickers.
*   **Prompt Evaluation**: Utilizes Google Gemini to analyze PDF content against specific prompts and generates a detailed PDF report of the evaluations.
*   **Orchestrated Workflow**: A master script (`main.py`) coordinates the entire pipeline.

**Main Technologies:**

*   **Python 3.x**: The primary programming language.
*   **PyMuPDF (fitz)**: For efficient PDF parsing and text extraction.
*   **google-generativeai**: For interacting with the Google Gemini API.
*   **python-dotenv**: For secure management of API keys via `.env` files.
*   **reportlab**: For generating PDF reports.
*   **newspaper3k**: For news article extraction and summarization.
*   **nltk**: For natural language processing tasks.

## Project Architecture and Workflow

The project follows a modular architecture, with `main.py` acting as the central orchestrator:

1.  **`main.py` (Master Controller)**:
    *   Serves as the entry point for the entire pipeline.
    *   Calls `sym_extract.py` to get a list of ticker symbols.
    *   Passes the ticker list to `scraper.py` to fetch and summarize news.
    *   Calls `prompt_evaluator.py` to perform Gemini-based evaluations and generate a PDF report.
    *   Includes robust error handling and logging for each step.

2.  **`sym_extract.py` (Ticker Extraction Module)**:
    *   **Purpose**: Extracts stock ticker symbols from PDF files located in the `files/` directory.
    *   **Process**: Reads PDF content, sends it to Google Gemini with a specific prompt to identify tickers, and returns a deduplicated list of symbols.
    *   **Key Function**: `run_ticker_extraction()`

3.  **`scraper.py` (News Scraping Module)**:
    *   **Purpose**: Fetches and summarizes financial news articles for a given list of company stock symbols.
    *   **Process**: Uses the `newspaper3k` library to scrape news from predefined sources and NLTK for summarization. Saves the news summary to `files/NewsSummary_MMDDYYYY.txt`.
    *   **Key Function**: `run_news_scraping(companies_list)`

4.  **`prompt_evaluator.py` (Prompt Evaluation Module)**:
    *   **Purpose**: Evaluates the content of files in the `files/` directory against prompts defined in `prompts.txt` using Google Gemini, and generates a PDF report.
    *   **Process**: Reads prompts, extracts text from files (including PDFs), sends content and prompts to Gemini, and compiles responses into `files/PromptSummary_MMDDYYYY.pdf`.
    *   **Key Function**: `run_prompt_evaluation()`

## Building and Running the Project

To set up and run the project, follow these steps:

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
    *   Place your PDF documents (e.g., financial reports, filings) into the `files/` directory. These will be used for ticker extraction and prompt evaluation.

5.  **Define Prompts**:
    *   Open the `prompts.txt` file in the project root.
    *   Add the prompts you want Gemini to evaluate, one prompt per line. The current `prompts.txt` contains detailed prompts for market movers, news impact, risk signals, momentum/sentiment, and investment watchlists.

6.  **Run the Main Script**:
    ```bash
    python3 main.py
    ```

## Development Conventions

*   **Python Version**: Python 3.x is required.
*   **Dependency Management**: Project dependencies are managed via `requirements.txt`.
*   **API Key Management**: Sensitive API keys are stored in a `.env` file and loaded using `python-dotenv`, ensuring they are not hardcoded or committed to version control (the `.env` file is listed in `.gitignore`).
*   **Modularity**: The project is structured into distinct modules (`sym_extract.py`, `scraper.py`, `prompt_evaluator.py`) with `main.py` serving as the orchestrator, promoting code reusability and maintainability.
*   **Error Handling and Logging**: Each step in the `main.py` pipeline includes explicit error handling and progress logging for better visibility and debugging.
*   **Output Management**: Generated reports (`NewsSummary_MMDDYYYY.txt`, `PromptSummary_MMDDYYYY.pdf`) are saved within the `files/` directory.

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
│   ├── your_document.pdf   # Example input PDF
│   ├── NewsSummary_MMDDYYYY.txt # Generated news summary
│   └── PromptSummary_MMDDYYYY.pdf # Generated prompt evaluation report
└── prompts.txt             # Prompts for Gemini evaluation
```