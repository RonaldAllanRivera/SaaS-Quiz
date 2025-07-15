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
1. **API Endpoint for Story Generation**
   - Input: topic (text), grade level (from logged-in child), child_id
   - Output: story (max 20 pages), 1 image per page, category (AI-generated), story & images stored
2. **Image Generation & Optimization**
   - Use OpenAI or similar for kid-friendly images
   - Optimize images (<500KB, web-friendly format)
   - Store images in AWS (S3)
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
- [ ] Integrate OpenAI API for story and image generation with prompt engineering
- [ ] Implement image optimization (<500KB, web-friendly formats)
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
- Update DB models if needed for stories, images, categories
- Implement image upload to AWS and optimization
- Frontend: Add UI for topic input, story display, image paging, quiz, and story selection

---
*This file is auto-generated as the root plan for the Story Generation & Quiz Feature.*
