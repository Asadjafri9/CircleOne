// Mobile Navigation

class MobileNavigation {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.navMenu = document.querySelector('.nav-menu');
        this.hamburger = null;
        this.init();
    }
    
    init() {
        if (!this.navbar || !this.navMenu) return;
        
        // Create hamburger button
        this.createHamburger();
        
        // Add event listeners
        this.hamburger.addEventListener('click', () => this.toggleMenu());
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.navbar.contains(e.target) && this.navMenu.classList.contains('active')) {
                this.closeMenu();
            }
        });
        
        // Close menu when clicking on a link
        this.navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    this.closeMenu();
                }
            });
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.closeMenu();
                this.navMenu.style.display = '';
            }
        });
    }
    
    createHamburger() {
        // Check if hamburger already exists
        if (document.querySelector('.hamburger')) return;
        
        this.hamburger = document.createElement('button');
        this.hamburger.className = 'hamburger';
        this.hamburger.setAttribute('aria-label', 'Toggle navigation');
        this.hamburger.setAttribute('aria-expanded', 'false');
        this.hamburger.innerHTML = `
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        `;
        
        // Insert hamburger before nav-menu
        this.navMenu.parentNode.insertBefore(this.hamburger, this.navMenu);
    }
    
    toggleMenu() {
        if (this.navMenu.classList.contains('active')) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        this.navMenu.classList.add('active');
        this.hamburger.classList.add('active');
        this.hamburger.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
    
    closeMenu() {
        this.navMenu.classList.remove('active');
        this.hamburger.classList.remove('active');
        this.hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Initialize mobile navigation
document.addEventListener('DOMContentLoaded', function() {
    new MobileNavigation();
});
