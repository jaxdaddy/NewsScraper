import os
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it.")
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file."""
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()
        document.close()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def get_gemini_response(prompt):
    """Sends a prompt to Google Gemini and returns the response."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return None

def extract_tickers_from_text(text):
    """
    Prompts Gemini to identify and return valid stock ticker symbols from the given text.
    Returns a list of unique ticker symbols.
    """
    if not text.strip():
        return []

    # Craft a precise prompt for Gemini
    prompt = (
        "From the following text, identify and return ONLY valid stock ticker symbols. "
        "Return them as a comma-separated list, with no other text, explanations, or formatting. "
        "If no valid ticker symbols are found, return an empty string.\n\n" +
        "Text: " + text
    )
    
    gemini_response = get_gemini_response(prompt)
    
    if gemini_response:
        # Clean and deduplicate the tickers
        tickers = [
            ticker.strip().upper() 
            for ticker in gemini_response.split(',') 
            if ticker.strip() # Filter out empty strings
        ]
        return sorted(list(set(tickers))) # Deduplicate and sort
    return []

def run_ticker_extraction(pdf_files_to_process):
    all_extracted_tickers = set()
    file_results = {}

    if not pdf_files_to_process:
        print("No PDF files provided for ticker extraction. Exiting.")
        return []

    print(f"Processing {len(pdf_files_to_process)} PDF files for ticker extraction...")

    for pdf_path in pdf_files_to_process:
        print(f"Extracting text from {os.path.basename(pdf_path)}...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            print(f"Text extracted from {os.path.basename(pdf_path)} (first 200 chars): {text[:200]}...")
            print(f"Sending text from {os.path.basename(pdf_path)} to Gemini for ticker extraction...")
            tickers = extract_tickers_from_text(text)
            if tickers:
                print(f"Found tickers in {os.path.basename(pdf_path)}: {', '.join(tickers)}")
                all_extracted_tickers.update(tickers)
                file_results[os.path.basename(pdf_path)] = sorted(list(tickers))
            else:
                print(f"No tickers found in {os.path.basename(pdf_path)}.")
                file_results[os.path.basename(pdf_path)] = []
        else:
            print(f"No text extracted from {os.path.basename(pdf_path)}.")
            file_results[os.path.basename(pdf_path)] = []

    print("\n--- Summary of Tickers per File ---")
    for filename, tickers in file_results.items():
        if tickers:
            print(f"  {filename}: {', '.join(tickers)}")
        else:
            print(f"  {filename}: No tickers found.")

    final_tickers_list = sorted(list(all_extracted_tickers))
    print("\n--- All Extracted Ticker Symbols (Deduplicated) ---")
    print(final_tickers_list)
    print("--------------------------------------------------")
    return final_tickers_list

if __name__ == "__main__":
    # For standalone testing, provide dummy files
    dummy_files = [os.path.join("files", f) for f in os.listdir("files/") if f.lower().endswith('.pdf') and f.startswith('COR_')][:3]
    if not dummy_files:
        print("No dummy PDF files found in 'files/' for standalone testing. Please place some COR_*.pdf files.")
    else:
        extracted_tickers = run_ticker_extraction(dummy_files)
        # The printing is already handled within run_ticker_extraction for standalone execution
