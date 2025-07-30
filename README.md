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

---

## 📚 Books API (AI Stories & Quizzes)

### Media/Image Handling
- Book/story images are fetched from Pixabay, deduplicated, and stored in the root `media/book_images/` folder.
- Images are served at `/media/book_images/...` in development (Django `DEBUG=true`).
- Docker Compose must use `DEBUG=true` (not `1` or `True`) for Django to serve media files locally.
- The backend container must map `./media:/app/media` so media files persist and are accessible.

### Postman Testing Instructions
1. **Authenticate and Obtain Token** (if needed)
   - Use `/api/v1/auth/login/` or Google OAuth flow to get a token.
2. **Generate a New Book Story**
   - `POST /api/v1/books/generate/`
   - Body:
     ```json
     {
       "topic": "Dinosaurs",
       "grade_level": 3,
       "lexile": 100,
       "child_id": 42
     }
     ```
   - Response: Book object with pages, each with `image` (media URL).
3. **Generate a Quiz for a Book**
   - `POST /api/v1/books/quiz/`
   - Body:
     ```json
     {
       "story_id": 101,
       "child_id": 42
     }
     ```
   - Response: Quiz object with questions.
4. **Fetch a Deduplicated Image from Pixabay**
   - `POST /api/v1/books/image/`
   - Body:
     ```json
     {
       "keyword": "dinosaur"
     }
     ```
   - Response: `{ "image_url": "/media/book_images/...", ... }`

**All endpoints require authentication. Use the same child IDs and user context as with lessons. Book and lesson quizzes are separate.**

---


- **Frontend:** Next.js (React) with custom auth context
- **Backend:** Django + Django REST Framework
- **Authentication:** Google OAuth2 with django-allauth and dj-rest-auth
- **AI:** OpenAI GPT-4 Vision for OCR and quiz generation
- **Payments:** Stripe for subscription plans
- **Database:** PostgreSQL
- **DevOps:** Docker & Docker Compose for local development and orchestration

## 🛠️ Getting Started

### 🐳 Docker-based Local Development

You can run the entire app locally (backend, frontend, and database) using Docker and Docker Compose. This is the recommended way to develop and test the app.

### 1. One-time Setup
- Ensure you have Docker and Docker Compose installed
- **Create a `.env` file in the project root (same folder as `docker-compose.yml`) with:**
  ```
  POSTGRES_PASSWORD=postgres
  ```
  This file is required for Docker Compose to start the database. It is gitignored and should never be committed.
- Copy `.env.example` to `.env` in `backend/` and fill in your secrets
- (Optional) Copy `.env.local.example` to `frontend/.env.local` for frontend env vars

### 2. Start All Services

```bash
# From the project root
docker-compose up
```

- This will build (if needed) and start the backend (Django), frontend (Next.js), and a PostgreSQL database
- Static files are collected automatically
- All dependencies are installed automatically in the containers
- No manual database setup is required

### 3. Access the App
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Django Admin: http://localhost:8000/admin/

### 4. Stopping Services

```bash
docker-compose down
```

### 5. Notes
- If you change dependencies (backend/requirements.txt or frontend/package.json), re-run `docker-compose build`
- If ports are in use, either stop the conflicting process or change the port in `docker-compose.yml`
- If you want to reset the DB and volumes: `docker-compose down -v`
- The backend requirements now include allauth, dj-rest-auth, PyJWT, cryptography, and whitenoise for full authentication and static file support.
- **Troubleshooting:** If Django admin is missing styles or static files, make sure you do NOT have a local `backend/staticfiles` folder. Docker now manages static files internally, and local folders can interfere with this.

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

### Quizzes & Questions (Lessons)
- `POST /api/v1/quizzes/generate/` - Generate a new quiz from a lesson.
- `GET /api/v1/quizzes/` - List all quizzes for the authenticated parent.
- `GET /api/v1/quizzes/<quiz_id>/questions/<question_number>/` - Get a specific question from a quiz.
- `POST /api/v1/quizzes/<quiz_id>/questions/<question_id>/submit/` - Submit an answer for a question.

### Books & Stories
- `POST /api/v1/books/generate/` - Generate a new story with images.
- `GET /api/v1/books/` - List all books for the authenticated parent.
- `GET /api/v1/books/<book_id>/questions/<question_number>/` - Get a specific question from a book.
- `POST /api/v1/books/<book_id>/questions/<question_id>/submit/` - Submit an answer for a question.

### Rewards & Reports
- `POST /api/v1/quizzes/rewards/spend/` - Spend tokens on rewards (e.g., avatars).
- `POST /api/v1/reports/generate/` - Generate an AI-powered feedback report for a quiz attempt.

## 📚 Books (AI-powered stories with images)
- Generate stories with 2–3 pages and relevant images from Pixabay
- Each story is tailored to the child’s topic, age, grade, and lexile
- Each story has its own quiz (separate from lesson quizzes)
- Images are deduplicated and stored locally
- Fallback image is used if Pixabay fails

### 📝 Lessons (Image-based quiz generation)
- Upload lesson images, extract text, and generate quizzes from lesson content
- Each lesson has its own quiz (separate from books quizzes)

### Shared Features
- Both books and lessons use the same child, lexile, age, grade, and authentication system
- Both books and lessons use the same token rewards, performance feedback, and improvement tips

## 💡 Project Goals

- Empower young learners through fun and engaging AI-powered quizzes
- Help parents track and nurture early development
- Create a safe, playful digital space for learning

## 📘 License

MIT License – feel free to fork, contribute, and customize!

---
