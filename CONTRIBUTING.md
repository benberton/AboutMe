# Contributing to Ben Berton's Portfolio

Thank you for your interest in contributing! This document provides guidelines and best practices for maintaining and improving this portfolio website.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [File Organization](#file-organization)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)

## 🚀 Getting Started

### Prerequisites
- Basic knowledge of HTML, CSS, and JavaScript
- A modern web browser
- A text editor or IDE
- Git for version control

### Setup
1. Clone the repository
2. Navigate to `docs/` folder
3. Open `index.html` in your browser
4. Make changes and refresh to see updates

## 🔄 Development Workflow

### Making Changes

1. **Create a branch** (if contributing):
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Edit HTML in `docs/index.html`
   - Edit styles in `docs/assets/css/styles.css`
   - Edit JavaScript in `docs/assets/js/main.js`

3. **Test your changes**:
   - Test on desktop browsers
   - Test on mobile devices
   - Check accessibility
   - Validate HTML/CSS

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push and create PR** (if contributing):
   ```bash
   git push origin feature/your-feature-name
   ```

## 🎨 Code Style

### HTML
- Use semantic HTML5 elements
- Include proper ARIA labels
- Maintain consistent indentation (4 spaces)
- Add comments for complex sections
- Keep accessibility in mind

```html
<!-- Good Example -->
<section id="education">
    <div class="section-inner">
        <h2>Education</h2>
        <div class="card card-with-logo">
            <!-- Card content -->
        </div>
    </div>
</section>
```

### CSS
- Use CSS custom properties for colors and spacing
- Follow BEM-like naming where appropriate
- Group related styles together
- Comment major sections
- Mobile-first approach for responsive design

```css
/* Section Comment */
.component-name {
    /* Properties in logical order */
    display: flex;
    align-items: center;
    
    /* Spacing */
    margin: var(--space-md);
    padding: var(--space-sm);
    
    /* Visual */
    background: var(--fog);
    border: 1px solid var(--stone-light);
    
    /* Transitions */
    transition: all var(--transition-smooth);
}
```

### JavaScript
- Use modern ES6+ syntax
- Add comments for complex logic
- Keep functions small and focused
- Handle edge cases

```javascript
// Good Example
function handleScroll() {
    const scrollPosition = window.scrollY;
    
    // Update progress indicator
    updateProgressDots(scrollPosition);
    
    // Handle parallax effect
    updateMountainLayers(scrollPosition);
}
```

## 📁 File Organization

### Directory Structure
```
docs/
├── index.html              # Main HTML file
├── assets/
│   ├── css/
│   │   └── styles.css      # Main stylesheet
│   ├── js/
│   │   └── main.js         # Main JavaScript
│   └── images/             # Image assets
└── ...
```

### Adding New Sections
1. Add HTML in `index.html`:
   ```html
   <section id="new-section">
       <div class="section-inner">
           <h2>Section Title</h2>
           <!-- Content -->
       </div>
   </section>
   ```

2. Add navigation link in header:
   ```html
   <a href="#new-section" class="header-link">New Section</a>
   ```

3. Add progress indicator dot:
   ```html
   <button class="progress-dot" data-section="new-section" 
           aria-label="Go to new section"></button>
   ```

4. Add styles if needed in `styles.css`

### Adding New Styles
1. Check if existing variables can be used
2. Add new variables to `:root` if needed
3. Group styles logically
4. Add responsive styles in media queries
5. Test across browsers and devices

## 🧪 Testing

### Manual Testing Checklist
- [ ] Desktop browsers (Chrome, Firefox, Safari, Edge)
- [ ] Mobile devices (iOS, Android)
- [ ] Tablet devices
- [ ] Different screen sizes (320px to 2560px)
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Reduced motion preferences
- [ ] Print styles

### Accessibility Testing
- [ ] Valid HTML (use W3C Validator)
- [ ] Proper heading hierarchy
- [ ] Alt text for images
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Color contrast ratios meet WCAG AA
- [ ] Focus indicators visible

### Performance Testing
- [ ] Lighthouse score 90+
- [ ] Images optimized
- [ ] CSS/JS minified for production
- [ ] No console errors
- [ ] Fast page load (< 2s on 3G)

## 📝 Commit Guidelines

### Commit Message Format
```
type: Brief description (50 characters or less)

More detailed explanation if needed (wrap at 72 characters).
Explain what changed and why.

- Bullet points for multiple changes
- Use present tense ("Add feature" not "Added feature")
- Reference issues/PRs if applicable
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
feat: Add dark mode toggle

Implement dark mode with preference detection and manual toggle.
- Add CSS custom properties for dark theme
- Create toggle button in header
- Save preference to localStorage

---

fix: Correct mobile timeline alignment

Timeline dots were misaligned on mobile screens below 480px.
Adjusted left positioning and added proper spacing.

---

docs: Update README with deployment instructions

Added section explaining GitHub Pages deployment process
and alternative hosting options.
```

## 🐛 Reporting Issues

### Before Submitting
- Check if the issue already exists
- Test in multiple browsers
- Include reproduction steps
- Add screenshots if visual issue

### Issue Template
```markdown
**Description**
Clear description of the issue

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Screenshots**
If applicable

**Environment**
- Browser: [e.g., Chrome 120]
- OS: [e.g., macOS 14]
- Device: [e.g., iPhone 15, Desktop]
- Screen Size: [e.g., 1920x1080]
```

## 🔧 Common Tasks

### Update Personal Information
Edit the intro section in `index.html`:
```html
<section id="intro">
    <div class="section-inner">
        <h2>I'm [Your Name]</h2>
        <p>[Your description]</p>
    </div>
</section>
```

### Add New Experience
Add to the timeline in the experience section:
```html
<div class="timeline-item">
    <div class="card card-with-logo">
        <img src="images/logo.png" alt="Company logo" class="card-logo">
        <div class="card-content">
            <h3>Job Title</h3>
            <p class="location">Location</p>
            <p>Date Range</p>
            <ul>
                <li>Achievement 1</li>
                <li>Achievement 2</li>
            </ul>
        </div>
    </div>
</div>
```

### Add New Skill
Add to the skills section:
```html
<span class="skill-tag">New Skill</span>
```

### Change Color Scheme
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #yourcolor;
    --secondary-color: #yourcolor;
    /* etc. */
}
```

## 📚 Resources

- [MDN Web Docs](https://developer.mozilla.org/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Can I Use](https://caniuse.com/)
- [CSS Tricks](https://css-tricks.com/)
- [A11y Project](https://www.a11yproject.com/)

## ❓ Questions

If you have questions or need help:
1. Check existing documentation
2. Review closed issues
3. Open a new issue with the "question" label

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉
