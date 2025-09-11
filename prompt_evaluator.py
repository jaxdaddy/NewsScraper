import os
import fitz  # PyMuPDF
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def read_prompts(prompts_file="prompts.txt"):
    """Reads prompts from the prompts.txt file."""
    prompts = []
    if not os.path.exists(prompts_file):
        print(f"Error: '{prompts_file}' not found.")
        return prompts
    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]
    return prompts

def get_file_content_for_gemini(files_dir="files/"):
    """Reads content of all files in files/ directory and prepares for Gemini multimodal input."""
    contents = []
    for filename in os.listdir(files_dir):
        filepath = os.path.join(files_dir, filename)
        if os.path.isfile(filepath):
            try:
                if filename.lower().endswith('.pdf'):
                    # For PDFs, extract text
                    document = fitz.open(filepath)
                    text = ""
                    for page_num in range(document.page_count):
                        page = document.load_page(page_num)
                        text += page.get_text()
                    document.close()
                    contents.append({'mime_type': 'text/plain', 'data': text, 'filename': filename})
                else:
                    # For other text files, read directly
                    with open(filepath, 'r', encoding='utf-8') as f:
                        contents.append({'mime_type': 'text/plain', 'data': f.read(), 'filename': filename})
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    return contents

def evaluate_with_gemini(prompts, file_contents):
    """Sends prompts and file contents to Gemini for evaluation."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest') # Use the same model as sym_extract.py
    evaluations = []
    for prompt_text in prompts:
        try:
            # Prepare parts for multimodal input
            # Add instruction for structured output
            modified_prompt_text = prompt_text + "\n\nPlease provide your response in a clear, concise, and structured format, using Markdown (e.g., bullet points, bolding) where appropriate for readability."
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

    story.append(Paragraph("Gemini Prompt Evaluation Report", styles['h1']))
    story.append(Spacer(1, 0.2 * 25.4)) # More space after title

    for eval_item in evaluations:
        story.append(Paragraph(f"<b>Prompt:</b> {eval_item['prompt']}", styles['h2']))
        story.append(Spacer(1, 0.1 * 25.4))
        story.append(Paragraph(f"<b>Response:</b>", styles['h3']))
        # Note: reportlab's Paragraph does not natively render Markdown. 
        # Gemini's Markdown output will appear as plain text unless parsed.
        story.append(Paragraph(eval_item['response'], styles['Normal']))
        story.append(Spacer(1, 0.4 * 25.4)) # More space between prompt-response pairs

    try:
        doc.build(story)
        print(f"PDF report generated: {output_filename}")
    except Exception as e:
        print(f"Error generating PDF report: {e}")

def run_prompt_evaluation():
    print("Starting prompt evaluation...")
    prompts = read_prompts()
    if not prompts:
        print("No prompts found in prompts.txt. Skipping evaluation.")
        return

    files_dir = "files/"
    if not os.path.exists(files_dir) or not os.listdir(files_dir):
        print(f"No files found in '{files_dir}'. Skipping prompt evaluation.")
        return

    file_contents = get_file_content_for_gemini(files_dir)
    if not file_contents:
        print("No readable file content found for Gemini evaluation. Skipping.")
        return

    evaluations = evaluate_with_gemini(prompts, file_contents)

    today = datetime.now().strftime("%m%d%Y")
    output_pdf_filename = os.path.join("files", f"PromptSummary_{today}.pdf") # Save to files/ directory
    generate_pdf_report(evaluations, output_pdf_filename)

if __name__ == "__main__":
    run_prompt_evaluation()
