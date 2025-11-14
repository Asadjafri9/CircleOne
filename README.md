# CircleOne
## Deployed Link: https://onecircle-production.up.railway.app/
## Video Demo 
https://drive.google.com/drive/folders/1xktB6MsheeWi3yli7qk81E4gxa0AqI6B?usp=sharing

A modern Flask web application with OAuth 2.0 authentication, business directory, and professional profiles.

## Features

- 🔐 OAuth 2.0 Authentication (Google)
- 💼 Business Directory
- 👥 Professional Profiles
- 🎨 Dark/Light Theme Support
- 📱 Responsive Design
- ✨ Interactive UI with Animations
  
## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
APP_URL=http://localhost:5000
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 3. Run the Application

```bash
python main.py
```

Visit `http://127.0.0.1:5000/` in your browser.

## Deployment on Railway

### Deploy to Railway.app

1. **Push to GitHub**: Push this repository to GitHub

2. **Connect to Railway**:
   - Go to [Railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment Variables** in Railway:
   - `SECRET_KEY` - A random secret key (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URL` - Railway will auto-provision PostgreSQL (automatically set if you add a PostgreSQL service)
   - `GOOGLE_CLIENT_ID` - Your Google OAuth Client ID
   - `GOOGLE_CLIENT_SECRET` - Your Google OAuth Client Secret
   - `APP_URL` - Your Railway app URL (e.g., `https://your-app.railway.app`)
   - `CLOUDINARY_CLOUD_NAME` - Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY` - Your Cloudinary API key
   - `CLOUDINARY_API_SECRET` - Your Cloudinary API secret

4. **Update Google OAuth Redirect URI**:
   - Add your Railway URL to Google OAuth settings: `https://your-app.railway.app/auth/google/callback`

5. **Deploy**: Railway will automatically detect Python and deploy using the `Procfile`

The app will be live at your Railway domain!

## Technologies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Authlib 1.3.0
- Cloudinary 1.36.0

## Database

Uses SQLite by default. Database file: `instance/app.db`

## Documentation

This repository includes comprehensive documentation:

- **[USER_STORIES.md](USER_STORIES.md)** - Complete user stories, epics, and feature breakdown
- **[STARTER_CODE.md](STARTER_CODE.md)** - Detailed starter code documentation and architecture guide

### Quick Links

- **User Stories & Epics**: See [USER_STORIES.md](USER_STORIES.md) for all features, user stories, acceptance criteria, and implementation status
- **Starter Code Guide**: See [STARTER_CODE.md](STARTER_CODE.md) for code structure, models, routes, and development workflow
