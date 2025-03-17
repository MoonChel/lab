import structlog
from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from starlette.responses import Response

# Configure structlog for JSON logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

app = FastAPI()

# Prometheus Counter
tweet_counter = Counter(
    "telegram_tweets_total",
    "Total tweets processed",
    ["type"]
)

@app.post("/telegram-webhook/")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Update Prometheus counter
    tweet_counter.labels(type=data['msg_type']).inc()

    # Log the received message in JSON format
    logger.info("Received Telegram message", **data)

    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)