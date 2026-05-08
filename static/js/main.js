/**
 * SOFTWAP - Main JavaScript
 */

(function() {
    'use strict';

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    function handleScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll);

    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger
            const hamburger = navToggle.querySelector('.hamburger');
            if (hamburger) {
                hamburger.classList.toggle('active');
            }
        });

        // Close menu when clicking a link
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.website-type-card, .service-item, .value-card, .reason-item').forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add CSS for animated elements
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Add shake animation
                    field.style.animation = 'shake 0.5s';
                    setTimeout(function() {
                        field.style.animation = '';
                    }, 500);
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });

        // Remove invalid class on input
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                this.classList.remove('is-invalid');
            });
        });
    });

    // Add shake animation CSS
    const shakeStyle = document.createElement('style');
    shakeStyle.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .is-invalid {
            border-color: #ef4444 !important;
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2) !important;
        }
    `;
    document.head.appendChild(shakeStyle);

    // Parallax effect for gradient blobs
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const blobs = document.querySelectorAll('.gradient-blob');
        
        blobs.forEach(function(blob, index) {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            blob.style.transform = 'translateY(' + yPos + 'px)';
        });
        
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            window.requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick);

    // Pricing calculator for application form
    const websiteTypeSelect = document.getElementById('id_website_type');
    if (websiteTypeSelect) {
        websiteTypeSelect.addEventListener('change', function() {
            const priceDisplay = document.querySelector('.price-estimate-display');
            if (priceDisplay) {
                const selectedOption = this.options[this.selectedIndex];
                if (selectedOption && selectedOption.dataset.price) {
                    priceDisplay.value = selectedOption.dataset.price;
                }
            }
        });
    }

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(function() {
                // Show feedback
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                setTimeout(function() {
                    button.textContent = originalText;
                }, 2000);
            });
        });
    });

    // Tooltip functionality
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(function(element) {
        element.addEventListener('mouseenter', function(e) {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            tooltip.style.cssText = `
                position: absolute;
                background: var(--bg-secondary);
                color: var(--text-primary);
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 0.875rem;
                white-space: nowrap;
                z-index: 1000;
                border: 1px solid var(--border);
                pointer-events: none;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.bottom + 8 + 'px';
            
            this._tooltip = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });

    console.log('SOFTWAP - Website loaded successfully');
})();
