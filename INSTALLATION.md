# INSTALLATION GUIDE

## Quick Start (5 minutes)

### Prerequisites
- Python 3.13
- pip
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/Alvin-creator-ai/afrifin-ai-cfo.git
cd afrifin-ai-cfo
```

### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3.13 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR (Required for Receipt Processing)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

### Step 5: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here
```

### Step 6: Run Application
```bash
# Initialize database
python -c "from memory.database import Database; db = Database(); db.init_default_accounts()"

# Start Streamlit app
streamlit run app.py
```

The application will open at: `http://localhost:8501`

---

## GitHub Codespaces Setup

### Prerequisites
- GitHub account
- Repository access

### Steps
1. Open repository in Codespaces:
   - Click "Code" → "Codespaces" → "Create codespace on main"

2. Wait for Codespaces to initialize (2-3 minutes)

3. In terminal:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Install Tesseract:
```bash
# In Codespaces (Linux)
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

5. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
nano .env
```

6. Start application:
```bash
streamlit run app.py
```

7. Open in browser using the Codespaces forwarded port

---

## Troubleshooting Installation

### Error: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install --upgrade openai
```

### Error: "Tesseract not found"
**Solution:** Verify tesseract is installed:
```bash
which tesseract  # macOS/Linux
where tesseract  # Windows
```

### Error: "OpenAI API Key not found"
**Solution:** Verify .env file:
```bash
# Check if .env exists and has OPENAI_API_KEY
cat .env
```

### Error: "Database locked"
**Solution:** Close other Streamlit instances and clear cache:
```bash
rm -rf .streamlit/
streamlit run app.py
```

### Error: "Port 8501 already in use"
**Solution:** Use different port:
```bash
streamlit run app.py --server.port 8502
```

---

## Post-Installation Verification

Run this to verify everything is working:

```bash
python -c "
import sys
print('✓ Python version:', sys.version)

from openai import OpenAI
print('✓ OpenAI library installed')

import pytesseract
print('✓ Tesseract installed')

import streamlit as st
print('✓ Streamlit installed')

import pandas as pd
print('✓ Pandas installed')

from memory.database import Database
db = Database()
print('✓ Database initialized')

print('\n✅ All systems ready!')
"
```

---

## Next Steps

After installation:

1. Review `.env` configuration
2. Read GETTING_STARTED.md
3. Start with "Transaction Analyzer" page
4. Upload sample receipt
5. Generate your first financial report

For detailed usage guide, see: [GETTING_STARTED.md](GETTING_STARTED.md)
