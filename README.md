# 💫 ATS Resume Checker

Yo 👋 I'm Saurav, a B.Tech student specializing in AI & ML, MERN, and Data Science. This project is an intelligent **ATS Resume Checker** designed to help candidates optimize their resumes for Applicant Tracking Systems using AI-driven insights.

---

## 🚀 About the Project:

This application analyzes resumes against specific job descriptions to provide a compatibility score and actionable feedback on missing keywords.

### Key Features:
* **AI Analysis**: Uses Large Language Models to compare resumes with job descriptions.
* **Real-time Feedback**: Provides an ATS compatibility score and identifies critical missing keywords.
* **Seamless UI**: Built with a React frontend and a FastAPI backend for high-performance processing.

---
---

##  Scoring Algorithm:

The application evaluates resumes based on three core parameters to calculate an overall compatibility percentage:

| Criteria | Weight | Description |
| :--- | :---: | :--- |
| **Keyword Matching** | **40%** | Detects industry-specific terms and tools mentioned in the JD. |
| **Skill Alignment** | **30%** | Analyzes core technical skills and soft skills relevant to the role. |
| **Contextual Relevance** | **30%** | Uses NLP to check if the experience matches the JD requirements. |

**Total Score Formula:**
$$Score = (Keywords \times 0.4) + (Skills \times 0.3) + (Context \times 0.3)$$

---

## 💻 Tech Stack:

### Frontend & UI:
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white) ![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

### Backend & AI:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

### Tools:
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

---

## 🛠️ Installation & Setup:

### 1. Backend (Python/FastAPI)
```bash
cd backend
# Activate your virtual environment
.\venv\Scripts\activate
# Install requirements
pip install -r requirements.txt
# Start the server
python main.py

cd frontend
# Install dependencies
npm install
# Start the development server
npm run dev
