# Starter Code Documentation - CircleOne

## Project Overview

CircleOne is a professional networking platform built with Flask. The starter code provides a fully functional foundation with authentication, business listings, professional profiles, and a modern UI. This document explains the codebase structure and how to work with it.

---

## Project Structure

```
Communication/
├── main.py                 # Main Flask application and routes
├── models.py              # Database models (User, BusinessListing, ProfessionalProfile)
├── config.py              # Application configuration
├── utils.py               # Utility functions (Cloudinary, image validation)
├── migrate_db.py          # Database migration script
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version specification
├── Procfile               # Railway/Heroku deployment configuration
├── railway.toml           # Railway deployment config
├── railway.json           # Railway service config
├── .env                   # Environment variables (not in repo)
├── instance/
│   └── app.db            # SQLite database file (created automatically)
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet with theme support
│   └── js/
│       ├── main.js       # Main JavaScript (theme, animations)
│       ├── forms.js      # Form handling utilities
│       ├── navigation.js # Navigation functionality
│       └── search.js     # Search functionality
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── login.html        # Login page
    ├── signup.html       # Registration page
    ├── dashboard.html    # User dashboard
    ├── profile.html      # User profile page
    ├── businesses.html   # Business directory listing
    ├── business_detail.html  # Business detail page
    ├── business_form.html    # Create/edit business form
    ├── professionals.html    # Professional directory listing
    ├── professional_detail.html  # Professional profile detail
    └── professional_form.html    # Create/edit professional profile form
```

---

## Core Components

### 1. Application Entry Point: `main.py`

**Purpose**: Central Flask application with all routes and business logic.

**Key Sections**:
- Flask app initialization (lines 12-46)
- OAuth setup (Google authentication)
- Route handlers for:
  - Authentication (`/login`, `/signup`, `/logout`, `/auth/google`)
  - User dashboard (`/dashboard`)
  - Business listings (`/businesses`, `/business/<id>`, `/dashboard/business/*`)
  - Professional profiles (`/professionals`, `/profile/<id>`, `/dashboard/profile/*`)
  - Theme API (`/api/update-theme`)

**Important Routes**:
```python
@app.route('/')                    # Home page
@app.route('/login')               # Login form
@app.route('/signup')              # Registration form
@app.route('/dashboard')           # User dashboard (protected)
@app.route('/businesses')          # Business directory
@app.route('/professionals')       # Professional directory
```

**Dependencies**:
- Flask, Flask-Login, Flask-WTF (CSRF protection)
- Authlib (OAuth)
- SQLAlchemy models from `models.py`
- Utility functions from `utils.py`

---

### 2. Database Models: `models.py`

**Purpose**: Defines all database schema and models using SQLAlchemy ORM.

#### Models:

**User Model** (`User`)
- Primary key: `id`
- Fields: `email`, `username`, `name`, `password_hash`, `oauth_provider`, `profile_photo`, `theme_preference`, `created_at`
- Relationships:
  - `businesses`: One-to-many with BusinessListing
  - `professional_profile`: One-to-one with ProfessionalProfile
- Methods: `set_password()`, `check_password()`, `to_dict()`

**BusinessListing Model** (`BusinessListing`)
- Primary key: `id`
- Foreign key: `user_id` → User
- Fields: `business_name`, `category`, `description`, `contact_email`, `phone`, `website`, `location`, `logo_url`, `hours`, `social_links` (JSON), `view_count`, `created_at`
- Methods: `get_social_links()`, `set_social_links()`, `increment_views()`, `to_dict()`

**ProfessionalProfile Model** (`ProfessionalProfile`)
- Primary key: `id`
- Foreign key: `user_id` → User (unique)
- Fields: `job_title`, `summary`, `how_i_help`, `linkedin_url`, `skills_json` (JSON array), `consent_given`, `contact_visible`, `view_count`, `created_at`
- Methods: `get_skills()`, `set_skills()`, `increment_views()`, `is_visible()`, `to_dict()`

**Database Initialization**:
- Tables are automatically created on first run via `db.create_all()` in `main.py`
- Database location: `instance/app.db` (SQLite) or `DATABASE_URL` (PostgreSQL in production)

---

### 3. Configuration: `config.py`

**Purpose**: Centralized configuration management using environment variables.

**Key Configuration**:
```python
SECRET_KEY              # Flask session secret (required)
DATABASE_URL            # Database connection string
GOOGLE_CLIENT_ID        # OAuth client ID (optional)
GOOGLE_CLIENT_SECRET    # OAuth client secret (optional)
APP_URL                 # Application URL for OAuth redirects
CLOUDINARY_CLOUD_NAME   # Cloudinary account (optional)
CLOUDINARY_API_KEY      # Cloudinary API key (optional)
CLOUDINARY_API_SECRET   # Cloudinary API secret (optional)
```

