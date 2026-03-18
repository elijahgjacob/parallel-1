import os
from dotenv import load_dotenv

load_dotenv()

PARALLEL_API_KEY = os.getenv("PARALLEL_API_KEY")

if not PARALLEL_API_KEY:
    raise ValueError("PARALLEL_API_KEY environment variable is required")
