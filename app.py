# app.py
from flask import Flask, render_template, request
from resume_utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
    resume_file = request.files['resume']
    job_description = request.form['jd']
    
    ext = resume_file.filename.split('.')[-1].lower()
    resume_path = f"temp_resume.{ext}"
    resume_file.save(resume_path)

    resume_text = ""
    if ext == 'pdf':
        resume_text = extract_text_from_pdf(resume_path)
        if len(resume_text.strip()) < 50:
            pages = convert_from_path(resume_path, 300)
            for page in pages:
                resume_text += pytesseract.image_to_string(page).lower()
    elif ext in ['docx', 'doc']:
        resume_text = extract_text_from_docx(resume_path)
    elif ext in ['jpg', 'jpeg', 'png', 'bmp']:
        resume_text = extract_text_from_image(resume_path)
    else:
        return "❌ Unsupported file type."

    score = calculate_score(resume_text, job_description)

    # Feedback message
    if score == 100:
        message = "✅ Excellent Match – All job keywords found in resume."
    elif score >= 80:
        message = "✅ Good Match – Your resume matches well with the job description."
    elif score >= 40:
        message = "⚠ Medium Match – Some keywords matched. Try to add more relevant skills."
    else:
        message = "❌ Low Match – Your resume has very little alignment with the job description."

    return render_template('index.html', score=score, message=message)

if __name__ == "__main__":
    app.run(debug=True)