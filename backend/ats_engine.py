import re
import fitz  # PyMuPDF
import pandas as pd
import torch
from collections import Counter
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- LOAD MODEL (ONLY ONCE) ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- LOAD SKILL DATABASE ----------------
skill_df = pd.read_csv("skills.csv")
skill_list = skill_df["skillLabel"].dropna().unique().tolist()

# Precompute skill embeddings once
skill_embeddings = model.encode(
    skill_list,
    convert_to_tensor=True,
    show_progress_bar=True
)

# ---------------- TEXT CLEANING ----------------
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ---------------- PDF EXTRACTION ----------------
def extract_text_from_pdf_stream(file_bytes) -> str:
    text = ""
    try:
        with fitz.open(stream=memoryview(file_bytes), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        if not text.strip():
            print("Warning: No text found in PDF.")
            return ""

        return clean_text(text)

    except Exception as e:
        print(f"PDF Extraction Error: {str(e)}")
        return ""

# ---------------- EXPERIENCE EXTRACTION ----------------
def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s+years?',
        r'(\d+)\s+yrs?',
        r'(\d+)\s+year',
        r'experience of (\d+)'
    ]

    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(m) for m in matches])

    return max(years) if years else 0

# ---------------- JD REQUIREMENT CLASSIFICATION ----------------
def classify_requirement(line):
    line_lower = line.lower()

    if any(word in line_lower for word in ["must", "mandatory", "required"]):
        return "must_have"
    elif any(word in line_lower for word in ["preferred", "nice to have"]):
        return "good_to_have"
    else:
        return "other"

# ---------------- SEMANTIC SKILL EXTRACTION ----------------
def extract_skills_semantic(text, threshold=0.65):
    text_embedding = model.encode(text, convert_to_tensor=True)

    cosine_scores = util.cos_sim(text_embedding, skill_embeddings)[0]

    matched_skills = [
        skill_list[i]
        for i in range(len(cosine_scores))
        if cosine_scores[i] >= threshold
    ]

    return matched_skills

# ---------------- ATS SCORING ----------------
def ats_scan(resume_text: str, jd_text: str):

    if not resume_text or len(resume_text.strip()) < 10:
        return {
            "final_score": 0,
            "error": "Resume text extraction failed."
        }

    # -------- Semantic Similarity --------
    try:
        resume_emb = model.encode(resume_text)
        jd_emb = model.encode(jd_text)

        semantic_score = float(
            cosine_similarity(
                resume_emb.reshape(1, -1),
                jd_emb.reshape(1, -1)
            )[0][0] * 100
        )
    except Exception as e:
        print(f"Model Error: {e}")
        semantic_score = 0

    # -------- Keyword Matching --------
    resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
    jd_words = re.findall(r'\b\w{3,}\b', jd_text.lower())
    freq = Counter(jd_words)

    important = {w for w, c in freq.items() if c >= 2}
    matched_keywords = important & resume_words

    keyword_score = (
        len(matched_keywords) / len(important) * 100
        if important else 50
    )

    # -------- Semantic Skill Matching --------
    jd_skills = extract_skills_semantic(jd_text)
    resume_skills = extract_skills_semantic(resume_text)

    matched_skills = set(jd_skills) & set(resume_skills)

    skill_score = (
        len(matched_skills) / len(jd_skills) * 100
        if jd_skills else 100
    )

    # -------- Experience Matching --------
    jd_exp = extract_experience_years(jd_text)
    resume_exp = extract_experience_years(resume_text)

    if jd_exp > 0:
        experience_score = min((resume_exp / jd_exp) * 100, 100)
    else:
        experience_score = 100

    # -------- Final Weighted Score --------
    final_score = (
        semantic_score * 0.40 +
        skill_score * 0.30 +
        keyword_score * 0.30
    )

    return {
        "final_score": round(final_score, 2),
        "semantic_score": round(semantic_score, 2),
        "skill_score": round(skill_score, 2),
        "keyword_score": round(keyword_score, 2),
        "experience_score": round(experience_score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(set(jd_skills) - matched_skills),
        "matched_keywords": list(matched_keywords)[:15]
    }