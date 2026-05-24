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

    // Load Data from JSON
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            // Load Hero Data
            const heroInfo = document.getElementById('hero-info');
            if (heroInfo && data.hero) {
                const paragraphsHtml = data.hero.paragraphs.map(p => `<p>${p}</p>`).join('\n');
                heroInfo.innerHTML = `
                    <h1>Hi, I'm <span class="highlight">${data.hero.name}</span></h1>
                    <h2>${data.hero.title}</h2>
                    ${paragraphsHtml}
                `;
            }

            // Load About Me Data
            const aboutList = document.getElementById('about-list');
            if (aboutList && data.about) {
                data.about.forEach(item => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <i class="fas fa-check-circle"></i>
                        <span>${item}</span>
                    `;
                    aboutList.appendChild(li);
                });
            }

            // Load Certifications Data
            const certGrid = document.getElementById('cert-grid');
            if (certGrid && data.certifications) {
                data.certifications.forEach(cert => {
                    const certCard = document.createElement('div');
                    certCard.classList.add('cert-card');

                    certCard.innerHTML = `
                        <i class="${cert.icon}"></i>
                        <h3>${cert.title}</h3>
                        <h4>${cert.issuer}</h4>
                    `;

                    certGrid.appendChild(certCard);
                });
            }

            // Load Experience Data
            const experienceTimeline = document.getElementById('experience-timeline');
            if (experienceTimeline && data.experience) {
                data.experience.forEach(exp => {
                    const timelineItem = document.createElement('div');
                    timelineItem.classList.add('timeline-item');

                    const detailsHtml = exp.details.map(detail => `<li>${detail}</li>`).join('\n');

                    timelineItem.innerHTML = `
                        <div class="timeline-content">
                            <div class="timeline-header">
                                <h3>${exp.role}</h3>
                                <h4>${exp.company}</h4>
                                <span class="date">${exp.duration}</span>
                                <span class="expand-btn">View Details <i class="fas fa-chevron-down"></i></span>
                            </div>
                            <div class="experience-details">
                                <ul>
                                    ${detailsHtml}
                                </ul>
                            </div>
                        </div>
                    `;

                    // Click event listener to expand/collapse
                    const timelineContent = timelineItem.querySelector('.timeline-content');
                    timelineContent.addEventListener('click', function() {
                        // Close other open experience items
                        const otherContents = experienceTimeline.querySelectorAll('.timeline-content');
                        otherContents.forEach(otherItem => {
                            if (otherItem !== timelineContent && otherItem.classList.contains('active')) {
                                otherItem.classList.remove('active');
                            }
                        });
                        this.classList.toggle('active');
                    });

                    experienceTimeline.appendChild(timelineItem);
                });
            }

            // Load Projects Data (Professional & Personal Subsections)
            const profGrid = document.getElementById('professional-projects-grid');
            const persGrid = document.getElementById('personal-projects-grid');

            function renderProjectCards(projectsArray, targetContainer) {
                if (targetContainer && projectsArray) {
                    targetContainer.innerHTML = ''; // Clear fallback/placeholders
                    projectsArray.forEach(project => {
                        const projectCard = document.createElement('div');
                        projectCard.classList.add('project-card');

                        const githubLinkHtml = project.github 
                            ? `<a href="${project.github}" target="_blank" class="project-github-link"><i class="fab fa-github"></i> View Repository</a>` 
                            : '';

                        projectCard.innerHTML = `
                            <div class="project-info">
                                <h3>${project.title}</h3>
                                <p class="role"><strong>Role:</strong> ${project.role}</p>
                                <p>${project.description}</p>
                                ${githubLinkHtml}
                            </div>
                        `;

                        targetContainer.appendChild(projectCard);
                    });
                }
            }

            if (data.projects) {
                renderProjectCards(data.projects.professional, profGrid);
                renderProjectCards(data.projects.personal, persGrid);
            }

            // Load Skills Data (Both Classic and Modern Tabbed Layouts)
            const skillsClassicView = document.getElementById('skills-classic-view');
            const skillsModernView = document.getElementById('skills-modern-view');

            if (data.skills) {
                // 1. Render Classic View
                if (skillsClassicView) {
                    skillsClassicView.innerHTML = ''; // Clear fallback
                    data.skills.forEach(cat => {
                        const wrapper = document.createElement('div');
                        wrapper.classList.add('skill-category-wrapper');

                        const gridItems = cat.subcategories.map(sub => `
                            <div class="text-skill-card">
                                <h4>${sub.name}</h4>
                                <p>${sub.items.join(', ')}</p>
                            </div>
                        `).join('\n');

                        wrapper.innerHTML = `
                            <h3 class="category-header"><i class="${cat.icon}"></i> ${cat.category}</h3>
                            <div class="category-grid">
                                ${gridItems}
                            </div>
                        `;

                        skillsClassicView.appendChild(wrapper);
                    });
                }

                // 2. Render Modern Tabbed View
                if (skillsModernView) {
                    skillsModernView.innerHTML = ''; // Clear fallback

                    // Create Tabs Navigation
                    const tabsNav = document.createElement('div');
                    tabsNav.classList.add('skills-tabs-nav');

                    // Create Tabs Content Container
                    const tabsContent = document.createElement('div');
                    tabsContent.classList.add('skills-tabs-content');

                    data.skills.forEach((cat, index) => {
                        const isActive = index === 0;

                        // Create Tab button
                        const tabBtn = document.createElement('button');
                        tabBtn.className = `tab-nav-btn ${isActive ? 'active' : ''}`;
                        tabBtn.dataset.tabId = `tab-pane-${index}`;
                        tabBtn.innerHTML = `<i class="${cat.icon}"></i> ${cat.category}`;
                        tabsNav.appendChild(tabBtn);

                        // Create Tab pane
                        const tabPane = document.createElement('div');
                        tabPane.id = `tab-pane-${index}`;
                        tabPane.className = `skills-tab-pane ${isActive ? 'active' : ''}`;

                        const rowContainer = document.createElement('div');
                        rowContainer.classList.add('modern-skills-container');

                        cat.subcategories.forEach(sub => {
                            const row = document.createElement('div');
                            row.classList.add('modern-skill-row');

                            const badgesHtml = sub.items.map(item => `
                                <span class="skill-badge">${item}</span>
                            `).join('\n');

                            row.innerHTML = `
                                <div class="modern-skill-row-header">${sub.name}</div>
                                <div class="modern-skill-row-content">
                                    <div class="skills-badge-container">
                                        ${badgesHtml}
                                    </div>
                                </div>
                            `;
                            rowContainer.appendChild(row);
                        });

                        tabPane.appendChild(rowContainer);
                        tabsContent.appendChild(tabPane);

                        // Tab Button click event
                        tabBtn.addEventListener('click', () => {
                            // Deactivate other tabs
                            tabsNav.querySelectorAll('.tab-nav-btn').forEach(btn => btn.classList.remove('active'));
                            tabsContent.querySelectorAll('.skills-tab-pane').forEach(pane => pane.classList.remove('active'));

                            // Activate selected
                            tabBtn.classList.add('active');
                            tabPane.classList.add('active');
                        });
                    });

                    skillsModernView.appendChild(tabsNav);
                    skillsModernView.appendChild(tabsContent);
                }

                // 3. Layout View Switcher Logic
                const btnClassic = document.getElementById('btn-classic-view');
                const btnModern = document.getElementById('btn-modern-view');

                function switchView(viewMode) {
                    if (viewMode === 'modern') {
                        btnClassic.classList.remove('active');
                        btnModern.classList.add('active');
                        skillsClassicView.classList.remove('active');
                        skillsModernView.classList.add('active');
                        localStorage.setItem('skills-view-preference', 'modern');
                    } else {
                        btnModern.classList.remove('active');
                        btnClassic.classList.add('active');
                        skillsModernView.classList.remove('active');
                        skillsClassicView.classList.add('active');
                        localStorage.setItem('skills-view-preference', 'classic');
                    }
                }

                if (btnClassic && btnModern) {
                    btnClassic.addEventListener('click', () => switchView('classic'));
                    btnModern.addEventListener('click', () => switchView('modern'));

                    // Force modern (Premium Tabs) view for all users
                    switchView('modern');
                }
            }

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