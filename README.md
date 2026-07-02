# perpend

`perpend` is an interactive learning roadmap tracker built with a Django (REST Framework) backend and a React frontend. It allows users to view structured roadmaps, double-click topics to mark them as completed/incomplete, and persist progress in a PostgreSQL database.

---

## 🏛️ Project Architecture

This repository is organized as a monorepo containing two main parts:

- **`app/` (React Frontend)**: A modern, responsive React Single Page Application that handles user authentication and displays the interactive roadmap grid.
- **`core/` (Django Backend)**: A Django REST Framework API that handles database interactions (PostgreSQL via Neon), user authentication (SimpleJWT), and roadmap data queries.

---

## ✨ Features

- **Interactive Roadmap Grid**: Clean, responsive layout showcasing subtopics colored with dynamic contrast text.
- **Progress Tracking**: Double-click any subtopic card to toggle its completion state. Progress is instantly saved to the database.
- **JWT Authentication**: Secure user registration/login flow using JWT access and refresh tokens.
- **Stateless Vercel Deployment**: Fully configured for zero-downtime hosting on Vercel's serverless infrastructure.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**
- **PostgreSQL** (local or cloud-hosted like Neon)

---

### 🔧 1. Backend Setup (`core/`)

1. Navigate to the backend directory:
   ```bash
   cd core
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `core/` directory and add your database configuration:
   ```env
   DATABASE_URL="postgresql://user:password@host:port/dbname?sslmode=require"
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser to access the admin portal:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the local Django server:
   ```bash
   python manage.py runserver
   ```
   *The backend will run on `http://localhost:8000`.*

---

### 🎨 2. Frontend Setup (`app/`)

1. Navigate to the frontend directory:
   ```bash
   cd ../app
   ```

2. Install the node packages:
   ```bash
   npm install
   ```

3. Create a `.env` file in the `app/` directory and configure the API endpoint:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the frontend React development server:
   ```bash
   npm start
   ```
   *The frontend will run on `http://localhost:3000`.*

---

## ☁️ Deployment (Vercel)

Both frontend and backend are deployed as separate Vercel projects pointing to the same repository.

### Backend Project Configuration
- **Root Directory**: `core`
- **Build Command**: None (handled automatically by Vercel's Python runtime)
- **Output Directory**: None
- **Environment Variables**:
  - `DATABASE_URL`: Your PostgreSQL connection string.

### Frontend Project Configuration
- **Root Directory**: `app`
- **Framework Preset**: Create React App
- **Environment Variables**:
  - `REACT_APP_API_URL`: The URL of your deployed Vercel backend project (e.g. `https://perpend.vercel.app`).
