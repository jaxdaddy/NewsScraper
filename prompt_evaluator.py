import os
import fitz  # PyMuPDF
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import markdown # Import the markdown library

def read_prompts(file_type):
    prompts_file = f"{file_type}_prompts.txt"
    prompts = []
    if not os.path.exists(prompts_file):
        print(f"Error: '{prompts_file}' not found. Please create it with prompts for {file_type} files.")
        return prompts
    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]
    return prompts

def get_file_content_for_gemini(file_paths):
    """Reads content of specified files and prepares for Gemini multimodal input."""
    contents = []
    for filepath in file_paths:
        if os.path.isfile(filepath):
            try:
                if filepath.lower().endswith('.pdf'):
                    # For PDFs, extract text
                    document = fitz.open(filepath)
                    text = ""
                    for page_num in range(document.page_count):
                        page = document.load_page(page_num)
                        text += page.get_text()
                    document.close()
                    contents.append({'mime_type': 'text/plain', 'data': text, 'filename': os.path.basename(filepath)})
                else:
                    # For other text files, read directly
                    with open(filepath, 'r', encoding='utf-8') as f:
                        contents.append({'mime_type': 'text/plain', 'data': f.read(), 'filename': os.path.basename(filepath)})
            except Exception as e:
                print(f"Error reading file {os.path.basename(filepath)}: {e}")
    return contents

def evaluate_with_gemini(prompts, file_contents):
    """Sends prompts and file contents to Gemini for evaluation."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest') # Use the same model as sym_extract.py
    evaluations = []
    for prompt_text in prompts:
        try:
            # Prepare parts for multimodal input
            # Add instruction for structured output
            modified_prompt_text = prompt_text + "\n\nPlease provide your response in a clear, concise, and structured format, using Markdown (e.g., bullet points, bolding, numbered lists) where appropriate for readability."
            parts = [modified_prompt_text]
            for content_item in file_contents:
                parts.append(content_item['data'])
            
            response = model.generate_content(parts)
            evaluations.append({'prompt': prompt_text, 'response': response.text})
        except Exception as e:
            print(f"Error evaluating prompt '{prompt_text}' with Gemini: {e}")
            evaluations.append({'prompt': prompt_text, 'response': f"Error: {e}"})
    return evaluations

def generate_pdf_report(evaluations, output_filename):
    """Generates a PDF report from Gemini evaluations."""
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom style for indented paragraphs (for list items)
    styles.add(ParagraphStyle(name='Indented', parent=styles['Normal'],
                              leftIndent=36, firstLineIndent=0,
                              spaceBefore=6, spaceAfter=6))

    story.append(Paragraph("Gemini Prompt Evaluation Report", styles['h1']))
    story.append(Spacer(1, 0.3 * 25.4)) # More space after title

    for eval_item in evaluations:
        story.append(Paragraph(f"<b>Prompt:</b> {eval_item['prompt']}", styles['h2']))
        story.append(Spacer(1, 0.2 * 25.4)) # Increased space
        story.append(Paragraph(f"<b>Response:</b>", styles['h3']))
        # Convert Markdown response to HTML for better rendering in ReportLab
        # Note: For proper table rendering, a Markdown table parser would be needed to convert
        # Markdown tables into ReportLab Table objects.
        html_response = markdown.markdown(eval_item['response'])
        story.append(Paragraph(html_response, styles['Indented'])) # Use the new indented style
        story.append(Spacer(1, 0.6 * 25.4)) # Increased space between prompt-response pairs

    try:
        doc.build(story)
        print(f"PDF report generated: {output_filename}")
    except Exception as e:
        print(f"Error generating PDF report: {e}")

def run_prompt_evaluation(file_type, selected_pdf_files, news_summary_path):
    print("Starting prompt evaluation...")
    prompts = read_prompts(file_type)
    if not prompts:
        print(f"No prompts found for file type '{file_type}'. Skipping evaluation.")
        return

    # Include options_primer.pdf and news_summary_path
    all_files_for_gemini = list(selected_pdf_files)
    options_primer_path = os.path.join("files", "options_primer.pdf")
    if os.path.exists(options_primer_path):
        all_files_for_gemini.append(options_primer_path)
    else:
        print(f"Warning: '{options_primer_path}' not found. Skipping its inclusion in Gemini evaluation.")

    if news_summary_path and os.path.exists(news_summary_path):
        all_files_for_gemini.append(news_summary_path)
    else:
        print(f"Warning: News summary file '{news_summary_path}' not found or not provided. Skipping its inclusion in Gemini evaluation.")

    if not all_files_for_gemini:
        print("No files to evaluate with Gemini. Skipping prompt evaluation.")
        return

    print("Files being sent to Gemini for evaluation:")
    for f_path in all_files_for_gemini:
        print(f"- {os.path.basename(f_path)}")

    file_contents = get_file_content_for_gemini(all_files_for_gemini)
    if not file_contents:
        print("No readable file content found for Gemini evaluation. Skipping.")
        return

    evaluations = evaluate_with_gemini(prompts, file_contents)

    # Output Management: Save to output/ directory
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    today = datetime.now().strftime("%m%d%Y")
    output_pdf_filename = os.path.join(output_dir, f"PromptSummary_{file_type}_{today}.pdf")
    generate_pdf_report(evaluations, output_pdf_filename)

if __name__ == "__main__":
    # For standalone testing, provide dummy file type and files
    # This part will likely be removed or simplified once integrated with main.py
    print("This script is intended to be run via main.py for full functionality.")
    print("For standalone testing, ensure you have COR_prompts.txt and COR_*.pdf files in 'files/'.")
    dummy_file_type = "COR"
    dummy_pdf_files = [os.path.join("files", f) for f in os.listdir("files/") if f.lower().endswith('.pdf') and f.startswith('COR_')][:3]
    if dummy_pdf_files:
        run_prompt_evaluation(dummy_file_type, dummy_pdf_files)
    else:
        print("No dummy COR_*.pdf files found for standalone testing.")
