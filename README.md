# FastAPI /chat webhook forwarder

Run the app:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

POST JSON to `/chat` with `user_query` and `session_id`:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_query":"Hello","session_id":"abc123"}'
```

The server will forward that JSON to the configured webhook and return the webhook status.
# Rayhan-s-AI-Assistant
