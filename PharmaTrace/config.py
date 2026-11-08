
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-key"
    )

    # Neon PostgreSQL connection string
    DATABASE_URL = os.environ.get("DATABASE_URL")
