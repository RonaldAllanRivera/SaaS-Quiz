# QuizNest 🐣 – AI-Powered Quiz Playground for Kids

**QuizNest** is a SaaS platform that empowers parents to create personalized, AI-generated quizzes tailored to their children’s age and grade level, starting with elementary schoolers. Parents upload lesson images and select a subject, age, and grade level, ensuring quizzes match each child’s ability. With gamified learning, performance tracking, and parental insights, QuizNest turns every moment into a learning opportunity.

## 🚀 Features

- 🔐 Secure Google login for parents
- 👦👧 Parent-managed child profiles (with age and grade level)
- 📸 Upload lesson images by subject (Math, English, Filipino, CLE, etc.)
- 🧠 OpenAI-powered text extraction and quiz generation, customized for each grade
- ❓ Auto-generated multiple choice and true/false quizzes
- 🧒 One-question-per-page kid interface
- 🎉 Token rewards for completed quizzes (custom avatars & backgrounds)
- 📊 AI-analyzed performance feedback and improvement tips for parents
- 🛡️ Child-safe design, dark mode, and text-to-speech support


## 📦 Tech Stack

- **Frontend:** Next.js (React) with custom auth context
- **Backend:** Django + Django REST Framework
- **Authentication:** Google OAuth2 with django-allauth and dj-rest-auth
- **AI:** OpenAI GPT-4 Vision for OCR and quiz generation
- **Payments:** Stripe for subscription plans
- **Database:** PostgreSQL

## 🛠️ Getting Started

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.10
- PostgreSQL
- API Keys: 
  - OpenAI API Key
  - Google OAuth2 Client ID (for web application)
  - Stripe API Keys (for payments)
  - Email SMTP Settings (for production)

### Local Setup

```bash
git clone https://github.com/yourusername/quiznest.git
cd quiznest

# Backend setup
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
cp .env-sample .env  # Update with your actual environment variables
# NOTE: The .env file is now located in the backend directory. All backend environment variables must be set in backend/.env.
python manage.py migrate
python manage.py runserver

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
npm run dev
```

## 📄 Environment Variables

See `.env-sample` in `/backend` and `.env.example` in `/frontend` for necessary configuration variables.

**If you write custom scripts in the backend that need environment variables, import and call `load_env.py` before accessing env vars:**
```python
from load_env import load_backend_env
load_backend_env()
```
This ensures your script loads `backend/.env` just like Django does.

## ⚙️ API Endpoints

All backend endpoints are versioned under `/api/v1/`. Authentication is required for most endpoints.

### Authentication
- `POST /api-token-auth/` - Obtain user authentication token.

### Lessons & Subjects
- `GET /api/v1/lessons/subjects/` - List all available subjects.
- `POST /api/v1/lessons/upload/` - Upload a lesson image to generate lesson text.
- `GET /api/v1/lessons/my-lessons/` - List all lessons for the authenticated parent.

### Quizzes & Questions
- `POST /api/v1/quizzes/generate/` - Generate a new quiz from a lesson.
- `GET /api/v1/quizzes/` - List all quizzes for the authenticated parent.
- `GET /api/v1/quizzes/<quiz_id>/questions/<question_number>/` - Get a specific question from a quiz.
- `POST /api/v1/quizzes/<quiz_id>/questions/<question_id>/submit/` - Submit an answer for a question.

### Rewards & Reports
- `POST /api/v1/quizzes/rewards/spend/` - Spend tokens on rewards (e.g., avatars).
- `POST /api/v1/reports/generate/` - Generate an AI-powered feedback report for a quiz attempt.

## 💡 Project Goals

- Empower young learners through fun and engaging AI-powered quizzes
- Help parents track and nurture early development
- Create a safe, playful digital space for learning

## 📘 License

MIT License – feel free to fork, contribute, and customize!

---
