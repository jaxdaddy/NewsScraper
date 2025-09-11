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

def run_ticker_extraction():
    pdf_dir = "files/"
    all_extracted_tickers = set()
    file_results = {}

    if not os.path.exists(pdf_dir):
        print(f"Error: Directory '{pdf_dir}' not found. Please create it and place PDF files inside.")
        return []

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in '{pdf_dir}'. Please place PDF files inside.")
        return []

    print(f"Processing {len(pdf_files)} PDF files in '{pdf_dir}'...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"Extracting text from {pdf_file}...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            print(f"Text extracted from {pdf_file} (first 200 chars): {text[:200]}...")
            print(f"Sending text from {pdf_file} to Gemini for ticker extraction...")
            tickers = extract_tickers_from_text(text)
            if tickers:
                print(f"Found tickers in {pdf_file}: {', '.join(tickers)}")
                all_extracted_tickers.update(tickers)
                file_results[pdf_file] = sorted(list(tickers))
            else:
                print(f"No tickers found in {pdf_file}.")
                file_results[pdf_file] = []
        else:
            print(f"No text extracted from {pdf_file}.")
            file_results[pdf_file] = []

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
    extracted_tickers = run_ticker_extraction()
    # The printing is already handled within run_ticker_extraction for standalone execution
