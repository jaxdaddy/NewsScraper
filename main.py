import os
from sym_extract import run_ticker_extraction
from scraper import run_news_scraping
from prompt_evaluator import run_prompt_evaluation
from datetime import datetime

def parse_date_from_filename(filename):
    """Parses date from filename in YYYY-MM-DD format (e.g., TYPE_Movers_YYYY-MM-DD.pdf)."""
    try:
        # Example: COR_Movers_2025-09-03.pdf
        # Split by '_' to get ['COR', 'Movers', '2025-09-03.pdf']
        parts = filename.split('_')
        if len(parts) >= 3: # Ensure there are enough parts
            date_part_with_ext = parts[-1] # '2025-09-03.pdf'
            date_part = date_part_with_ext.split('.')[0] # '2025-09-03'
            
            # Split by '-' to get year, month, day
            date_components = date_part.split('-')
            if len(date_components) == 3:
                year = int(date_components[0])
                month = int(date_components[1])
                day = int(date_components[2])
                return datetime(year, month, day)
    except (ValueError, IndexError):
        pass
    return None

def main():
    print("--- Starting Master Controller (main.py) ---")

    # Phase 1: File Cleanup - Remove old NewsSummary files
    pdf_dir = "files/"
    if os.path.exists(pdf_dir):
        for f in os.listdir(pdf_dir):
            if f.startswith("NewsSummary_"):
                try:
                    os.remove(os.path.join(pdf_dir, f))
                    print(f"Removed old NewsSummary file: {f}")
                except Exception as e:
                    print(f"Error removing old NewsSummary file {f}: {e}")

    # Step 0: User selects file type
    valid_types = ["COR", "COY", "POR", "POY"]
    file_type = "COR" # Default for automated testing
    # while file_type not in valid_types:
    #     file_type = input(f"Enter the file type to process ({ ', '.join(valid_types)}): ").upper()
    #     if file_type not in valid_types:
    #         print("Invalid file type. Please try again.")

    pdf_dir = "files/"
    if not os.path.exists(pdf_dir):
        print(f"Error: Directory '{pdf_dir}' not found. Please create it and place PDF files inside.")
        return

    # Identify the three most recent files of the selected type
    all_files = []
    for f in os.listdir(pdf_dir):
        if f.startswith(f"{file_type}_") and f.lower().endswith('.pdf'):
            file_date = parse_date_from_filename(f)
            if file_date:
                all_files.append((file_date, f))
    
    all_files.sort(key=lambda x: x[0], reverse=True)
    selected_pdf_files = [os.path.join(pdf_dir, f[1]) for f in all_files[:3]]

    if not selected_pdf_files:
        print(f"No recent PDF files found for type '{file_type}'. Exiting.")
        return

    print(f"Processing the following {len(selected_pdf_files)} files for type '{file_type}':")
    for f in selected_pdf_files:
        print(f"- {os.path.basename(f)}")

    # Step 1: Extract ticker symbols from PDFs
    print("\n--- Step 1: Extracting ticker symbols from PDF files ---")
    try:
        extracted_tickers = run_ticker_extraction(selected_pdf_files) # Pass selected files
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
    news_summary_path = None # Initialize to None
    try:
        # NewsScraper.py expects a list of company symbols
        news_summary_content, output_filename = run_news_scraping(extracted_tickers)
        
        if news_summary_content:
            # Save the news summary to a file
            with open(output_filename, "w", encoding='utf-8') as f:
                f.write("\n".join(news_summary_content))
            print(f"News scraping complete. Summary saved to {output_filename}")
            news_summary_path = output_filename # Store the path
        else:
            print("News scraping completed, but no news content was generated.")
            print("Error: NewsSummary file was not generated. Halting workflow.")
            return # Halt workflow if no news content

    except Exception as e:
        print(f"Error during news scraping: {e}")
        return

    # Step 3: Run prompt evaluation and generate report
    print("\n--- Step 3: Running prompt evaluation and generating report ---")
    try:
        run_prompt_evaluation(file_type, selected_pdf_files, news_summary_path) # Pass news_summary_path
        print("Prompt evaluation and report generation complete.")
    except Exception as e:
        print(f"Error during prompt evaluation: {e}")
        return

    print("\n--- Master Controller (main.py) Finished ---")

if __name__ == "__main__":
    main()

