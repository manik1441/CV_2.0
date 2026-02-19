document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const navbar = document.querySelector('.navbar');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const headerOffset = 80; // Height of your fixed header
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                const startPosition = window.pageYOffset;
                const distance = offsetPosition - startPosition;
                const duration = 800; // Duration in milliseconds (0.8 seconds)
                let start = null;

                function step(timestamp) {
                    if (!start) start = timestamp;
                    const progress = timestamp - start;

                    // Ease-in-out cubic function for smoother acceleration and deceleration
                    const easeInOutCubic = (t) => {
                        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
                    };

                    const percentage = Math.min(progress / duration, 1);
                    const ease = easeInOutCubic(percentage);

                    window.scrollTo(0, startPosition + (distance * ease));

                    if (progress < duration) {
                        window.requestAnimationFrame(step);
                    }
                }

                window.requestAnimationFrame(step);
            }

            // Close mobile menu after click
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    });

    // Experience Timeline Expansion
    const timelineItems = document.querySelectorAll('.timeline-content');

    timelineItems.forEach(item => {
        item.addEventListener('click', function() {
            // Close other open items (optional, remove if you want multiple open)
            timelineItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });

            this.classList.toggle('active');
        });
    });

    // Load Data from JSON
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            // Load Education Data
            const educationTimeline = document.getElementById('education-timeline');
            if (educationTimeline && data.education) {
                data.education.forEach(edu => {
                    const timelineItem = document.createElement('div');
                    timelineItem.classList.add('timeline-item');

                    timelineItem.innerHTML = `
                        <div class="timeline-content">
                            <h3>${edu.degree}</h3>
                            <h4>${edu.college}</h4>
                            <h4>${edu.location}</h4>
                            <span class="date">${edu.year}</span>
                        </div>
                    `;

                    educationTimeline.appendChild(timelineItem);
                });
            }

            // Load Contact Data
            const contactContent = document.getElementById('contact-content');
            if (contactContent && data.contact) {
                contactContent.innerHTML = `
                    <p class="location"><i class="fas fa-map-marker-alt"></i> ${data.contact.location}</p>
                    <p class="phone"><i class="fas fa-phone"></i> ${data.contact.phone}</p>
                    <p class="email"><i class="fas fa-email"></i> ${data.contact.email}</p>
                    <p>${data.contact.message}</p>
                    <div class="social-links">
                        <a href="mailto:${data.contact.email}" title="Email"><i class="fas fa-envelope"></i></a>
                        <a href="${data.contact.linkedin}" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="${data.contact.github}" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                    </div>
                `;
            }
        })
        .catch(error => console.error('Error loading data:', error));
});