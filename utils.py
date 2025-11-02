import cloudinary
import cloudinary.uploader
from flask import current_app
from werkzeug.utils import secure_filename
import os

def init_cloudinary():
    """Initialize Cloudinary with configuration"""
    cloudinary.config(
        cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=current_app.config['CLOUDINARY_API_KEY'],
        api_secret=current_app.config['CLOUDINARY_API_SECRET']
    )

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validate_image(file):
    """
    Validate image file
    Returns: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        allowed = ', '.join(current_app.config['ALLOWED_EXTENSIONS'])
        return False, f"Invalid file type. Allowed types: {allowed}"
    
    # Check file size (Flask's MAX_CONTENT_LENGTH handles this at request level)
    # But we can do an additional check here if needed
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    if file_size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        return False, f"File too large. Maximum size: {max_size_mb}MB"
    
    return True, None

def upload_image_to_cloudinary(file, folder="business_logos"):
    """
    Upload image to Cloudinary
    Returns: (success, url_or_error)
    """
    try:
        # Validate file
        is_valid, error = validate_image(file)
        if not is_valid:
            return False, error
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image",
            transformation=[
                {'width': 800, 'height': 800, 'crop': 'limit'},
                {'quality': 'auto:good'},
                {'fetch_format': 'auto'}
            ]
        )
        
        # Return the secure URL
        return True, result['secure_url']
    
    except cloudinary.exceptions.Error as e:
        return False, f"Cloudinary error: {str(e)}"
    except Exception as e:
        return False, f"Upload error: {str(e)}"

def delete_image_from_cloudinary(public_id):
    """
    Delete image from Cloudinary
    Returns: (success, message)
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result.get('result') == 'ok':
            return True, "Image deleted successfully"
        return False, "Failed to delete image"
    except Exception as e:
        return False, f"Delete error: {str(e)}"

def extract_public_id_from_url(cloudinary_url):
    """
    Extract public_id from Cloudinary URL
    Example: https://res.cloudinary.com/demo/image/upload/v1234567890/folder/image.jpg
    Returns: folder/image
    """
    if not cloudinary_url or 'cloudinary.com' not in cloudinary_url:
        return None
    
    try:
        # Split URL and get the path after 'upload/'
        parts = cloudinary_url.split('/upload/')
        if len(parts) < 2:
            return None
        
        # Get everything after version number (v1234567890/)
        path_parts = parts[1].split('/')
        if len(path_parts) < 2:
            return None
        
        # Remove version and extension
        public_id_parts = path_parts[1:]
        public_id = '/'.join(public_id_parts)
        
        # Remove file extension
        if '.' in public_id:
            public_id = public_id.rsplit('.', 1)[0]
        
        return public_id
    except:
        return None
