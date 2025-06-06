# resume_utils.py
import os
import re
import nltk
from docx import Document
from PIL import Image
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

nltk.download('punkt')

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass
    return text.lower()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text).lower()

def extract_text_from_image(file_path):
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text.lower()
    except:
        return ""

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = nltk.word_tokenize(text)
    return " ".join(tokens)

def calculate_score(resume_text, job_description):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    jd_words = set(cleaned_jd.split())
    resume_words = set(cleaned_resume.split())
    matched_words = jd_words.intersection(resume_words)

    min_score = 20
    total_keywords = len(jd_words)
    matched = len(matched_words)

    if total_keywords == 0:
        score = 0
    elif matched == 0:
        score = min_score
    elif matched == total_keywords:
        score = 100
    else:
        score = min_score + ((matched / total_keywords) * (100 - min_score))

    return round(score)