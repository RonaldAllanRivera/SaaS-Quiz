# 📜 CHANGELOG - QuizNest

## [2.3.0] — 2025-06-21

### Added

- Age and grade level fields to Child model for better quiz targeting
- Parent can now set age and grade level when creating/editing a child profile
- Quiz generation API prompt now includes child’s grade and age for simpler, grade-appropriate questions
- All quiz generation and child serializers updated to handle new fields


## [2.2.1] — 2025-06-21

### Fixed

- All Django/DRF APIViews and serializers updated for Pylance compatibility: type hints, explicit Dict[str, Any] for `validated_data`, `getattr` for related fields, and conditional access to resolve static checker issues
- Quiz creation now generates a guaranteed unique, non-empty `link_slug` using UUID to resolve IntegrityError and 500 errors when generating quizzes
- Regex extraction of OpenAI quiz questions made robust to prevent `.group()` on `None` matches (eliminates internal server errors for bad AI output)
- Reverse relationships on models now use correct `related_name` and type-safe access for static analysis and runtime safety

### Changed

- All quiz/question/lesson API logic now Pylance-friendly with zero type or attribute warnings in VS Code
- Updated view logic for safer dict and attribute access


## [2.2.0] — 2025-06-21

### Added

- Subject list API endpoint for populating subject dropdown on frontend
- Parent's uploaded lessons API endpoint for dashboard lesson management
- Quiz list API endpoint with filter by lesson for parent quiz management
- Quiz detail endpoint with nested questions for delivering full quizzes to frontend
- Single-question API endpoint for paginated/stepwise quiz UI
- All endpoints authenticated with DRF token-based authentication
- All new endpoints verified working with Postman and test data

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