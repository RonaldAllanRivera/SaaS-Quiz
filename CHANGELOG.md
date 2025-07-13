# 📜 CHANGELOG - QuizNest

## [2.5.2] — 2025-07-13

### Changed
- Backend `.env` file is now always loaded from the `backend/` directory for all Django and custom scripts
- Updated README.md to clarify `.env` location and backend setup steps
- Removed staticfiles Docker volume mount from backend service to prevent local staticfiles folder from hiding collected static files; Django admin static is now always served correctly in Docker.

### Added
- Utility script `backend/load_env.py` for loading environment variables in custom backend scripts

---

## [2.5.1] — 2025-07-06

### Added
- User email display in the welcome message after login
- Automatic user profile fetching after authentication

### Changed
- Improved welcome message visibility with better text contrast
- Enhanced error handling for user profile fetching
- Removed Facebook login references from the UI

### Fixed
- Fixed email display in the welcome message for Google OAuth users

## [2.5.0] — 2025-07-06

### Added

- **Google Social Login**: Integrated Google OAuth2 authentication for seamless sign-in
- **Environment-based Email Configuration**: Added support for different email backends in development and production
- **Email Verification**: Configured email verification settings for production environments
- **Improved Docker Local Development**: Database password is now loaded from a root `.env` file (gitignored) instead of being hardcoded in `docker-compose.yml`. This is best practice and prevents secret scanning alerts.

### Changed

- Moved environment files (`.env` and `.env-sample`) to the backend directory for better organization
- Removed redundant root `manage.py` in favor of the one in the backend directory
- Updated documentation to reflect new file structure and setup instructions

### Fixed

- Resolved `NoReverseMatch` error for `account_signup` URL
- Fixed email sending configuration to prevent connection errors in development
- Updated deprecated allauth settings to use current recommended configurations

## [2.4.0] — 2025-07-05

### Added

- **Quiz Answer Submission**: New endpoint (`/quizzes/<quiz_id>/questions/<question_id>/submit/`) allows children to submit answers one by one.
- **Automatic Scoring & Rewards**: The submission API automatically checks answers, updates the attempt score, and awards tokens to the child's profile upon passing a quiz.
- **Token Spending API**: New endpoint (`/quizzes/rewards/spend/`) allows children to spend their earned tokens on virtual items like avatars and backgrounds.
- **AI-Powered Feedback Reports**: New endpoint (`/reports/generate/`) uses OpenAI to generate a personalized, encouraging feedback report for parents based on a child's incorrect answers.
- **API Versioning**: All backend APIs are now versioned under the `/api/v1/` prefix for better long-term maintenance and scalability.

### Fixed

- Resolved multiple bugs during testing, including a missing `Pillow` dependency, a corrupted virtual environment, and deprecated OpenAI model names (`gpt-4-vision-preview`).
- Corrected the OpenAI API payload structure for `gpt-4-turbo` to handle image URLs correctly.


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