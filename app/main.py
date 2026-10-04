app = FastAPI(
    title="Secure Enterprise Knowledge Assistant",
    description="Enterprise RAG knowledge assistant API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Secure Enterprise Knowledge Assistant API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
