# Contributing to ResumeAI

Thank you for your interest in contributing to ResumeAI! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js LTS
- Git
- Groq API Key

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ResumeAI.git
   cd ResumeAI
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv ..\.venv
   ..\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

3. **Set Up Frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start Development Servers**
   - Backend: `cd backend && flask run --port=5001`
   - Frontend: `cd frontend && npm run dev`

## 📋 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write clean, readable code
- Follow the existing code style
- Add comments for complex logic
- Test your changes locally

### 3. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for test changes

### 4. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📝 Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use 2-space indentation (Flask convention)
- Use meaningful variable names
- Add docstrings to functions and classes
- Use type hints where applicable

Example:
```python
def analyze_resume_with_ai(resume_text: str) -> dict:
    """
    Analyze resume using Groq AI.
    
    Args:
        resume_text: Raw resume text to analyze
        
    Returns:
        Dictionary with analysis results
    """
    # Implementation
```

### JavaScript/React (Frontend)
- Use ES6+ features
- Use meaningful component names
- Add JSDoc comments
- Keep components small and focused
- Use hooks instead of class components

Example:
```javascript
/**
 * Resume upload component
 * @param {Function} onUploadComplete - Callback after upload completes
 * @returns {JSX.Element}
 */
export function ResumeUpload({ onUploadComplete }) {
  // Implementation
}
```

## 🧪 Testing

Before submitting your PR, make sure to:
- Test your changes locally
- Verify no console errors or warnings
- Test with different data inputs
- Check responsive design (frontend)

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/error messages
- Your environment (OS, Python version, Node version, etc.)

## 💡 Feature Requests

For feature requests, please:
- Describe the feature in detail
- Explain the use case and benefits
- Provide any relevant examples or mock-ups
- Consider how it fits into the project vision

## 📚 Documentation

- Update README.md if adding new features
- Add comments for complex code sections
- Update API documentation for new endpoints
- Include setup instructions for new dependencies

## 🚫 What NOT to Do

- Don't commit `.env` files or sensitive data
- Don't commit `node_modules/` or `__pycache__/`
- Don't use hardcoded API keys or secrets
- Don't submit code without testing
- Don't make large unrelated changes in one PR

## ✅ PR Checklist

Before submitting your PR, verify:
- [ ] Code follows style guidelines
- [ ] Changes are tested locally
- [ ] No console errors or warnings
- [ ] `.gitignore` covers unnecessary files
- [ ] `.env` and secrets are NOT committed
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No merge conflicts with main branch

## 🤔 Questions?

- Check existing issues and PRs
- Review the project documentation
- Ask in PR comments or open a discussion

---

**Thank you for contributing to ResumeAI! 🎉**
