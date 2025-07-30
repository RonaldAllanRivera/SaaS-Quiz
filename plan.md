# Story Generation & Quiz Feature Plan

## Overview
This feature will allow kids to request AI-generated stories (with images) based on their chosen topic and grade level. After reading, kids will take a quiz. Passing the quiz earns tokens and generates a message. Stories, images, and categories are stored and reused.

## Architecture Review
- **Tokens**: Already implemented for rewarding kids (see quizzes/views.py:QuizSubmitAnswerAPIView).
- **Messages**: Used in feedback and responses (see reports/views.py and quizzes/views.py).
- **OpenAI Integration**: Used for quiz and feedback generation (see reports/views.py:AIReportFeedbackAPIView, quizzes/views.py:QuizGenerateAPIView).
- **AWS Integration**: Used for image/file storage (see lessons/views.py:LessonUploadAPIView for image handling, but AWS specifics may need review/expansion).
- **Models**: Quiz, Question, Child, Attempt, Feedback, LessonText (for stories), etc.
- **API Structure**: Django REST Framework, endpoints under `/api/v1/`.

## Feature Requirements

### 📚 Books (AI-powered stories with images)
- Generate stories with 2–3 pages and relevant images from Pixabay
- Each story is tailored to the child’s topic, age, grade, and lexile
- Each story has its own quiz (separate from lesson quizzes)
- Images are deduplicated and stored locally
- Fallback image is used if Pixabay fails

#### Books API Endpoints
- `POST /api/v1/books/generate/` – Generate a new story with images
- `POST /api/v1/books/quiz/` – Generate a quiz for a story
- `POST /api/v1/books/image/` – Fetch a deduplicated image from Pixabay for a keyword

### 📝 Lessons (Image-based quiz generation)
- Upload lesson images, extract text, and generate quizzes from lesson content
- Each lesson has its own quiz (separate from books quizzes)

### Shared Features
- Both books and lessons use the same child, lexile, age, grade, and authentication system
- Both books and lessons use the same token rewards, performance feedback, and improvement tips

1. **API Endpoint for Story Generation**
   - Input: topic (text), grade level (from logged-in child), child_id
   - Output: story (max 20 pages), 1 image per page, category (AI-generated), story & image references stored
2. **Image Sourcing & Caching**
   - Use free stock image APIs (Pixabay, Pexels, Unsplash) with safe search
   - AI generates search queries for each story page
   - Implement hybrid caching:
     - Hotlink images initially
     - Cache locally or on S3 for better performance
     - Fallback to default images if needed
   - Optimize images (<500KB, web-friendly format)
3. **Story Storage**
   - Store stories in DB (new model or extend LessonText)
   - Store images in S3, save URLs in DB
   - Save/assign category (avoid duplicates)
4. **Quiz Generation**
   - After reading, generate 10-question quiz (AI or template based)
   - Store quiz/attempt/results
5. **Token & Messaging**
   - Passing quiz: award tokens
   - Auto-generate pass/fail message for kid
6. **Story Discovery**
   - Endpoint/page for kids to choose from generated stories
   - Stories/images are reusable for other kids

## Task List
- [x] Review current system architecture and relevant code (tokens, messages, DB, AWS integration)
- [ ] Design API endpoint for story generation (input: topic, grade level, child_id)
- [ ] Integrate free stock image API (Pixabay/Pexels/Unsplash) with safe search
- [ ] Implement hybrid image caching (hotlink + S3/local storage)
- [ ] Add fallback/default images for failed searches
- [ ] Ensure grade-level adaptation in story generation
- [ ] Paginate story (max 20 pages, 1 image per page)
- [ ] Store stories in DB; upload images to AWS
- [ ] Generate and store categories via AI, avoiding duplicates
- [ ] Implement quiz generation (10 questions, after story completion)
- [ ] Token reward logic for passing quiz
- [ ] Auto-generate and send pass/fail messages to kids
- [ ] Endpoint/page for kids to select from generated stories
- [ ] Enable reuse of stories/images by other kids

## Next Steps
- Design and implement the story generation API endpoint (backend)
- Update DB models for stories, image references, and categories
- Implement hybrid image caching strategy
- Set up safe search filters and content moderation
- Frontend: Add UI for topic input, story display, image paging, quiz, and story selection

---
*This file is auto-generated as the root plan for the Story Generation & Quiz Feature.*
