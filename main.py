from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.flask_client import OAuth
from config import Config
from models import db, User, BusinessListing, ProfessionalProfile
from utils import init_cloudinary, upload_image_to_cloudinary, validate_image
import os
import json

app = Flask(__name__)
app.config.from_object(Config)
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize CSRF Protection
csrf = CSRFProtect(app)

# Initialize Cloudinary
with app.app_context():
    init_cloudinary()

# Initialize OAuth
oauth = OAuth(app)

# Google OAuth Configuration
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Home page"""
    # Get actual counts from database
    total_members = User.query.count()
    total_businesses = BusinessListing.query.count()
    
    return render_template('index.html', 
                          total_members=total_members,
                          total_businesses=total_businesses)


@app.route('/check-oauth')
def check_oauth():
    """Check if OAuth is configured correctly"""
    google_configured = bool(app.config.get('GOOGLE_CLIENT_ID')) and app.config.get(
        'GOOGLE_CLIENT_ID') != 'your-google-client-id'

    return f"""
    <html>
    <head><title>Google OAuth Status</title></head>
    <body style="font-family: Arial; padding: 40px; max-width: 800px; margin: 0 auto;">
        <h1>🔐 Google OAuth Configuration</h1>
        
        <div style="background: {'#d4edda' if google_configured else '#f8d7da'}; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2 style="margin-top: 0;">Status: {'✅ CONFIGURED' if google_configured else '❌ NOT CONFIGURED'}</h2>
            <p><strong>Client ID:</strong> {app.config.get('GOOGLE_CLIENT_ID', 'NOT SET')}</p>
            <p><strong>Redirect URI:</strong> {app.config['APP_URL']}/auth/google/callback</p>
        </div>
        
        <hr>
        
        {'<div style="background: #d4edda; padding: 20px; border-radius: 8px;"><h3>✅ Ready to Go!</h3><p>Your Google OAuth is properly configured.</p><p><a href="/login" style="background: #4285f4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin-top: 10px;">Test Login Now →</a></p></div>' if google_configured else '<div style="background: #f8d7da; padding: 20px; border-radius: 8px;"><h3>❌ Configuration Missing</h3><p>Please add your Google OAuth credentials to the .env file and restart the server.</p></div>'}
        
        <p style="margin-top: 30px;"><a href="/">← Back to Home</a> | <a href="/login">Login Page →</a></p>
    </body>
    </html>
    """


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        
        if not username_or_email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))
        
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/email or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not name or not password:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('signup'))
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'error')
            return redirect(url_for('signup'))
        
        # Check if email already exists (if provided)
        if email and User.query.filter_by(email=email).first():
            flash('Email already exists. Please use another or login.', 'error')
            return redirect(url_for('signup'))
        
        # Create new user
        # For SQLite compatibility, use placeholder email if none provided
        user_email = email if email else f'{username}@circleone.local'
        
        new_user = User(
            username=username,
            name=name,
            email=user_email,
            oauth_provider='local',
            profile_photo=f'https://ui-avatars.com/api/?name={name.replace(" ", "+")}&background=4285f4&color=fff',
            theme_preference='light'
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f'Welcome to CircleOne, {name}! Your account has been created.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')


@app.route('/auth/test-login', methods=['GET', 'POST'])
def test_login():
    """Development test login (bypasses OAuth)"""
    # If already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Create or get test user
    test_user = User.query.filter_by(email='test@example.com').first()
    if not test_user:
        test_user = User(
            email='test@example.com',
            name='Test User',
            oauth_provider='test',
            profile_photo='https://ui-avatars.com/api/?name=Test+User&background=4285f4&color=fff',
            theme_preference='light'
        )
        db.session.add(test_user)
        db.session.commit()

    login_user(test_user)
    flash('Logged in as Test User (Development Mode)', 'success')
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - requires authentication"""
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    logout_user()
    return redirect(url_for('index'))

# Google OAuth routes


