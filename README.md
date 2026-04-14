# AI News Chatbot

A FastAPI-based news chatbot with:
- an interactive web chat interface
- mock news data (tech, politics, finance)
- REST endpoints for chat and news retrieval

## Features

- Interactive chat UI at `/`
- Chat endpoint at `/chat`
- 30 mock news articles across categories
- Category/news lookup endpoints
- Health check endpoint

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Getting Started

### 1) Clone and enter the project

```bash
git clone https://github.com/MrPhantom2325/news-chatbot.git
cd news-chatbot
```

### 2) Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 3) Run the app

```bash
python main.py
```

The server starts on:
- `http://localhost:8000` (chat UI)
- `http://localhost:8000/docs` (Swagger docs)

## API Endpoints

- `GET /` — Main chat interface
- `POST /chat` — Chat with the bot
- `GET /news` — Get all news articles
- `GET /news/{category}` — Get news by category (`tech`, `politics`, `finance`)
- `GET /news/article/{article_id}` — Get one article by ID
- `GET /health` — Health check

## Example Requests

### Chat

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the latest tech news?","user_preferences":["tech"]}'
```

### News by Category

```bash
curl "http://localhost:8000/news/tech"
```

## Notes

- The project currently uses mock/static news data in `main.py`.
- Host and port are set in `main.py` via `uvicorn.run(app, host="0.0.0.0", port=8000)`.
