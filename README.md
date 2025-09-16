# NewsScraper Project

This project orchestrates a pipeline to extract stock ticker symbols from PDF documents, fetch relevant financial news for those tickers, and then evaluate the PDF documents based on predefined prompts using Google Gemini, generating a consolidated summary report.

## Project Workflow

The `main.py` script orchestrates the following steps:

1.  **File Cleanup**: Automatically removes any old `NewsSummary_*.txt` files from the `files/` directory at the start of the workflow.
2.  **User File Type Selection**: Prompts the user to select a file type (e.g., COR, COY, POR, POY) to process.
3.  **Extract Ticker Symbols**: `sym_extract.py` identifies and extracts company stock ticker symbols from the three most recent PDF files of the selected type in the `files/` directory, using Google Gemini's Generative AI.
4.  **Gather News**: `scraper.py` takes the extracted ticker symbols and fetches relevant financial news from various sources, summarizing the articles. The newly generated news summary (`NewsSummary_MMDDYYYY.txt`) is saved to the `files/` directory.
5.  **Evaluate Prompts and Generate Report**: `prompt_evaluator.py` uploads the selected type-specific PDF files, the newly generated `NewsSummary` file, and `options_primer.pdf` to Gemini. It then evaluates them against prompts defined in a type-specific prompt file (e.g., `COR_prompts.txt`), and generates a PDF report (`PromptSummary_TYPE_YYYYMMDD.pdf`) in the `output/` directory.

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
    *   Place your PDF documents (e.g., `COR_Movers_YYYY-MM-DD.pdf`, `COY_Annual_YYYY-MM-DD.pdf`) into the `files/` directory. Ensure filenames follow the `TYPE_Description_YYYY-MM-DD.pdf` format.
    *   Ensure `options_primer.pdf` is also present in the `files/` directory.

5.  **Define Prompts**: 
    *   Create separate prompt files for each file type you intend to process (e.g., `COR_prompts.txt`, `COY_prompts.txt`, `POR_prompts.txt`, `POY_prompts.txt`).
    *   Adapt the prompts in each file to be contextually appropriate for the specific data type.

6.  **Run the Main Script**:
    ```bash
    python3 main.py
    ```
    *The script will prompt you to select a file type.* 

## Generated Reports

*   **News Summary**: `files/NewsSummary_MMDDYYYY.txt` - Contains summarized financial news for the extracted tickers.
*   **Prompt Evaluation Report**: `output/PromptSummary_TYPE_MMDDYYYY.pdf` - Contains the evaluation of your PDF files by Gemini based on the type-specific prompts.

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
│   ├── COR_Movers_YYYY-MM-DD.pdf # Example input PDF
│   ├── COY_Annual_YYYY-MM-DD.pdf # Example input PDF
│   ├── options_primer.pdf  # Always included in prompt evaluation
│   ├── NewsSummary_MMDDYYYY.txt # Generated news summary
│   └── ...
├── output/                 # Directory for final PromptSummary reports
│   └── PromptSummary_TYPE_MMDDYYYY.pdf # Generated prompt evaluation report
├── COR_prompts.txt         # Prompts for Corporate Movers Reports
├── COY_prompts.txt         # Prompts for Company Yearly Reports
├── POR_prompts.txt         # Prompts for Portfolio Reports
└── POY_prompts.txt         # Prompts for Portfolio Yearly Reports
```