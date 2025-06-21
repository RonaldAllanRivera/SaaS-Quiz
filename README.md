# QuizNest 🐣 – AI-Powered Quiz Playground for Kids

**QuizNest** is a SaaS platform that empowers parents to create personalized, AI-generated quizzes for their 3-year-old children using simple lesson image uploads. With gamified learning, performance tracking, and parental insights, QuizNest turns every moment into a learning opportunity.

## 🚀 Features

- 🔐 Google/Facebook login for parents
- 📸 Upload lesson images by subject (Math, English, Filipino, CLE, etc.)
- 🧠 OpenAI-powered text extraction and quiz generation
- ❓ Auto-generated multiple choice and true/false quizzes
- 🧒 One-question-per-page kid interface
- 🎉 Token rewards for completed quizzes (custom avatars & backgrounds)
- 📊 AI-analyzed performance feedback and improvement tips for parents
- 🛡️ Child-safe design, dark mode, and text-to-speech support

## 📦 Tech Stack

- **Frontend:** Next.js (React) with NextAuth
- **Backend:** Django + Django REST Framework
- **AI:** OpenAI GPT-4 Vision for OCR and quiz generation
- **Payments:** Stripe for subscription plans
- **Database:** PostgreSQL

## 🛠️ Getting Started

### Prerequisites

- Node.js ≥ 18
- Python ≥ 3.10
- PostgreSQL
- API Keys: OpenAI, Stripe, Google (OAuth)

### Local Setup

```bash
git clone https://github.com/yourusername/quiznest.git
cd quiznest

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
npm run dev
```

## 📄 Environment Variables

See `.env.example` files in both `/backend` and `/frontend` for necessary configuration variables.

## 💡 Project Goals

- Empower young learners through fun and engaging AI-powered quizzes
- Help parents track and nurture early development
- Create a safe, playful digital space for learning

## 📘 License

MIT License – feel free to fork, contribute, and customize!

---
