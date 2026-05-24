# Manik Chaudhary - Professional Portfolio Website (CV 2.0)

Welcome to the repository for **CV 2.0**, the premium, interactive, and highly responsive professional portfolio website of **Manik Chaudhary**, a QA Architect and Lead Automation Test Engineer with over 11+ years of software quality engineering experience.

This portfolio is hand-crafted using modern vanilla technologies (HTML5, CSS3, and ES6+ JavaScript) to deliver a high-end, premium user experience showcasing professional expertise, leadership skills, career milestones, certifications, and projects.

---

## 🌟 Visual & Interactive Features

- **Premium Glassmorphic Design:** Implements clean, modern frosted-glass visual aesthetics utilizing advanced CSS3 backdrop filters, dynamic gradients, sleek shadows, and custom hover states.
- **Dynamic Data Binding:** Minimizes static HTML footprint by decoupling contact details and educational history into a centralized, easily editable JSON configuration file (`data.json`) loaded asynchronously at runtime.
- **Interactive Experience Timeline:** Experience milestones support dynamic expand/collapse states. On desktop viewports, clicking an experience card expands it to the side to reveal detailed bullet points with zero layout shift, creating a unique side-panel layout.
- **Custom Cubic Bezier Smooth Scrolling:** Employs a hand-crafted `requestAnimationFrame` JavaScript scroll-interpolation script utilizing an `easeInOutCubic` easing function for exceptionally smooth transitions to navbar anchors.
- **Responsive Mobile Layout:** Adaptable navigation features a custom Hamburger toggle menu optimized for mobile and tablet devices.
- **Modern Typography & Icons:** Clean, modern font layouts powered by Google Fonts (Poppins) and high-quality vector iconography via FontAwesome.

---

## 📂 Project Architecture

The workspace is organized as a lightweight, performant, and flat-structured static web application coupled with a Python-based resume builder:

```
CV_2.0/
├── index.html                   # Main page layout & semantic HTML5 structure
├── style.css                    # Comprehensive styling, variables, glassmorphism, & animations
├── file.js                      # UI logic: animations, scroll engines, & dynamic fetch
├── data.json                    # Centralized dataset for education and contact information
├── cv_updater.py                # Python script to apply smart gap analysis, sync data, and generate PDF
├── cv_differences.csv           # Auto-generated difference report tracking smart CV enhancements
├── Manik_Chaudhary_Test_Lead.pdf # Professional offline resume
└── Image.png                    # Profile picture asset
```

### File Breakdown

*   **`index.html`:** Implements proper SEO semantic structures (`<header>`, `<main>`, `<section>`, `<footer>`), search-engine friendly meta-tags, and sets up high-performance sections for Experience, Skills, Projects, and Certifications.
*   **`style.css`:** Drives the custom-tailored CSS design system using CSS variables (`:root`). Implements custom keyframes (`fadeInUp`, `fadeInRight`, `fadeInPage`) and a grid system for modular components (cards, certification badges, timelines).
*   **`file.js`:** Listens for `DOMContentLoaded` to bootstrap the application. Manages responsive state changes, triggers easing-driven anchor scroll calculations, captures timeline item activations, and asynchronously handles network operations (`fetch('data.json')`).
*   **`data.json`:** Serves as a localized config. Editing contact information or updating colleges/graduation years in this file instantly updates the active website dynamically.
*   **`cv_updater.py`:** A robust Python automation engine that parses `data.json` dynamically, performs smart resume gap analysis (updating titles, summaries, and credentials), exports modification differences to `cv_differences.csv`, and generates a publication-quality 2-page print-ready resume PDF using ReportLab flowables.
*   **`cv_differences.csv`:** An auto-generated audit report that details the original values, proposed values, and strategic hiring-market rationales behind the automated resume updates.

---

## 🛠️ Automated CV Updater & PDF Generator

The repository includes a powerful automated script, `cv_updater.py`, that bridges the gap between your digital profile (`data.json`) and your print-ready executive PDF resume.

### 🌟 Key Capabilities
1. **Smart Enhancements & Gap Analysis**: Automatically updates titles (e.g., modernizing target QA roles), adjusts summary phrasing, and injects critical credentials like *SAFe 5.0 Practitioner* dynamically to align with enterprise QA requirements.
2. **Audit Tracking (`cv_differences.csv`)**: Logs every single automated enhancement, detailing the modified section, original value, proposed value, and professional rationale behind the change.
3. **ReportLab PDF Compilation Engine**: Programmatically builds a pixel-perfect, double-sided (exactly 2 pages) executive PDF resume (`Manik_Chaudhary_Test_Lead_V1.pdf`) using structured tables, custom spacing, and professional color typography (Navy, Slate, and Charcoal).
4. **Data Sync Option**: If you want the smart resume modifications to persist directly back to your source website configuration file (`data.json`), simply set `UPDATE_DATA_JSON = True` in `cv_updater.py`.

### 🚀 Running the CV Updater
To run the resume compiler and generator locally:

1. **Install Dependencies**:
   Ensure you have ReportLab installed:
   ```bash
   pip install reportlab
   ```
2. **Run the Script**:
   Execute the updater script using Python:
   ```bash
   python cv_updater.py
   ```
3. **Verify Output**:
   - Open `cv_differences.csv` to review the smart changes applied.
   - Open `Manik_Chaudhary_Test_Lead_V1.pdf` to see your beautifully formatted 2-page executive resume.

---


## 🚀 How to Run Locally

Because the JavaScript files perform an asynchronous HTTP `fetch` to retrieve `data.json`, standard modern web browsers will block this request under the `file://` protocol due to **CORS (Cross-Origin Resource Sharing)** security restrictions. 

To view the fully functional website locally, you should run it using a local development server:

### Method 1: VS Code Live Server (Recommended)
1. Install the **Live Server** extension in VS Code.
2. Open the `CV_2.0` directory in VS Code.
3. Click the **Go Live** button in the bottom status bar, or right-click `index.html` and select **Open with Live Server**.

### Method 2: Python HTTP Server (Standard Terminal)
If you have Python installed, open your shell in the `CV_2.0` directory and run:
```bash
# For Python 3.x
python -m http.server 8000
```
Then navigate to `http://localhost:8000` in your web browser.

### Method 3: Node.js `http-server`
If you have Node.js installed:
```bash
npx http-server -p 8000
```
Then navigate to `http://localhost:8000` in your web browser.