# Load environment variables from .env
import os
from dotenv import load_dotenv
load_dotenv()

# MongoDB connection string from environment
MONGO_URI = os.getenv("MONGO_URI")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")