# ai-commit-vibe 🚀

A lightweight CLI tool that uses **Gemini 2.5 Flash** to generate concise **Conventional Commit** messages based on your staged changes.

Instead of writing commit messages manually, let AI analyze your git diff and suggest accurate commits instantly.

## ✨ Features

- **AI-powered commit suggestions** using Gemini 2.5 Flash
- **Initial commit detection**
- **Noise filtering** (ignores lock files and metadata)
- **Interactive selection** from 3 suggested commit messages
- **Conventional Commit format**

Example output:

    Suggested Commit Messages:
    
        1. feat(cli): add AI-powered commit message generator
        2. refactor(core): extract commit prompt logic
        3. chore: initialize project structure

## 📦 Installation
Install directly from GitHub using pip:
```bash
pip install git+https://github.com/YOUR_USERNAME/ai-commit-vibe.git
```

## 🔑 Setup
You need a Google Gemini API Key. Set it in your environment:

Windows (PowerShell/CMD)
```bash
setx GEMINI_API_KEY "your_key_here"
```

Mac/Linux
```bash
export GEMINI_API_KEY="your_key_here"
```

## 🛠️ Usage
 1. Stage your changes:
 ```bash
 git add .
 ```

 2. Run the tool:
 ```bash
 ai-commit
 ```

 3. Select your message: Choose 1, 2, or 3 to commit instantly!
