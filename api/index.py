from main import app

# Vercel needs a named handler, but for FastAPI it usually just expects the module
# This file effectively exposes the 'app' object to Vercel's runtime
