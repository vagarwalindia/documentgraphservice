from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.v1 import health, documents
from infrastructure.config.settings import settings
from infrastructure.db.database import engine
from infrastructure.kafka.consumer import start_kafka_consumers
from infrastructure.kafka.loader import load_consumers


# -------------------------------
# Lifespan (startup/shutdown)
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Starting application...")

    # Example: DB connection warmup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)
        print("Database connected")
    except Exception as e:
        print(f"Database connection failed : {e}")
        raise

    # Example: initialize Kafka, S3 clients if needed

    start_kafka_consumers()
    # init_s3()

    yield

    # SHUTDOWN
    print("Shutting down application...")

    await engine.dispose()
    print("Database connection closed")


# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(
    title="Document Graph Service",
    version="1.0.0",
    description="Event-driven document graph builder",
    docs_url="/docs" if settings.ENV != "prod" else None,
    redoc_url=None,
    lifespan=lifespan
)


# -------------------------------
# Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# API Routes (Versioned)
# -------------------------------
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])


# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
async def root():
    return {
        "service": "document-graph-service",
        "env": settings.ENV,
        "status": "running"
    }