@app.route('/auth/google')
def google_login():
    redirect_uri = f"{app.config['APP_URL']}/auth/google/callback"
    print("DEBUG REDIRECT URI:", redirect_uri)
    # Force Google to show account selection screen
    return google.authorize_redirect(
        redirect_uri,
        prompt='select_account'  # This allows choosing different accounts
    )


@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')

        if not user_info:
            flash('Failed to get user information from Google', 'error')
            return redirect(url_for('login'))

        email = user_info.get('email')
        name = user_info.get('name')
        profile_photo = user_info.get('picture')

        if not email:
            flash('Failed to get email from Google', 'error')
            return redirect(url_for('login'))

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        if not user:
            # Create new user
            user = User(
                email=email,
                name=name,
                oauth_provider='google',
                profile_photo=profile_photo
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {name}! Your account has been created.', 'success')
        else:
            # Update existing user info
            user.name = name
            user.profile_photo = profile_photo
            user.oauth_provider = 'google'
            db.session.commit()
            flash(f'Welcome back, {name}!', 'success')

        # Log in the user
        login_user(user)
        return redirect(url_for('dashboard'))
    except Exception as e:
        error_msg = str(e)
        print(f"Error during Google OAuth: {error_msg}")
        flash(f'Google login failed: {error_msg}', 'error')
        return redirect(url_for('login'))


# API route for updating theme preference
@app.route('/api/update-theme', methods=['POST'])
@login_required
def update_theme():
    """Update user's theme preference"""
    data = request.get_json()
    theme = data.get('theme', 'light')

    if theme in ['light', 'dark']:
        current_user.theme_preference = theme
        db.session.commit()
        return {'success': True, 'theme': theme}

    return {'success': False, 'error': 'Invalid theme'}, 400


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

# Business Directory Routes


@app.route('/businesses')
def businesses():
    """Business directory with search and filter"""
    # Get query parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')

    # Build query
    query = BusinessListing.query

    if search:
        query = query.filter(
            (BusinessListing.business_name.ilike(f'%{search}%')) |
            (BusinessListing.description.ilike(f'%{search}%'))
        )

    if category:
        query = query.filter(BusinessListing.category == category)

    if location:
        query = query.filter(BusinessListing.location.ilike(f'%{location}%'))

    # Order by view count and created date
    listings = query.order_by(
        BusinessListing.view_count.desc(), BusinessListing.created_at.desc()).all()

    # Get all unique categories for filter
    categories = db.session.query(BusinessListing.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('businesses.html',
                           listings=listings,
                           categories=categories,
                           search=search,
                           selected_category=category,
                           selected_location=location)


@app.route('/business/<int:id>')
def business_detail(id):
    """Business detail page with view counter"""
    business = BusinessListing.query.get_or_404(id)

    # Increment view count
    business.increment_views()

    # Check if current user is the owner
    is_owner = current_user.is_authenticated and business.user_id == current_user.id

    return render_template('business_detail.html', business=business, is_owner=is_owner)


@app.route('/dashboard/business/new', methods=['GET', 'POST'])
@login_required
def create_business():
    """Create new business listing"""
    if request.method == 'POST':
        try:
            # Get form data
            business_name = request.form.get('business_name')
            category = request.form.get('category')
            description = request.form.get('description')
            contact_email = request.form.get('contact_email')
            phone = request.form.get('phone')
            website = request.form.get('website')
            location = request.form.get('location')
            hours = request.form.get('hours')

            # Handle logo upload or URL
            logo_url = None

            # Check if file was uploaded
            if 'logo_file' in request.files:
                file = request.files['logo_file']
                if file and file.filename != '':
                    # Upload to Cloudinary
                    success, result = upload_image_to_cloudinary(file)
                    if success:
                        logo_url = result
                    else:
                        flash(f'Image upload failed: {result}', 'error')
                        return redirect(url_for('create_business'))

            # If no file uploaded, check for URL input
            if not logo_url:
                logo_url = request.form.get('logo_url')

            # Handle social links
            social_links = {
                'facebook': request.form.get('facebook', ''),
                'twitter': request.form.get('twitter', ''),
                'instagram': request.form.get('instagram', ''),
                'linkedin': request.form.get('linkedin', '')
            }
            # Remove empty social links
            social_links = {k: v for k, v in social_links.items() if v}

            # Create business listing
            business = BusinessListing(
                user_id=current_user.id,
                business_name=business_name,
                category=category,
                description=description,
                contact_email=contact_email,
                phone=phone,
                website=website,
                location=location,
                logo_url=logo_url,
                hours=hours
            )
            business.set_social_links(social_links)

            db.session.add(business)
            db.session.commit()

            flash('Business listing created successfully!', 'success')
            return redirect(url_for('business_detail', id=business.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating business listing: {str(e)}', 'error')
            return redirect(url_for('create_business'))

    return render_template('business_form.html', business=None, mode='create')


@app.route('/dashboard/business/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_business(id):
    """Edit existing business listing"""
    business = BusinessListing.query.get_or_404(id)

    # Check if user owns this business
    if business.user_id != current_user.id:
        flash('You do not have permission to edit this business.', 'error')
        return redirect(url_for('businesses'))

    if request.method == 'POST':
        try:
            # Update business data
            business.business_name = request.form.get('business_name')
            business.category = request.form.get('category')
            business.description = request.form.get('description')
            business.contact_email = request.form.get('contact_email')
            business.phone = request.form.get('phone')
            business.website = request.form.get('website')
            business.location = request.form.get('location')
            business.hours = request.form.get('hours')

            # Handle logo upload or URL
            # Check if file was uploaded
            if 'logo_file' in request.files:
                file = request.files['logo_file']
                if file and file.filename != '':
                    # Upload new image to Cloudinary
                    success, result = upload_image_to_cloudinary(file)
                    if success:
                        business.logo_url = result
                    else:
                        flash(f'Image upload failed: {result}', 'error')
                        return redirect(url_for('edit_business', id=id))

            # If no file uploaded, check if URL was updated
            if 'logo_file' not in request.files or not request.files['logo_file'].filename:
                url_input = request.form.get('logo_url')
                if url_input:
                    business.logo_url = url_input

            # Handle social links
            social_links = {
                'facebook': request.form.get('facebook', ''),
                'twitter': request.form.get('twitter', ''),
                'instagram': request.form.get('instagram', ''),
                'linkedin': request.form.get('linkedin', '')
            }
            # Remove empty social links
            social_links = {k: v for k, v in social_links.items() if v}
            business.set_social_links(social_links)

            db.session.commit()

            flash('Business listing updated successfully!', 'success')
            return redirect(url_for('business_detail', id=business.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating business listing: {str(e)}', 'error')
            return redirect(url_for('edit_business', id=id))

    return render_template('business_form.html', business=business, mode='edit')


@app.route('/dashboard/business/delete/<int:id>', methods=['POST'])
@login_required
def delete_business(id):
    """Delete business listing"""
    business = BusinessListing.query.get_or_404(id)

    # Check if user owns this business
    if business.user_id != current_user.id:
        flash('You do not have permission to delete this business.', 'error')
        return redirect(url_for('businesses'))

    try:
        db.session.delete(business)
        db.session.commit()
        flash('Business listing deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting business listing: {str(e)}', 'error')

    return redirect(url_for('dashboard'))

# Professional Directory Routes


@app.route('/professionals')
def professionals():
    """Professional directory page"""
    # Get query parameters
    search = request.args.get('search', '')
    skill = request.args.get('skill', '')

    # Build query - only show profiles with consent
    query = ProfessionalProfile.query.filter_by(consent_given=True)

    if search:
        query = query.join(User).filter(
            (User.name.ilike(f'%{search}%')) |
            (ProfessionalProfile.job_title.ilike(f'%{search}%')) |
            (ProfessionalProfile.summary.ilike(f'%{search}%'))
        )

    if skill:
        # Search for skill in JSON array
        query = query.filter(
            ProfessionalProfile.skills_json.ilike(f'%{skill}%'))

    # Order by view count and created date
    profiles = query.order_by(ProfessionalProfile.view_count.desc(),
                              ProfessionalProfile.created_at.desc()).all()

    # Get all unique skills for filter
    all_profiles = ProfessionalProfile.query.filter_by(
        consent_given=True).all()
    skills_set = set()
    for profile in all_profiles:
        skills_set.update(profile.get_skills())
    skills = sorted(list(skills_set))

    return render_template('professionals.html',
                           profiles=profiles,
                           skills=skills,
                           search=search,
                           selected_skill=skill)


@app.route('/profile/<int:id>')
def professional_profile(id):
    """Professional profile detail page with view counter"""
    profile = ProfessionalProfile.query.get_or_404(id)

    # Check if profile is visible
    if not profile.is_visible():
        # Only owner can view non-consented profiles
        if not current_user.is_authenticated or profile.user_id != current_user.id:
            flash('This profile is not publicly visible.', 'error')
            return redirect(url_for('professionals'))

    # Increment view count (only if not owner and profile is visible)
    if current_user.is_authenticated and profile.user_id != current_user.id:
        profile.increment_views()
    elif not current_user.is_authenticated and profile.is_visible():
        profile.increment_views()

    # Check if current user is the owner
    is_owner = current_user.is_authenticated and profile.user_id == current_user.id

    return render_template('professional_detail.html', profile=profile, is_owner=is_owner)


@app.route('/dashboard/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_professional_profile():
    """Edit professional profile"""
    # Get or create profile
    profile = ProfessionalProfile.query.filter_by(
        user_id=current_user.id).first()

    if request.method == 'POST':
        try:
            job_title = request.form.get('job_title')
            summary = request.form.get('summary')
            how_i_help = request.form.get('how_i_help')
            linkedin_url = request.form.get('linkedin_url')
            consent_given = request.form.get('consent_given') == 'on'
            contact_visible = request.form.get('contact_visible') == 'on'

            # Handle skills (comma-separated input)
            skills_input = request.form.get('skills', '')
            skills_list = [s.strip()
                           for s in skills_input.split(',') if s.strip()]

            if profile:
                # Update existing profile
                profile.job_title = job_title
                profile.summary = summary
                profile.how_i_help = how_i_help
                profile.linkedin_url = linkedin_url
                profile.consent_given = consent_given
                profile.contact_visible = contact_visible
                profile.set_skills(skills_list)
            else:
                # Create new profile
                profile = ProfessionalProfile(
                    user_id=current_user.id,
                    job_title=job_title,
                    summary=summary,
                    how_i_help=how_i_help,
                    linkedin_url=linkedin_url,
                    consent_given=consent_given,
                    contact_visible=contact_visible
                )
                profile.set_skills(skills_list)
                db.session.add(profile)

            db.session.commit()

            flash('Professional profile updated successfully!', 'success')
            return redirect(url_for('professional_profile', id=profile.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating professional profile: {str(e)}', 'error')
            return redirect(url_for('edit_professional_profile'))

    return render_template('professional_form.html', profile=profile)


@app.route('/dashboard/profile/delete', methods=['POST'])
@login_required
def delete_professional_profile():
    """Delete professional profile"""
    profile = ProfessionalProfile.query.filter_by(
        user_id=current_user.id).first()

    if not profile:
        flash('No profile to delete.', 'error')
        return redirect(url_for('dashboard'))

    try:
        db.session.delete(profile)
        db.session.commit()
        flash('Professional profile deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting professional profile: {str(e)}', 'error')

    return redirect(url_for('dashboard'))


# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Get port from environment variable (Railway/Heroku) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode in production (Railway sets RAILWAY_ENVIRONMENT)
    debug_mode = os.environ.get('RAILWAY_ENVIRONMENT') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
