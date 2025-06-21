# 📜 CHANGELOG – AIWriter

## [2.0.0] — 2025-06-21

### Added

- Initialized new QuizNest SaaS project structure for quiz generation system
- Django backend scaffolded with modular apps: users, lessons, quizzes, reports
- Custom User model (`is_parent` flag) for parent-child management
- Subject and LessonText models for storing categorized lesson content
- Quiz, Question, Child, Attempt, and Feedback models for full quiz workflow
- PostgreSQL environment configuration via `.env`
- Requirements and settings set for modern DRF, Postgres, and API key management

### Docs

- README.md, .gitignore, CHANGELOG.md, and .env.example template added to repo root

## [2.1.0] — 2025-06-21

### Added

- Lesson upload API endpoint: supports image and subject input, uses OpenAI Vision for text extraction
- OpenAI Vision integration for extracting and filtering lesson text from images
- LessonText creation via API, fully linked to parent user and subject
- Quiz generation API endpoint: generates 10 random quiz questions (MCQ/TF) from extracted lesson text using OpenAI
- Full backend flow: parent can upload a lesson and generate quizzes automatically