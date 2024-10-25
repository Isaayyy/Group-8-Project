# Import the libraries
import pdfplumber
import pandas as pd
import re
import json

import pdfplumber
import pytesseract
from PIL import Image
from PIL import ImageEnhance
import os
import tkinter as tk
from tkinter import filedialog

# Function to preprocess the image for better OCR results
def preprocess_image(pil_image):
    # Convert to grayscale
    pil_image = pil_image.convert("L")
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(2.0)  # Increase contrast
    return pil_image

# Function to extract text from PDF including images with OCR
def extract_text_with_ocr(pdf_file):
    extracted_text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text from the page (standard text)
            page_text = page.extract_text()
            extracted_text += page_text if page_text else ''

            # Extract images and apply OCR to them
            for img_index, img in enumerate(page.images):
                # Get image coordinates and extract the image
                x0, top, x1, bottom = img['x0'], img['top'], img['x1'], img['bottom']
                image_cropped = page.within_bbox((x0, top, x1, bottom)).to_image()
                pil_image = image_cropped.original  # Convert to PIL Image format

                # Preprocess the image
                processed_image = preprocess_image(pil_image)

                # Use pytesseract to do OCR on the processed image
                ocr_text = pytesseract.image_to_string(processed_image, config='--psm 11')  # Set page segmentation mode
                extracted_text += ocr_text

    return extracted_text

# Function to open a file dialog and select a PDF
def select_pdf_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    pdf_file = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )
    return pdf_file

# Select and process the PDF
pdf_file = select_pdf_file()

if pdf_file:  # Check if a file was selected
    extracted_text = extract_text_with_ocr(pdf_file)
    print("Extracted Text:\n", extracted_text)
else:
    print("No file was selected.")
