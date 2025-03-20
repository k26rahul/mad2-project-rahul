# Quiz Master V2 - Full Specification

## **1. Overview**

Quiz Master V2 is a multi-user exam preparation application designed to manage and attempt quizzes across multiple subjects. The platform supports two roles: **Admin (Quiz Master)** and **Users (Students)**.

## **2. Technology Stack**

### **Backend**

- **Flask** – REST API
- **SQLite** – Database
- **Redis** – Caching
- **Celery + Redis** – Background jobs
- **Flask-Security** – Role-based access control (RBAC), no HTML features

### **Frontend**

- **Vue.js (Options API)** – UI
- **Bootstrap** – Styling (no other CSS framework allowed)
- **Vite** – Build tool

### **Others**

- **Google Chat Webhooks / Email** – User notifications
- **CSV Export** – Quiz reports
- **Jinja2** – Used only for the entry point (not for UI)

## **3. User Roles & Authentication**

### **Admin (Quiz Master)**

- **Single admin user** (hardcoded at database initialization, cannot be registered)
- Full control over users, subjects, chapters, quizzes, and reports
- Can log in but not register

### **Users (Students)**

- Can **register and log in**
- Can attempt quizzes
- Can view their scores and history
- Can export quiz results as CSV

### **Authentication System**

- Flask-based authentication
- Session-based login/logout
- Admin login redirects to admin dashboard
- User login redirects to user dashboard

## **4. Data Models**

### **User Model**

- `id` (PK)
- `email` (unique, used as username)
- `password` (hashed)
- `full_name`
- `qualification`
- `dob`
- `role` (admin/user)

### **Subject Model**

- `id` (PK)
- `name`
- `description`

### **Chapter Model**

- `id` (PK)
- `subject_id` (FK to Subject)
- `name`
- `description`

### **Quiz Model**

- `id` (PK)
- `chapter_id` (FK to Chapter)
- `date_of_quiz`
- `time_duration` (hh:mm)
- `remarks`

### **Question Model**

- `id` (PK)
- `quiz_id` (FK to Quiz)
- `question_statement`
- `option1`
- `option2`
- `option3`
- `option4`
- `correct_option`

### **Score Model**

- `id` (PK)
- `quiz_id` (FK to Quiz)
- `user_id` (FK to User)
- `time_stamp_of_attempt`
- `total_scored`

## **5. Features**

### **5.1 Admin Features**

#### **Admin Dashboard**

- View summary reports and statistics
- Manage subjects, chapters, quizzes, and users

#### **Subject Management**

- Create/Edit/Delete subjects

#### **Chapter Management**

- Create/Edit/Delete chapters under subjects

#### **Quiz Management**

- Create/Edit/Delete quizzes under chapters
- Specify **date** and **duration**
- Manage **MCQ questions (only one correct option)**
- Search quizzes by **name, chapter, or subject**

#### **User Management**

- View/search user details

#### **Reports & Exports**

- View summary statistics (charts, tables)
- Export all quiz-related data as CSV

### **5.2 User Features**

#### **User Dashboard**

- View available subjects & chapters
- View history of attempted quizzes

#### **Quiz Participation**

- Choose subject → chapter → quiz
- Start the quiz with a **countdown timer**
- Submit answers
- View **quiz result** immediately

#### **Reports & Exports**

- View past quiz attempts
- Export personal quiz history as CSV

## **6. API Endpoints**

### **6.1 Authentication**

- `POST /auth/login` – Login
- `POST /auth/logout` – Logout
- `POST /auth/register` – Register (users only)

### **6.2 Admin Routes (`/admin/*`)**

- `GET /admin/dashboard` – View admin dashboard
- `GET /admin/subjects` – List subjects
- `POST /admin/subjects` – Create a subject
- `PUT /admin/subjects/:id` – Update a subject
- `DELETE /admin/subjects/:id` – Delete a subject
- `GET /admin/chapters` – List chapters
- `POST /admin/chapters` – Create a chapter
- `PUT /admin/chapters/:id` – Update a chapter
- `DELETE /admin/chapters/:id` – Delete a chapter
- `GET /admin/quizzes` – List quizzes
- `POST /admin/quizzes` – Create a quiz
- `PUT /admin/quizzes/:id` – Update a quiz
- `DELETE /admin/quizzes/:id` – Delete a quiz
- `GET /admin/questions` – List questions
- `POST /admin/questions` – Create a question
- `PUT /admin/questions/:id` – Update a question
- `DELETE /admin/questions/:id` – Delete a question
- `GET /admin/reports` – View reports
- `GET /admin/reports/export` – Export data as CSV

### **6.3 User Routes (`/user/*`)**

- `GET /user/dashboard` – View user dashboard
- `GET /user/subjects` – List subjects
- `GET /user/chapters` – List chapters
- `GET /user/quizzes` – List quizzes
- `GET /user/quizzes/:id/start` – Start a quiz
- `POST /user/quizzes/:id/submit` – Submit quiz
- `GET /user/quizzes/:id/result` – View quiz result
- `GET /user/history` – View past attempts
- `GET /user/profile` – View user profile
- `PUT /user/profile` – Update user profile
- `GET /user/reports/export` – Export user quiz history as CSV

## **7. Background Jobs (Celery + Redis)**

### **7.1 Scheduled Jobs**

- **Daily Reminder** – Notify users of new quizzes
- **Monthly Report** – Email quiz statistics to users

### **7.2 User-Triggered Jobs**

- **Export User Quiz Data (CSV)** – Generates and emails quiz history
- **Export Admin Quiz Data (CSV)** – Admin can download all quiz statistics

## **8. Frontend Routes (Vue.js)**

### **Auth Routes**

- `/login`, `/register`, `/logout`

### **Admin Routes (`/admin/*`)**

- `/admin/dashboard`, `/admin/subjects`, `/admin/quizzes`, `/admin/reports`

### **User Routes (`/user/*`)**

- `/user/dashboard`, `/user/quizzes`, `/user/history`, `/user/profile`

## **9. Performance & Caching**

- Use **Redis** for caching quiz data
- Expire cache periodically for freshness

## **10. Optional Enhancements**

- PDF reports for **monthly activity summaries**
- **Charts.js** for visual statistics
- Responsive UI for **desktop & mobile**
- Form validation with **HTML5 & JavaScript**
