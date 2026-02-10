# DataFlow Systems - Intelligent Data Pipeline

A real-time data enrichment pipeline that fetches top stories from **Hacker News**, analyzes them using **Groq's LPU™ Inference Engine (Llama 3.3 70B)**, and delivers structured insights via a modern web interface and API.

![DataFlow Systems](https://placehold.co/1200x400/0f172a/38bdf8?text=DataFlow+Systems+Architecture)

## 🚀 Features

-   **Live Data Ingestion**: Fetches the latest top stories from the Hacker News API.
-   **AI Enrichment**: Uses `llama-3.3-70b-versatile` on Groq to generate concise summaries and sentiment analysis in milliseconds.
-   **Modern UI**: Glassmorphism-styled dashboard with a real-time system architecture visualization.
-   **API-First**: Exposes a RESTful `/process` endpoint for integration.
-   **Vercel Ready**: configured for serverless deployment with `api/index.py`.

## 🛠️ Architecture

1.  **Extract**: Pull top story IDs and metadata from Hacker News.
2.  **Transform**:
    *   Construct context from titles and text.
    *   **AI Analysis**: Send prompts to Groq API.
    *   Parse JSON response (Summary + Sentiment).
3.  **Load**: Store enriched data to `data.json` (or `/tmp` in serverless) and trigger notifications.

## 📦 Installation

### Prerequisites
-   Python 3.10+
-   `uv` (recommended) or `pip`
-   Groq API Key

### Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jbanmol/fetch-analyse_sentiment.git
    cd fetch-analyse_sentiment
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    # OR
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    Create a `.env.local` file:
    ```env
    GROQ_API_KEY=gsk_...
    ```

## ⚡ Usage

### Run Locally
Start the FastAPI server:
```bash
uv run uvicorn main:app --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** to view the dashboard.

### API Endpoint
Trigger the pipeline via curl:
```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "source": "Hacker News"}'
```

## ☁️ Deployment (Vercel)

This project is configured for Vercel.

1.  Install Vercel CLI: `npm i -g vercel`
2.  Deploy: `vercel --prod`
3.  Set `GROQ_API_KEY` in Vercel Project Settings > Environment Variables.

## 📄 License
MIT
