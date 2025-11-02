// Form Validation and Loading States

class FormValidator {
    constructor(formSelector) {
        this.form = document.querySelector(formSelector);
        if (!this.form) return;
        
        this.submitButton = this.form.querySelector('button[type="submit"]');
        this.init();
    }
    
    init() {
        // Add event listener for form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Add real-time validation
        const inputs = this.form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
        
        // Add email validation
        const emailInputs = this.form.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.addEventListener('blur', () => this.validateEmail(input));
        });
        
        // Add URL validation
        const urlInputs = this.form.querySelectorAll('input[type="url"]');
        urlInputs.forEach(input => {
            input.addEventListener('blur', () => this.validateURL(input));
        });
    }
    
    handleSubmit(e) {
        // Validate all fields
        const isValid = this.validateForm();
        
        if (!isValid) {
            e.preventDefault();
            this.showFormError('Please fix the errors before submitting.');
            return;
        }
        
        // Show loading state
        this.showLoading();
    }
    
    validateForm() {
        let isValid = true;
        const requiredFields = this.form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    validateField(field) {
        const value = field.value.trim();
        
        // Check if required field is empty
        if (field.hasAttribute('required') && !value) {
            this.showFieldError(field, 'This field is required.');
            return false;
        }
        
        // Check minimum length
        if (field.hasAttribute('minlength')) {
            const minLength = parseInt(field.getAttribute('minlength'));
            if (value.length < minLength) {
                this.showFieldError(field, `Minimum ${minLength} characters required.`);
                return false;
            }
        }
        
        // Check maximum length
        if (field.hasAttribute('maxlength')) {
            const maxLength = parseInt(field.getAttribute('maxlength'));
            if (value.length > maxLength) {
                this.showFieldError(field, `Maximum ${maxLength} characters allowed.`);
                return false;
            }
        }
        
        this.clearFieldError(field);
        return true;
    }
    
    validateEmail(input) {
        const value = input.value.trim();
        if (!value) return true;
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            this.showFieldError(input, 'Please enter a valid email address.');
            return false;
        }
        
        this.clearFieldError(input);
        return true;
    }
    
    validateURL(input) {
        const value = input.value.trim();
        if (!value) return true;
        
        try {
            new URL(value);
            this.clearFieldError(input);
            return true;
        } catch {
            this.showFieldError(input, 'Please enter a valid URL (e.g., https://example.com).');
            return false;
        }
    }
    
    showFieldError(field, message) {
        // Remove existing error
        this.clearFieldError(field);
        
        // Add error class
        field.classList.add('input-error');
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error-message';
        errorDiv.textContent = message;
        
        // Insert after field
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    clearFieldError(field) {
        field.classList.remove('input-error');
        
        const errorMessage = field.parentNode.querySelector('.field-error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
    
    showFormError(message) {
        // Remove existing form error
        const existingError = this.form.querySelector('.form-error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error-message';
        errorDiv.innerHTML = `
            <span class="error-icon">⚠️</span>
            <span>${message}</span>
        `;
        
        // Insert at top of form
        this.form.insertBefore(errorDiv, this.form.firstChild);
        
        // Scroll to error
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    showLoading() {
        if (!this.submitButton) return;
        
        // Disable button
        this.submitButton.disabled = true;
        
        // Save original text
        this.submitButton.dataset.originalText = this.submitButton.textContent;
        
        // Add loading state
        this.submitButton.classList.add('btn-loading');
        this.submitButton.innerHTML = `
            <span class="spinner"></span>
            <span>Processing...</span>
        `;
    }
    
    hideLoading() {
        if (!this.submitButton) return;
        
        // Enable button
        this.submitButton.disabled = false;
        
        // Remove loading state
        this.submitButton.classList.remove('btn-loading');
        
        // Restore original text
        if (this.submitButton.dataset.originalText) {
            this.submitButton.textContent = this.submitButton.dataset.originalText;
        }
    }
}

// File upload validation
class FileUploadValidator {
    constructor(inputSelector, options = {}) {
        this.input = document.querySelector(inputSelector);
        if (!this.input) return;
        
        this.options = {
            maxSize: options.maxSize || 5 * 1024 * 1024, // 5MB default
            allowedTypes: options.allowedTypes || ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'],
            ...options
        };
        
        this.init();
    }
    
    init() {
        this.input.addEventListener('change', (e) => this.validateFile(e));
    }
    
    validateFile(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        // Check file size
        if (file.size > this.options.maxSize) {
            const maxSizeMB = this.options.maxSize / (1024 * 1024);
            this.showError(`File is too large. Maximum size is ${maxSizeMB}MB.`);
            e.target.value = '';
            return false;
        }
        
        // Check file type
        if (!this.options.allowedTypes.includes(file.type)) {
            const allowed = this.options.allowedTypes.map(t => t.split('/')[1].toUpperCase()).join(', ');
            this.showError(`Invalid file type. Allowed types: ${allowed}.`);
            e.target.value = '';
            return false;
        }
        
        this.clearError();
        return true;
    }
    
    showError(message) {
        this.clearError();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error-message';
        errorDiv.textContent = message;
        
        this.input.parentNode.insertBefore(errorDiv, this.input.nextSibling);
        this.input.classList.add('input-error');
    }
    
    clearError() {
        this.input.classList.remove('input-error');
        const errorMessage = this.input.parentNode.querySelector('.field-error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
}

// Auto-dismiss flash messages
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            message.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash messages
    initFlashMessages();
    
    // Initialize form validation for business form
    if (document.querySelector('.business-form')) {
        new FormValidator('.business-form');
        new FileUploadValidator('#logo_file');
    }
    
    // Initialize form validation for professional form
    if (document.querySelector('.professional-form')) {
        new FormValidator('.professional-form');
    }
    
    // Initialize any other forms
    document.querySelectorAll('form[data-validate]').forEach(form => {
        new FormValidator(`#${form.id}`);
    });
});

// Keyframe for slide up animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);
