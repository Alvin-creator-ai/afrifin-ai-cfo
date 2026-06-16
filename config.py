"""
Configuration settings for AfriFin AI CFO.

Loads environment variables and provides configuration constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4"

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/afrifin.db")
DATABASE_NAME = os.getenv("DATABASE_NAME", "afrifin.db")

# Application Configuration
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Business Configuration
BUSINESS_CURRENCY = os.getenv("BUSINESS_CURRENCY", "KES")
BUSINESS_COUNTRY = os.getenv("BUSINESS_COUNTRY", "Kenya")
ACCOUNTING_STANDARD = os.getenv("ACCOUNTING_STANDARD", "IFRS")

# Streamlit Configuration
STREAMLIT_SERVER_PORT = os.getenv("STREAMLIT_SERVER_PORT", "8501")
STREAMLIT_SERVER_HEADLESS = os.getenv("STREAMLIT_SERVER_HEADLESS", "true").lower() == "true"

# Chart of Accounts
DEFAULT_ACCOUNTS = {
    "1010": "Cash",
    "1020": "Bank",
    "1030": "Accounts Receivable",
    "2010": "Accounts Payable",
    "3010": "Owner's Capital",
    "3020": "Retained Earnings",
    "4010": "Service Revenue",
    "4020": "Product Revenue",
    "5010": "Fuel Expense",
    "5020": "Internet Expense",
    "5030": "Utilities Expense",
    "5040": "Rent Expense",
    "5050": "Salary Expense",
    "5060": "Office Supplies Expense",
}

# Validation Rules
MAX_TRANSACTION_AMOUNT = 10000000  # 10 million KES
MIN_TRANSACTION_AMOUNT = 0.01
SUPPORTED_RECEIPT_FORMATS = [".pdf", ".png", ".jpg", ".jpeg"]

# Report Settings
REPORTS_DIRECTORY = "./reports"
EXPORTS_DIRECTORY = "./exports"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