**Environment Loading**:
- Uses `python-dotenv` to load `.env` file
- Provides sensible defaults for local development
- All sensitive values should be in `.env` (not committed to git)

**Local Development**:
```env
SECRET_KEY=<generated-secret>
DATABASE_URL=sqlite:///app.db
APP_URL=http://localhost:5000
```

---

### 4. Utilities: `utils.py`

**Purpose**: Helper functions for image upload and Cloudinary integration.

**Functions**:

**`init_cloudinary()`**
- Initializes Cloudinary configuration from environment variables
- Called once at app startup

**`upload_image_to_cloudinary(file)`**
- Uploads image file to Cloudinary
- Returns tuple: `(success: bool, result: str)` where result is URL or error message
- Validates file before upload
- Handles errors gracefully

**`validate_image(file)`**
- Validates image file extension and size
- Returns `(is_valid: bool, error_message: str)`
- Checks: file extension in allowed list, file size < 5MB

---

### 5. Frontend: Templates & Static Files

#### Templates (Jinja2)

**Base Template** (`templates/base.html`)
- Provides common HTML structure
- Includes navigation bar
- Theme toggle button
- Flash message display
- CSRF token injection

**Template Hierarchy**:
```
base.html (parent)
├── index.html
├── login.html
├── signup.html
├── dashboard.html
├── profile.html
├── businesses.html
├── business_detail.html
├── business_form.html
├── professionals.html
├── professional_detail.html
└── professional_form.html
```

**Template Features**:
- Theme support via `data-theme` attribute
- Responsive design with CSS Grid and Flexbox
- Flash messages for user feedback
- CSRF protection on forms
- Conditional content based on authentication

#### Static Assets

**CSS** (`static/css/style.css`)
- CSS custom properties for theming
- Dark/light theme support
- Responsive breakpoints
- Modern animations and transitions
- Card-based layouts

**JavaScript** (`static/js/main.js`)
- Theme initialization and toggle
- Scroll animations
- Form enhancements
- Card interactions (tilt, ripple effects)
- API calls for theme updates

---

## Key Features Implementation

### 1. Authentication System

**Local Authentication**:
- Password hashing using Werkzeug (`generate_password_hash`, `check_password_hash`)
- Session management with Flask-Login
- Login with username or email
- CSRF protection on forms

**OAuth Authentication**:
- Google OAuth 2.0 via Authlib
- Automatic user creation from OAuth data
- Profile photo import from OAuth provider
- OAuth provider tracking in user record

**Session Management**:
- Flask-Login handles user sessions
- `@login_required` decorator protects routes
- Automatic redirect to login for protected pages

---

### 2. Business Directory System

**Create Business**:
- Form with validation
- Image upload via Cloudinary or URL
- Social media links stored as JSON
- Immediate availability in directory

**Search & Filter**:
- Full-text search in business name and description
- Category filtering
- Location filtering
- Results sorted by popularity (views) and date

**View Tracking**:
- Automatic view count increment
- Owner views not counted (optional enhancement)
- Statistics displayed on dashboard

---

### 3. Professional Profile System

**Profile Creation**:
- Job title, summary, skills
- Privacy controls (consent for public visibility)
- Contact information visibility toggle
- LinkedIn integration

**Skills Management**:
- Comma-separated input
- Stored as JSON array in database
- Searchable in directory
- Displayed as tags

**Visibility Control**:
- `consent_given`: Required for public directory listing
- `contact_visible`: Controls email visibility
- Owner can always view their own profile

---

### 4. Theme System

**Implementation**:
- CSS custom properties for theme variables
- JavaScript toggles `data-theme` attribute on `<html>`
- API endpoint saves preference to database
- Persistent across sessions for logged-in users

**Theme Variables**:
```css
--primary-color
--text-color
--bg-color
--card-bg
--border-color
--shadow
```

---

### 5. Image Upload System

**Cloudinary Integration**:
- Secure cloud storage for images
- Automatic image optimization
- CDN delivery
- Fallback to URL input if Cloudinary not configured

**File Validation**:
- Extension checking (PNG, JPG, JPEG, GIF, WEBP)
- File size limit (5MB)
- Error handling and user feedback

---

## Database Schema

### Users Table
```
id (PK)
email (unique, nullable)
username (unique, nullable)
name (required)
password_hash (nullable)
oauth_provider (default: 'local')
profile_photo (nullable)
theme_preference (default: 'light')
created_at (timestamp)
```

