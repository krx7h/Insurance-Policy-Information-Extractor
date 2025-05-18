# Import required libraries
import pytesseract  # For OCR
from pdf2image import convert_from_path  # Convert PDF pages to images
import spacy  # For Named Entity Recognition
import re  # For regular expressions
import os  # For file handling

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a scanned PDF using OCR
def extract_text_from_pdf(pdf_path):
    print("Converting PDF to text...")

    # Convert PDF to a list of image pages
    pages = convert_from_path(pdf_path)

    all_text = ""

    # Loop through each page and extract text
    for index in range(len(pages)):
        print("Processing page", index + 1)
        image = pages[index]
        text = pytesseract.image_to_string(image)
        all_text = all_text + text + "\n"

    return all_text


# Function to extract Policy Number using regex
def extract_policy_number(text):
    print("Extracting Policy Number...")
    pattern = r"\b(?:Policy\s*Number|Policy\s*No)[^\w]*([A-Z0-9\-]{6,})"
    match = re.search(pattern, text, re.IGNORECASE)

    if match is not None:
        policy_number = match.group(1)
        return policy_number
    else:
        return "Not Found"


# Function to extract Sum Insured using regex
def extract_sum_insured(text):
    print("Extracting Sum Insured...")
    pattern = r"\bSum\s*Insured[^\d]*([\d,]+)"
    match = re.search(pattern, text, re.IGNORECASE)

    if match is not None:
        sum_insured = match.group(1)
        return sum_insured
    else:
        return "Not Found"


# Function to extract Policy Period using regex
def extract_policy_period(text):
    print("Extracting Policy Period...")
    pattern = r"Policy\s*Period[^\d]*(\d{2}/\d{2}/\d{4})\s*(?:to|-)\s*(\d{2}/\d{2}/\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)

    if match is not None:
        start_date = match.group(1)
        end_date = match.group(2)
        policy_period = start_date + " to " + end_date
        return policy_period
    else:
        return "Not Found"


# Function to extract insured person's name using spaCy NER
def extract_insured_name(text):
    print("Extracting Name...")
    document = nlp(text)

    for entity in document.ents:
        if entity.label_ == "PERSON":
            name = entity.text
            return name

    return "Not Found"


# Main function
def extract_insurance_policy_details(pdf_file):
    print("\n Reading file:", pdf_file)

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_file)

    # Step 2: Extract details
    policy_number = extract_policy_number(text)
    sum_insured = extract_sum_insured(text)
    policy_period = extract_policy_period(text)
    insured_name = extract_insured_name(text)

    # Step 3: Display the extracted details
    print("\n Extracted Information:")
    print("Policy Number:", policy_number)
    print("Sum Insured:", sum_insured)
    print("Policy Period:", policy_period)
    print("Insured Name:", insured_name)


# Run this script directly
if __name__ == "__main__":
    folder = "insurance_policies"  # Folder with scanned PDFs

    print("\n Starting Insurance Policy Extraction...\n")

    # Loop through all PDF files in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder, filename)
            extract_insurance_policy_details(file_path)
