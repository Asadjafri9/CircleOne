from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)  # Nullable for username login
    username = db.Column(db.String(80), unique=True, nullable=True, index=True)  # For username/password login
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # For username/password login
    oauth_provider = db.Column(db.String(50), nullable=False, default='local')  # 'google', 'microsoft', 'local', or 'test'
    profile_photo = db.Column(db.String(500), nullable=True)
    theme_preference = db.Column(db.String(20), default='light')  # 'light' or 'dark'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    businesses = db.relationship('BusinessListing', backref='owner', lazy=True, cascade='all, delete-orphan')
    professional_profile = db.relationship('ProfessionalProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email or self.username}>'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'oauth_provider': self.oauth_provider,
            'profile_photo': self.profile_photo,
            'theme_preference': self.theme_preference,
            'created_at': self.created_at.isoformat()
        }


class BusinessListing(db.Model):
    """Business listing model for directory"""
    __tablename__ = 'business_listings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    business_name = db.Column(db.String(255), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(500), nullable=True)
    logo_url = db.Column(db.String(500), nullable=True)
    hours = db.Column(db.String(500), nullable=True)
    social_links = db.Column(db.Text, nullable=True)  # JSON stored as text
    view_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<BusinessListing {self.business_name}>'
    
    def get_social_links(self):
        """Parse social_links JSON string to dictionary"""
        if self.social_links:
            try:
                return json.loads(self.social_links)
            except:
                return {}
        return {}
    
    def set_social_links(self, links_dict):
        """Convert dictionary to JSON string for storage"""
        if links_dict:
            self.social_links = json.dumps(links_dict)
        else:
            self.social_links = None
    
    def increment_views(self):
        """Increment view counter"""
        self.view_count += 1
        db.session.commit()
    
    def to_dict(self):
        """Convert business listing to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'category': self.category,
            'description': self.description,
            'contact_email': self.contact_email,
            'phone': self.phone,
            'website': self.website,
            'location': self.location,
            'logo_url': self.logo_url,
            'hours': self.hours,
            'social_links': self.get_social_links(),
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat(),
            'owner_name': self.owner.name if self.owner else None
        }


class ProfessionalProfile(db.Model):
    """Professional profile model for directory"""
    __tablename__ = 'professional_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    job_title = db.Column(db.String(255), nullable=False, index=True)
    summary = db.Column(db.Text, nullable=True)
    how_i_help = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.String(500), nullable=True)
    skills_json = db.Column(db.Text, nullable=True)  # JSON array of skills
    consent_given = db.Column(db.Boolean, default=False, nullable=False)
    contact_visible = db.Column(db.Boolean, default=False, nullable=False)
    view_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ProfessionalProfile {self.user.name if self.user else "Unknown"}>'
    
    def get_skills(self):
        """Parse skills JSON string to list"""
        if self.skills_json:
            try:
                return json.loads(self.skills_json)
            except:
                return []
        return []
    
    def set_skills(self, skills_list):
        """Convert list to JSON string for storage"""
        if skills_list:
            self.skills_json = json.dumps(skills_list)
        else:
            self.skills_json = None
    
    def increment_views(self):
        """Increment view counter"""
        self.view_count += 1
        db.session.commit()
    
    def is_visible(self):
        """Check if profile should be visible in directory"""
        return self.consent_given
    
    def to_dict(self):
        """Convert professional profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name if self.user else None,
            'email': self.user.email if self.user and self.contact_visible else None,
            'profile_photo': self.user.profile_photo if self.user else None,
            'job_title': self.job_title,
            'summary': self.summary,
            'how_i_help': self.how_i_help,
            'linkedin_url': self.linkedin_url,
            'skills': self.get_skills(),
            'consent_given': self.consent_given,
            'contact_visible': self.contact_visible,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat()
        }