### Business Listings Table
```
id (PK)
user_id (FK → users.id)
business_name (required, indexed)
category (required, indexed)
description (nullable)
contact_email (nullable)
phone (nullable)
website (nullable)
location (nullable)
logo_url (nullable)
hours (nullable)
social_links (JSON text)
view_count (default: 0)
created_at (timestamp)
```

### Professional Profiles Table
```
id (PK)
user_id (FK → users.id, unique)
job_title (required, indexed)
summary (nullable)
how_i_help (nullable)
linkedin_url (nullable)
skills_json (JSON array text)
consent_given (default: false)
contact_visible (default: false)
view_count (default: 0)
created_at (timestamp)
```

---

## Security Features

1. **CSRF Protection**: Flask-WTF CSRF tokens on all forms
2. **Password Hashing**: Werkzeug secure password hashing
3. **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
4. **Session Security**: Flask-Login secure session management
5. **Route Protection**: `@login_required` decorator
6. **File Upload Validation**: Extension and size checking
7. **OAuth Security**: Authlib secure OAuth implementation

---

## Development Workflow

### 1. Initial Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
echo "DATABASE_URL=sqlite:///app.db" >> .env
echo "APP_URL=http://localhost:5000" >> .env

# Run application
python main.py
```

### 2. Database Management

**Automatic Creation**: Database and tables created automatically on first run.

**Manual Migration** (if needed):
```python
# In Python shell
from main import app, db
with app.app_context():
    db.create_all()
```

### 3. Adding New Features

**Example: Adding a New Route**
```python
@app.route('/new-feature')
@login_required
def new_feature():
    return render_template('new_feature.html')
```

**Example: Adding a New Model**
```python
# In models.py
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... fields

# Then create migration
# Tables auto-created on next run
```

---

## Testing the Application

### Manual Testing Checklist

**Authentication**:
- [ ] Register new account
- [ ] Login with username/email
- [ ] Login with Google OAuth (if configured)
- [ ] Logout
- [ ] Access protected routes without login

**Business Listings**:
- [ ] Create business listing
- [ ] Edit business listing
- [ ] Delete business listing
- [ ] Upload business logo
- [ ] Search businesses
- [ ] Filter by category/location

**Professional Profiles**:
- [ ] Create professional profile
- [ ] Edit professional profile
- [ ] Set visibility preferences
- [ ] Search professionals
- [ ] Filter by skills

**UI/UX**:
- [ ] Toggle dark/light theme
- [ ] Test responsive design (mobile/tablet)
- [ ] Check animations and transitions

---

## Deployment Considerations

### Environment Variables for Production

Required:
- `SECRET_KEY` (generate secure random key)
- `DATABASE_URL` (PostgreSQL recommended)
- `APP_URL` (your production domain)

Optional but Recommended:
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (for OAuth)
- `CLOUDINARY_*` variables (for image uploads)

### Railway Deployment

1. Push code to GitHub
2. Connect Railway to GitHub repo
3. Add PostgreSQL service (auto-creates `DATABASE_URL`)
4. Set environment variables in Railway dashboard
5. Deploy (automatic via `Procfile`)

---

## Common Tasks & Troubleshooting

### Issue: Database not found
**Solution**: Database auto-creates on first run. Check `instance/` folder exists.

### Issue: OAuth not working
**Solution**: Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`. Check redirect URI matches Google Console settings.

### Issue: Image upload fails
**Solution**: Verify Cloudinary credentials in `.env`, or use logo URL option instead.

### Issue: Theme not saving
**Solution**: Must be logged in for theme to save to database. Guest users use localStorage only.

### Issue: Module not found
**Solution**: Run `pip install -r requirements.txt` to install all dependencies.

---

## Next Steps & Enhancements

### Critical Missing Features:
1. **User Connections System**: Add ability for users to connect with each other
2. **Messaging System**: Implement in-app messaging between users
3. **Network Display**: Show user's network/connections in dashboard

### Suggested Enhancements:
1. Email notifications for connection requests
2. Activity feed
3. Advanced analytics dashboard
4. Profile recommendations
5. Export functionality for listings
6. Email verification
7. Password reset functionality
8. Admin panel for user management

---

## Code Conventions

- **Python**: PEP 8 style guide
- **Templates**: Jinja2 with clear separation of logic
- **JavaScript**: ES6+ with comments for complex logic
- **CSS**: BEM-inspired naming with custom properties
- **Database**: SQLAlchemy ORM (no raw SQL)

---

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Jinja2 Templates**: https://jinja.palletsprojects.com/
- **Authlib OAuth**: https://docs.authlib.org/

---

*Last Updated: 2024*

