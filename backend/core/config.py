import os
from dotenv import load_dotenv

# Load environment variables only once
load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')

# Server configuration
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# SMTP configuration
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

# pgAdmin configuration
PGADMIN_EMAIL = os.getenv('PGADMIN_EMAIL')
PGADMIN_PASSWORD = os.getenv('PGADMIN_PASSWORD')
PGADMIN_PORT = int(os.getenv('PGADMIN_PORT', 5050)) 