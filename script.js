// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Reveal next text block
function revealNext(button) {
    const textRevealer = button.closest('.text-revealer');
    const blocks = textRevealer.querySelectorAll('.text-block');
    let currentIndex = -1;
    
    blocks.forEach((block, index) => {
        if (block.classList.contains('active')) {
            currentIndex = index;
        }
    });
    
    if (currentIndex < blocks.length - 1) {
        blocks[currentIndex].classList.remove('active');
        blocks[currentIndex + 1].classList.add('active');
        
        // Scroll to the new active block
        blocks[currentIndex + 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Hide button if it's the last block
        if (currentIndex + 1 === blocks.length - 1) {
            button.style.opacity = '0';
            setTimeout(() => {
                button.style.display = 'none';
            }, 300);
        }
    }
}

// Toggle case accordion
function toggleCase(titleElement) {
    const caseItem = titleElement.closest('.case-item');
    const isActive = caseItem.classList.contains('active');
    
    // Close all other cases
    document.querySelectorAll('.case-item').forEach(item => {
        if (item !== caseItem) {
            item.classList.remove('active');
        }
    });
    
    // Toggle current case
    if (isActive) {
        caseItem.classList.remove('active');
    } else {
        caseItem.classList.add('active');
        // Scroll to case
        setTimeout(() => {
            caseItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}

// Toggle experience accordion
function toggleExperience(headerElement) {
    const item = headerElement.closest('.experience-item');
    const isActive = item.classList.contains('active');

    // Close other items
    document.querySelectorAll('.experience-item').forEach(other => {
        if (other !== item) {
            other.classList.remove('active');
        }
    });

    // Toggle current
    if (isActive) {
        item.classList.remove('active');
    } else {
        item.classList.add('active');
    }
}

// Parallax effect for backgrounds
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax-bg');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach((element, index) => {
            const section = element.closest('.section');
            const rect = section.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                const speed = 0.3;
                const yPos = -(scrolled - rect.top) * speed;
                element.style.transform = `translateY(${yPos}px)`;
            }
        });
    });
}

// Highlight keywords animation
function initKeywordHighlight() {
    const keywords = document.querySelectorAll('.highlight-keyword');
    
    keywords.forEach(keyword => {
        keyword.addEventListener('mouseenter', function() {
            this.style.textShadow = '0 0 20px rgba(0, 212, 255, 1)';
            this.style.transform = 'scale(1.05)';
        });
        
        keyword.addEventListener('mouseleave', function() {
            this.style.textShadow = '';
            this.style.transform = '';
        });
    });
}

// Tool icons animation on reveal
function initToolIcons() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const icons = entry.target.querySelectorAll('.tool-icon');
                icons.forEach((icon, index) => {
                    icon.style.setProperty('--delay', index);
                    setTimeout(() => {
                        icon.style.opacity = '1';
                        icon.style.transform = 'scale(1) rotate(0deg)';
                    }, index * 100);
                });
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.text-block').forEach(block => {
        observer.observe(block);
    });
}

// Navigation active state
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.section');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Smooth scroll for navigation links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Show case preview on hover
function initCaseHover() {
    const caseTitles = document.querySelectorAll('.case-title');
    
    caseTitles.forEach(title => {
        const caseItem = title.closest('.case-item');
        const preview = caseItem.querySelector('.case-preview');
        
        title.addEventListener('mouseenter', () => {
            if (!caseItem.classList.contains('active')) {
                preview.style.opacity = '1';
                preview.style.transform = 'translateY(0)';
            }
        });
        
        title.addEventListener('mouseleave', () => {
            if (!caseItem.classList.contains('active')) {
                preview.style.opacity = '0.7';
            }
        });
    });
}

// Keyboard navigation
function initKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
            const activeRevealer = document.querySelector('.text-block.active')?.closest('.text-revealer');
            if (activeRevealer) {
                const nextButton = activeRevealer.querySelector('.btn-next');
                if (nextButton && nextButton.style.display !== 'none') {
                    revealNext(nextButton);
                }
            }
        }
    });
}

// Sequential reveal for "What I look for" section
function initWhatILookFor() {
    const section = document.querySelector('#what-i-look-for');
    if (!section) return;

    const blocks = Array.from(section.querySelectorAll('.text-block'));
    const nextButton = section.querySelector('.what-next-btn');
    if (!blocks.length || !nextButton) return;

    let currentIndex = 0;

    // initial state
    blocks.forEach((block, index) => {
        if (index === 0) {
            block.classList.add('active');
        } else {
            block.classList.remove('active');
        }

        const p = block.querySelector('p');
        if (p) {
            p.style.cursor = 'pointer';
            p.addEventListener('click', () => {
                if (currentIndex >= blocks.length - 1) return;

                blocks[currentIndex].classList.remove('active');
                currentIndex += 1;
                blocks[currentIndex].classList.add('active');
                blocks[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });

                if (currentIndex === blocks.length - 1) {
                    nextButton.style.display = 'inline-block';
                    nextButton.style.opacity = '1';
                }
            });
        }
    });

    // configure final next button
    nextButton.textContent = 'Далее';
    nextButton.style.display = 'none';
    nextButton.style.opacity = '0';
    nextButton.addEventListener('click', () => scrollToSection('why-choose-me'));
}

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initParallax();
    initKeywordHighlight();
    initToolIcons();
    initNavigation();
    initSmoothScroll();
    initCaseHover();
    initWhatILookFor();
    initKeyboardNavigation();
    
    // Show first text block in each revealer
    document.querySelectorAll('.text-revealer').forEach(revealer => {
        const firstBlock = revealer.querySelector('.text-block');
        if (firstBlock) {
            firstBlock.classList.add('active');
        }
    });
    
    // Add fade-in animation to sections on scroll
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        sectionObserver.observe(section);
    });
    
    // Initial fade-in for hero
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.opacity = '1';
        hero.style.transform = 'translateY(0)';
    }
});

// Add glow effect to active navigation link
const style = document.createElement('style');
style.textContent = `
    .nav-links a.active {
        color: var(--primary-color);
    }
    .nav-links a.active::after {
        width: 100%;
    }
    .case-preview {
        opacity: 0.7;
        transform: translateY(-5px);
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);