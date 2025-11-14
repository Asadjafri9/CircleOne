// Main JavaScript file for CircleOne

// Initialize animations and theme
document.addEventListener('DOMContentLoaded', function () {
    initializeAnimations();
    initializeTheme();
    updateThemeIcon();
});

// Initialize theme based on user preference or system preference
function initializeTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');

    // If no theme is set, check system preference
    if (!currentTheme) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = prefersDark ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
    }
}

// Add smooth animations to elements
function initializeAnimations() {
    // Scroll reveal animation
    const revealElements = document.querySelectorAll('.feature-card, .dashboard-card, .profile-card, .business-card, .professional-card, .stat-card, .info-card');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    revealElements.forEach(element => {
        element.classList.add('reveal');
        revealObserver.observe(element);
    });

    // Parallax effect on scroll - DISABLED for stability
    // window.addEventListener('scroll', handleParallax);

    // Magnetic button effect - DISABLED for stability
    // initializeMagneticButtons();

    // Card tilt effect on mouse move - DISABLED for stability
    // initializeCardTilt();

    // Animated number counters
    animateCounters();

    // Enhanced card interactions - DISABLED for stability
    // enhanceCardInteractions();
}

// Update theme icon
function updateThemeIcon() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const icons = document.querySelectorAll('.theme-icon');
    const labels = document.querySelectorAll('.theme-label');

    icons.forEach(icon => {
        icon.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
    });

    labels.forEach(label => {
        label.textContent = currentTheme === 'dark' ? 'Light' : 'Dark';
    });
}

// Toggle theme for authenticated users (saves to database)
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    // Update theme immediately
    document.documentElement.setAttribute('data-theme', newTheme);
    updateThemeIcon();

    // Save to database via API
    fetch('/api/update-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme: newTheme })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Theme saved to database:', data.theme);
            }
        })
        .catch(error => console.error('Error saving theme:', error));

    return newTheme;
}

// Toggle theme for guest users (uses localStorage only)
function toggleThemeGuest() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', newTheme);
    updateThemeIcon();

    // Save theme preference to localStorage
    localStorage.setItem('theme', newTheme);

    return newTheme;
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function () {
    // For guests, check localStorage
    const savedTheme = localStorage.getItem('theme');
    const currentTheme = document.documentElement.getAttribute('data-theme');

    // If guest and has saved preference, use it
    if (!document.body.classList.contains('authenticated') && savedTheme && savedTheme !== currentTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    // Update icon to match current theme (for both authenticated and guest users)
    updateThemeIcon();

    // Ensure authenticated users also get icon updated correctly
    const htmlTheme = document.documentElement.getAttribute('data-theme');
    if (!htmlTheme) {
        // If no theme is set, default to light
        document.documentElement.setAttribute('data-theme', 'light');
    }
    updateThemeIcon();
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to OAuth buttons
document.querySelectorAll('.btn-oauth').forEach(button => {
    button.addEventListener('click', function () {
        this.style.opacity = '0.7';
        this.style.pointerEvents = 'none';
        this.innerHTML = '<span>Redirecting...</span>';
    });
});

// Simple notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#34a853' : type === 'error' ? '#ea4335' : '#4285f4'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Handle form submissions with AJAX
function handleFormSubmit(formId, callback) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (callback) {
                    callback(result);
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('An error occurred. Please try again.', 'error');
            }
        });
    }
}

console.log('CircleOne initialized');

// Parallax scrolling effect
function handleParallax() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.parallax');

    parallaxElements.forEach(element => {
        const speed = 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
    });
}

// Magnetic button effect
function initializeMagneticButtons() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-glow');

    buttons.forEach(button => {
        button.addEventListener('mousemove', function (e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const moveX = (x - centerX) * 0.1;
            const moveY = (y - centerY) * 0.1;

            button.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.05)`;
        });

        button.addEventListener('mouseleave', function () {
            button.style.transform = 'translate(0, 0) scale(1)';
        });
    });
}

// 3D card tilt effect
function initializeCardTilt() {
    const cards = document.querySelectorAll('.feature-card, .business-card, .professional-card, .stat-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
        });

        card.addEventListener('mouseleave', function () {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
        });
    });
}

// Animated number counters
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = counter.textContent;
        const isNumber = /^\d+/.test(target);

        if (isNumber) {
            const targetNumber = parseInt(target.replace(/\D/g, ''));
            let current = 0;
            const increment = targetNumber / 50;
            const duration = 2000;
            const stepTime = duration / 50;

            const observer = new IntersectionObserver(function (entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !counter.classList.contains('counted')) {
                        counter.classList.add('counted');

                        const timer = setInterval(() => {
                            current += increment;
                            if (current >= targetNumber) {
                                counter.textContent = target;
                                clearInterval(timer);
                            } else {
                                counter.textContent = Math.floor(current) + (target.includes('+') ? '+' : '');
                            }
                        }, stepTime);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(counter);
        }
    });
}

// Enhanced card interactions
function enhanceCardInteractions() {
    const cards = document.querySelectorAll('.feature-card, .business-card, .professional-card');

    cards.forEach(card => {
        // Add ripple effect on click
        card.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = card.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            card.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Add CSS for ripple effect
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: rippleAnimation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes rippleAnimation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Smooth scroll with easing
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const startPosition = window.pageYOffset;
            const targetPosition = target.offsetTop - 80;
            const distance = targetPosition - startPosition;
            const duration = 800;
            let start = null;

            function animation(currentTime) {
                if (start === null) start = currentTime;
                const timeElapsed = currentTime - start;
                const run = easeInOutCubic(timeElapsed, startPosition, distance, duration);
                window.scrollTo(0, run);
                if (timeElapsed < duration) requestAnimationFrame(animation);
            }

            function easeInOutCubic(t, b, c, d) {
                t /= d / 2;
                if (t < 1) return c / 2 * t * t * t + b;
                t -= 2;
                return c / 2 * (t * t * t + 2) + b;
            }

            requestAnimationFrame(animation);
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll <= 0) {
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.15)';
    }

    lastScroll = currentScroll;
});

// Add loading animation for images
document.querySelectorAll('img').forEach(img => {
    // Add lazy loading attribute if not present
    if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
    }

    img.addEventListener('load', function () {
        this.classList.add('loaded');
        this.style.opacity = '1';
    });

    if (img.complete) {
        img.classList.add('loaded');
        img.style.opacity = '1';
    }
});

// Enhanced form interactions
document.querySelectorAll('.form-control, .search-input').forEach(input => {
    input.addEventListener('focus', function () {
        this.parentElement?.classList.add('focused');
    });

    input.addEventListener('blur', function () {
        if (!this.value) {
            this.parentElement?.classList.remove('focused');
        }
    });
});
