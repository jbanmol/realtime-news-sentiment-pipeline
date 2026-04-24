# Realtime News Sentiment Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM_Inference-F55036)
![Hacker News](https://img.shields.io/badge/Hacker_News-Live_Data-FF6600?logo=ycombinator&logoColor=white)
![Sentiment](https://img.shields.io/badge/Sentiment-Analysis-0EA5E9)

FastAPI data pipeline that fetches live Hacker News items and enriches them with LLM-generated sentiment and summaries using Groq-hosted Llama models.

## What This Demonstrates

- API-first data pipeline design
- Live data ingestion from Hacker News
- LLM-based summarization and sentiment enrichment
- Structured JSON outputs for downstream applications
- FastAPI service layer with a lightweight dashboard
- Deployment-oriented project structure

## Architecture

```text
Hacker News API
  -> fetch service
  -> article/comment text extraction
  -> Groq LLM enrichment
  -> structured sentiment + summary output
  -> API/dashboard consumer
```

## Quick Start

```bash
git clone https://github.com/jbanmol/realtime-news-sentiment-pipeline.git
cd realtime-news-sentiment-pipeline
pip install -r requirements.txt
export GROQ_API_KEY=\"your_key_here\"
uvicorn main:app --port 8000 --reload
```

Then open `http://localhost:8000`.

## API Example

```bash
curl -X POST \"http://localhost:8000/process\" \
  -H \"Content-Type: application/json\" \
  -d '{\"email\":\"user@example.com\",\"source\":\"Hacker News\"}'
```

## Tech Stack

Python, FastAPI, Groq API, Llama 3.3, HTML dashboard, Vercel-oriented deployment.

## Next Improvements

- Add durable storage for historical runs
- Add tests for fetch/enrichment failure modes
- Add evaluation examples for summary quality and sentiment consistency
