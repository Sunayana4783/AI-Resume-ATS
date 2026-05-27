import pdfplumber
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:   # important fix
                text += page_text
    return text


def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text


pdf_path = r"C:\Users\sunay\OneDrive\Desktop\Resume-Parser-AI\resumes\myresume.pdf"


text = extract_text(pdf_path)
cleaned_text = clean_text(text)


tokens = word_tokenize(cleaned_text)


stop_words = set(stopwords.words('english'))

filtered_words = [word for word in tokens if word not in stop_words]


print("\n--- TOKENS ---")
print(tokens)

print("\n--- FILTERED WORDS ---")
print(filtered_words)


skills_list = [
    "python", "java", "sql", "html", "css", "javascript",
    "machine learning", "deep learning", "data science",
    "pandas", "numpy", "nlp", "flask", "django",
    "c", "c++", "git"
]

text_joined = " ".join(filtered_words)

detected_skills = []

for skill in skills_list:
    if skill in text_joined:
        detected_skills.append(skill)

print("\n--- DETECTED SKILLS ---")
print(set(detected_skills))