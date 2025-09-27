# Quiz Master - V2

> Project submission for Modern Application Development II (January 2025).
>
> - [📄 Project Report](PROJECT_REPORT_QUIZ_MASTER_V2.md)
> - [📹 Video Presentation](https://drive.google.com/file/d/1w2S_fLCxj1wUBu0FfCn3Lyl53yswBkMO/view?usp=drive_link)

A multi-user exam preparation platform where users can practice quizzes for different subjects and chapters.

The platform has two roles: **Admin** (Quiz Master) and **Users**.

The admin manages subjects, chapters, and quizzes, while users can register, take quizzes, and track their scores.

## Features 🚀

- **User Management**: Admin manages users, and users can register/login.
- **Quiz Creation & Management**: Admin creates subjects, chapters, and quizzes.
- **Timed Quizzes**: Users attempt quizzes with a countdown timer.
- **Score Tracking**: Users can view past quiz scores and performance analytics.
- **Background Jobs**: Celery handles CSV exports, reminders, and reports.
- **Daily Reminders**: Users get notified about new quizzes via email or chat.
- **Monthly Reports**: Users receive a summary of their quiz performance.
- **CSV Export**: Users and Admin can export quiz data.
- **Caching & Performance Optimization**: Redis improves API response times.

## Milestones ✅

- ✅ Setup project structure
- ✅ Configure Flask API
- ✅ Implement user authentication
- ✅ Create database models
- ✅ Admin dashboard for quiz management
- ✅ User dashboard for quiz attempts
- ✅ Implement quiz timer
- ✅ Store and display quiz scores
- ✅ Implement background jobs with Celery
- ✅ Implement caching with Redis
- ✅ Add CSV export functionality
- ✅ Send daily quiz reminders
- ✅ Generate and send monthly reports
- ✅ Optimize API performance
- ✅ Final testing and deployment

## Project Structure 📁

```
├── backend/                # Server-side application code
│   ├── app.py              # Flask application entry point and configuration
│   ├── cache.py            # Redis cache configuration and helper functions
│   ├── celery_app.py       # Celery task queue setup and worker config
│   ├── cleanup.sh          # Script to reset database and clear cache
│   ├── db/                 # Database related files
│   │   ├── models.py       # SQLAlchemy model definitions and relationships
│   │   ├── seed.py         # Database seeding logic and helper functions
│   │   ├── data_quizzes.py    # Sample quiz data for database seeding
│   │   └── data_subjects.py   # Sample subject data for database seeding
│   ├── routes/             # API route handlers
│   │   ├── admin_bp.py     # Admin-specific endpoints (users, stats)
│   │   ├── auth_bp.py      # Authentication endpoints (login, register)
│   │   ├── chapter_bp.py   # Chapter CRUD operations
│   │   ├── question_bp.py  # Question CRUD operations
│   │   ├── quiz_bp.py      # Quiz CRUD and attempt operations
│   │   └── subject_bp.py   # Subject CRUD operations
│   ├── static/             # Generated files (CSV exports, etc)
│   └── templates/          # HTML templates
│       └── email/          # Email notification templates
│
└── frontend/               # Client-side application code
    ├── index.html          # Main HTML template
    ├── jsconfig.json       # JavaScript/TypeScript configuration
    ├── package.json        # NPM dependencies and scripts
    ├── vite.config.js      # Vite bundler configuration
    └── src/                # Source code directory
        ├── App.vue         # Root Vue component
        ├── main.js         # JavaScript entry point
        ├── assets/         # Static assets (images, styles)
        │   └── base.css    # Global CSS styles
        ├── router/         # Vue Router configuration
        │   ├── index.js    # Route definitions and guards
        ├── store/          # State management
        │   ├── index.js    # Vue store configuration
        ├── utils/          # Helper functions and utilities
        └── views/          # Vue components by section
            ├── admin/      # Admin dashboard components
            │   └── forms/  # Admin form components
            ├── auth/       # Authentication components
            ├── common/     # Shared/common components
            └── user/       # User dashboard components
```

## ER Diagram 📊

![ER Diagram](ER_DIAGRAM_QUIZ_MASTER_V2.png)

## API Routes 🛣️

### Auth Routes `/api/auth`

- `GET /whoami` - Check current authentication status
- `POST /login` - Login with email and password
- `POST /register` - Register new user account
- `POST /logout` - Logout current user

### Admin Routes `/api/admin`

- `GET /users/<id>` - Get single user details
- `GET /users` - Get all users list
- `PUT /users/<id>/block` - Block a user
- `PUT /users/<id>/unblock` - Unblock a user
- `GET /statistics` - Get platform statistics
- `POST /repopulate` - Reset and reseed database

### User Routes `/api/user`

- `GET /quiz-attempts` - Get user's quiz attempts
- `POST /quiz-attempts/<quiz_id>` - Submit a quiz attempt
- `GET /send-test-email` - Send test email to user
- `POST /export-attempts` - Export user's attempts to CSV

### Subject Routes `/api/subject`

- `GET /get/<id>` - Get single subject
- `GET /get-all` - Get all subjects
- `POST /create` - Create new subject
- `PUT /update/<id>` - Update a subject
- `DELETE /delete/<id>` - Delete a subject

### Chapter Routes `/api/chapter`

- `GET /get/<id>` - Get single chapter
- `GET /get-all` - Get all chapters
- `POST /create` - Create new chapter
- `PUT /update/<id>` - Update a chapter
- `DELETE /delete/<id>` - Delete a chapter

### Quiz Routes `/api/quiz`

- `GET /get/<id>` - Get single quiz
- `GET /get-all` - Get all quizzes
- `POST /create` - Create new quiz
- `PUT /update/<id>` - Update a quiz
- `DELETE /delete/<id>` - Delete a quiz

### Question Routes `/api/question`

- `GET /get/<id>` - Get single question
- `GET /get-all` - Get all questions
- `POST /create` - Create new question
- `PUT /update/<id>` - Update existing question
- `DELETE /delete/<id>` - Delete a question

## Frontend Data Stores 🗄️

The application uses reactive stores to manage state. Each store is responsible for a specific domain.

### Auth Store

Properties:

- `isLoggedIn` - Boolean indicating user's login state
- `role` - User's role ('admin' or 'user')

### Subject Store

Properties:

- `subjects` - Map of subject objects indexed by ID

Methods:

- `fetch(id)` - Get single subject
- `fetchAll()` - Get all subjects
- `create(data)` - Create new subject
- `update(id, data)` - Update existing subject
- `delete(id)` - Delete subject
- `getChaptersForSubject(subject)` - Get chapters for a subject
- `handleChapterCreated(chapter)` - Handle chapter creation
- `handleChapterDeleted(chapter)` - Handle chapter deletion

### Chapter Store

Properties:

- `chapters` - Map of chapter objects indexed by ID

Methods:

- `fetch(id)` - Get single chapter
- `fetchAll()` - Get all chapters
- `create(data)` - Create new chapter
- `update(id, data)` - Update existing chapter
- `delete(id)` - Delete chapter
- `handleSubjectDeleted()` - Handle subject deletion

### Quiz Store

Properties:

- `quizzes` - Map of quiz objects indexed by ID

Methods:

- `fetch(id)` - Get single quiz
- `fetchAll()` - Get all quizzes
- `create(data)` - Create new quiz
- `update(id, data)` - Update existing quiz
- `delete(id)` - Delete quiz
- `getQuestionsForQuiz(quiz)` - Get questions for a quiz
- `handleQuestionCreated(question)` - Handle question creation
- `handleQuestionDeleted(question)` - Handle question deletion
- `handleChapterDeleted()` - Handle chapter deletion

### Question Store

Properties:

- `questions` - Map of question objects indexed by ID

Methods:

- `fetch(id)` - Get single question
- `fetchAll()` - Get all questions
- `create(data)` - Create new question
- `update(id, data)` - Update existing question
- `delete(id)` - Delete question
- `handleQuizDeleted()` - Handle quiz deletion

### Quiz Attempt Store

Properties:

- `attempts` - Map of quiz attempts indexed by ID
- `answerFeedbacks` - Map of answer feedbacks indexed by attempt ID

Methods:

- `fetchAll()` - Get all attempts for current user
- `create(quizId, answers)` - Create new quiz attempt

Each store uses the `fetchHelper` utility for API communication and maintains its data in a reactive Map structure. The stores also handle related entity changes through various handle methods to maintain data consistency.

# Project Setup and Running Guide

This guide provides step-by-step instructions for setting up and running the application on both Linux and Windows.

**Follow the sections in order.**

## Prerequisites

- Git installed
- Python 3.x
- Node.js and npm
- VSCode (recommended for terminal restoration extension)

## Initial Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/k26rahul/mad2-project-rahul.git
   cd mad2-project-rahul
   ```

2. **Set Up Virtual Environment**

   - Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Nodemon Globally**

   ```bash
   npm install -g nodemon
   ```

5. **Install Redis**

   - Linux:
     ```bash
     sudo apt-get update
     sudo apt-get install redis-server
     ```
   - Windows:
     1. Download from https://github.com/microsoftarchive/redis/releases (e.g., MSI installer).
     2. During installation:
        - Set port to 6380.
        - Check "Add to PATH".
     3. If PATH not added, manually add "C:\Program Files\Redis" to system PATH.

   **Troubleshooting Redis on Windows:**

   - If fails to start: Run `& "C:\Program Files\Redis\redis-server.exe" --bind 127.0.0.1 --port 6380`.
   - If port 6380 in use:
     1. Find process: `netstat -ano | findstr 6380`.
     2. Get details: `tasklist /FI "PID eq <PID>"`.
     3. Kill: `taskkill /PID <PID> /F` or use Task Manager (Services tab, sort by PID).

6. **Install MailHog**

   - Download from https://github.com/mailhog/MailHog/releases.
   - Linux: Use MailHog_linux_amd64; make executable and add to PATH.
   - Windows: Use MailHog_windows_amd64.exe; rename to MailHog.exe and add to PATH.

7. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application

Install VSCode extension: [Restore Terminals](https://marketplace.visualstudio.com/items?itemName=EthanSK.restore-terminals) by Ethan Sarif-Kattan.

**For Windows Users:** Delete `.vscode/restore-terminals.json` and rename `.vscode/restore-terminals.windows.json` to `restore-terminals.json` for Windows-specific commands.

1. Open project in VSCode.
2. Use extension: Press `Ctrl+Shift+P`, type "Restore Terminals", and select it.

**Note:** If extension fails (common on Windows), manually open 6 terminals in VSCode and run commands below. This is more reliable.

### Manual Terminal Commands

- **Terminal 1: Flask Backend**

  ```bash
  cd backend
  # Linux: ./run.sh
  # Windows (PowerShell): ./run.ps1
  ```

- **Terminal 2: Frontend**

  ```bash
  cd frontend
  # Linux: ./run.sh
  # Windows (PowerShell): ./run.ps1
  ```

- **Terminal 3: Redis Server**

  ```bash
  cd backend
  redis-server --port 6380
  # If Redis fails to start, refer to troubleshooting steps above.
  ```

- **Terminal 4: Celery Worker**

  ```bash
  cd backend
  # Linux: celery -A app.celery_app.celery worker --loglevel=info
  # Windows: celery -A app.celery_app.celery worker --loglevel=info --pool=solo
  ```

- **Terminal 5: Celery Beat**

  ```bash
  cd backend
  celery -A app.celery_app.celery beat --loglevel=info
  ```

- **Terminal 6: MailHog Server**
  ```bash
  # Linux: MailHog
  # Windows: MailHog.exe or full path if not in PATH
  ```

## Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- MailHog UI: http://localhost:8025
