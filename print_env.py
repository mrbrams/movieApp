import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch and print the DATABASE_URL environment variable
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

print(f"DATABASE_URL: {database_url}")
print(f"SECRET_KEY: {secret_key}")
print(f"ALGORITHM: {algorithm}")
print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {access_token_expire_minutes}")