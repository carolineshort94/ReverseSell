import os
from dotenv import load_dotenv


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/reverse"
)

# CORS configuration
cors_origins_value = os.environ.get(
    "CORS_ORIGINS", "http://localhost,http://localhost:3000"
)
CORS_ORIGINS = cors_origins_value.split(",")
