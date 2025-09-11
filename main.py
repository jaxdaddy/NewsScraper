import os
from sym_extract import run_ticker_extraction
from scraper import run_news_scraping
from prompt_evaluator import run_prompt_evaluation
from datetime import datetime

def main():
    print("--- Starting Master Controller (main.py) ---")

    # Step 1: Extract ticker symbols from PDFs
    print("\n--- Step 1: Extracting ticker symbols from PDF files ---")
    try:
        extracted_tickers = run_ticker_extraction()
        if not extracted_tickers:
            print("No ticker symbols found in PDF files. Exiting.")
            return
        print(f"Ticker extraction complete. Found {len(extracted_tickers)} unique tickers.")
        print(f"Extracted Tickers: {extracted_tickers}")
    except Exception as e:
        print(f"Error during ticker extraction: {e}")
        return

    # Step 2: Pass symbols to NewsScraper.py and fetch news
    print("\n--- Step 2: Fetching financial news for extracted tickers ---")
    try:
        # NewsScraper.py expects a list of company symbols
        news_summary_content, output_filename = run_news_scraping(extracted_tickers)
        
        if news_summary_content:
            # Save the news summary to a file
            with open(output_filename, "w", encoding='utf-8') as f:
                f.write("\n".join(news_summary_content))
            print(f"News scraping complete. Summary saved to {output_filename}")
        else:
            print("News scraping completed, but no news content was generated.")

    except Exception as e:
        print(f"Error during news scraping: {e}")
        return

    # Step 3: Run prompt evaluation and generate report
    print("\n--- Step 3: Running prompt evaluation and generating report ---")
    try:
        run_prompt_evaluation()
        print("Prompt evaluation and report generation complete.")
    except Exception as e:
        print(f"Error during prompt evaluation: {e}")
        return

    print("\n--- Master Controller (main.py) Finished ---")

if __name__ == "__main__":
    main()
