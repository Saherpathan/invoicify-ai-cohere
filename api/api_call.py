from flask import Flask, request, render_template, redirect, url_for
import pdfplumber
import cohere
from dotenv import load_dotenv
import os
import json
import re
from PIL import Image
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
import os

# Update the upload and output folders
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/output'

# Ensure the directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Cohere API key
cohere_api_key = os.getenv('COHERE_API_KEY')

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract text from images using pytesseract
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

# Function to use Cohere API for text extraction
def extract_invoice_details_with_cohere(text, cohere_api_key):
    co = cohere.Client(cohere_api_key)
    prompt = f"""
    Extract the following details from the given text:

    1. Customer Name
    2. Customer Address
    3. Customer Phone No
    4. Customer Email ID
    5. Products (Name, HSN, Quantity, Amount). Ensure that percentages or extra details are not included in the product names.
    6. Total Amount

    Text:
    {text}

    Please provide the details in the following JSON format without any extra characters:

    {{
        "Customer Name": "value",
        "Customer Address": "value",
        "Customer Phone No": "value",
        "Customer Email ID": "value",
        "Products": [
            {{"Name": "value", "HSN": "value", "Quantity": "value", "Amount": "value"}},
            ...
        ],
        "Total Amount": "value"
    }}
    """
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=300,
        temperature=0.5,
    )

    response_text = response.generations[0].text
    try:
        json_result = json.loads(response_text)
    except json.JSONDecodeError:
        # Clean and extract JSON
        json_string = re.search(r'\{.*\}', response_text, re.DOTALL).group(0)
        json_result = json.loads(json_string)

    return json_result

def format_json_as_text(json_data):
    customer_name = json_data.get('Customer Name', 'N/A')
    customer_address = json_data.get('Customer Address', 'N/A')
    customer_phone = json_data.get('Customer Phone No', 'N/A')
    customer_email = json_data.get('Customer Email ID', 'N/A')
    total_amount = json_data.get('Total Amount', 'N/A')

    products = json_data.get('Products', [])

    formatted_text = (
        "<div style='border: 2px solid #E5E7EB; padding: 20px; border-radius: 8px; margin-bottom: 20px;'>"
        "<h2 style='font-size: 24px; color: #4F46E5; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px;'>Customer Details</h2>"
        f"<p style='margin: 10px 0;'><strong>Name:</strong> {customer_name}</p>"
        f"<p style='margin: 10px 0;'><strong>Address:</strong> {customer_address}</p>"
        f"<p style='margin: 10px 0;'><strong>Phone No:</strong> {customer_phone}</p>"
        f"<p style='margin: 10px 0;'><strong>Email ID:</strong> {customer_email}</p>"
        "</div>"
    )

    if products:
        formatted_text += (
            "<div style='border: 2px solid #E5E7EB; padding: 20px; border-radius: 8px; margin-bottom: 20px;'>"
            "<h2 style='font-size: 24px; color: #4F46E5; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px;'>Product Details</h2>"
        )
        for product in products:
            name = product.get('Name', 'N/A')
            hsn = product.get('HSN', 'N/A')
            quantity = product.get('Quantity', 'N/A')
            amount = product.get('Amount', 'N/A')

            formatted_text += (
                "<div style='margin-bottom: 15px; padding: 15px; border: 1px solid #D1D5DB; border-radius: 8px;'>"
                f"<p style='margin: 5px 0;'><strong>Product Name:</strong> {name}</p>"
                f"<p style='margin: 5px 0;'><strong>HSN:</strong> {hsn}</p>"
                f"<p style='margin: 5px 0;'><strong>Quantity:</strong> {quantity}</p>"
                f"<p style='margin: 5px 0;'><strong>Amount:</strong> {amount}</p>"
                "</div>"
            )
        formatted_text += "</div>"
    else:
        formatted_text += "<p>No products found.</p>"

    formatted_text += (
        "<div style='border: 2px solid #E5E7EB; padding: 20px; border-radius: 8px;'>"
        "<h2 style='font-size: 24px; color: #4F46E5; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px;'>Total Amount</h2>"
        f"<p style='margin: 10px 0;'><strong>Total Amount in INR:</strong> {total_amount}</p>"
        "</div>"
    )

    return formatted_text


# Function to save JSON result to file
def save_json_to_file(json_data, filename):
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    with open(output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and (file.filename.endswith('.pdf') or file.filename.endswith(('.png', '.jpg', '.jpeg'))):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            else:
                extracted_text = extract_text_from_image(file_path)

            # Extract details using Cohere
            extracted_details = extract_invoice_details_with_cohere(extracted_text, cohere_api_key)
            formatted_text = format_json_as_text(extracted_details)

            # Save the JSON result
            save_json_to_file(extracted_details, f"{filename.split('.')[0]}.json")

            return render_template('result.html', details=formatted_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
