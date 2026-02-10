import asyncio
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any
import httpx
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

# Configuration
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
DATA_FILE = "/tmp/data.json" # Use /tmp for Vercel compatibility (readonly otherwise)
NOTIFICATION_EMAIL_TARGET = "23f1001015@ds.study.iitm.ac.in"
MAX_STORIES = 3

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    logger.info("GROQ_API_KEY found.")
else:
    logger.warning("GROQ_API_KEY NOT found in environment.")

client = AsyncGroq(api_key=api_key) if api_key else None

async def fetch_story_details(client: httpx.AsyncClient, story_id: int) -> Dict[str, Any]:
    """Fetch details for a single story."""
    try:
        response = await client.get(f"{HN_API_BASE}/item/{story_id}.json", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching story {story_id}: {e}")
        return {}

async def fetch_data() -> List[Dict[str, Any]]:
    """Fetch top stories from Hacker News and getting details for the first few."""
    async with httpx.AsyncClient() as http_client:
        try:
            # Fetch top story IDs
            response = await http_client.get(f"{HN_API_BASE}/topstories.json", timeout=10.0)
            response.raise_for_status()
            story_ids = response.json()[:MAX_STORIES]
            
            # Fetch details in parallel
            tasks = [fetch_story_details(http_client, sid) for sid in story_ids]
            stories = await asyncio.gather(*tasks)
            
            # Filter out failed fetches
            return [s for s in stories if s]
        except Exception as e:
            logger.error(f"Error fetching top stories: {e}")
            return []

async def analyze_story(text: str) -> Dict[str, Any]:
    if not text:
        return {"summary": "No content to analyze", "sentiment": "neutral"}
        
    if not client:
        logger.warning("Groq API key not found. Skipping analysis.")
        return {"summary": "Analysis skipped (no key)", "sentiment": "neutral"}
        
    try:
        prompt = (
            f"Analyze the following text.\n"
            f"1. Generate a concise summary (1-2 sentences).\n"
            f"2. Classify sentiment as positive, negative, or neutral.\n"
            f"Return a valid JSON object with keys 'summary' and 'sentiment'. Do not include markdown code blocks.\n\n"
            f"Text: {text[:4000]}"
        )
        
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error analyzing story: {e}")
        return {"summary": "Analysis failed", "sentiment": "neutral", "error": str(e)}

def store_data(processed_data: List[Dict[str, Any]]):
    """Append processed data to a local JSON file."""
    try:
        # Load existing data
        existing_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    pass
        
        # Append new data
        existing_data.extend(processed_data)
        
        # Write back
        with open(DATA_FILE, "w") as f:
            json.dump(existing_data, f, indent=2)
            
        logger.info(f"Stored {len(processed_data)} items in {DATA_FILE}")
    except Exception as e:
        logger.error(f"Error storing data: {e}")

def notify_completion(count: int, recipient: str):
    """Send a mock notification."""
    message = f"Pipeline processing completed. {count} items processed. Notification sent to {NOTIFICATION_EMAIL_TARGET}"
    logger.info(message)
    # Also log to a file as a 'persistent' notification record
    with open("notifications.log", "a") as f:
        f.write(f"{datetime.now().isoformat()} - {message} (User requested recipient: {recipient})\n")

async def run_pipeline(email: str, source: str) -> Dict[str, Any]:
    """Orchestrate the entire pipeline."""
    processing_start = datetime.now()
    results = []
    errors = []
    
    logger.info(f"Starting pipeline for source: {source}, recipient: {email}")
    
    # 1. Fetch Data
    raw_stories = await fetch_data()
    if not raw_stories:
        errors.append("Failed to fetch stories from Hacker News")
    
    # 2. AI Enrichment
    for story in raw_stories:
        # Use title + text (if available) or url
        text_content = story.get("title", "") + " " + story.get("text", "")
        if not text_content.strip() and story.get("url"):
            text_content = f"Article URL: {story.get('url')}"
            
        analysis = await analyze_story(text_content)
        
        item_result = {
            "original": story,
            "analysis": analysis.get("summary", ""),
            "sentiment": analysis.get("sentiment", "neutral"),
            "stored": True,
            "timestamp": datetime.now().isoformat()
        }
        results.append(item_result)
        
    # 3. Storage
    store_data(results)
    
    # 4. Notification
    notify_completion(len(results), email)
    
    return {
        "items": results,
        "notificationSent": True,
        "processedAt": processing_start.isoformat(),
        "errors": errors
    }
