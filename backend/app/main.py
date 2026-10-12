import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .models import AssessmentResponse, SymptomAssessmentRequest
from .services.ai_service import AIService

# Configure application logging
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("healthguide.api")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Safety-first health information and warning sign recognition prototype.",
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AIService()


@app.middleware("http")
async def privacy_preserving_access_log(request: Request, call_next):
    """
    Privacy-first access log middleware:
    Guarantees that full symptom text and personal health descriptions are NEVER logged to console or disk.
    Only logs sanitized metadata: method, path, status, and elapsed time.
    """
    start_time = time.time()
    response = await call_next(request)
    elapsed = (time.time() - start_time) * 1000

    logger.info(
        "Request: %s %s -> Status: %d (%.1f ms)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Clean validation error response without leaking internals."""
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err.get("loc", []) if x != "body"])
        msg = err.get("msg", "Invalid value")
        errors.append(f"{loc}: {msg}" if loc else msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation failed",
            "details": errors,
            "message": "Please ensure all required symptom fields are correctly filled within valid limits.",
        },
    )


@app.get("/api/health")
async def health_check():
    """Service health and diagnostic status."""
    ai_available = bool(
        (settings.ai_provider == "GEMINI" and settings.gemini_api_key)
        or (settings.ai_provider == "OPENAI" and settings.openai_api_key)
    )
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "ai_enabled": ai_available,
        "ai_provider": settings.ai_provider if ai_available else "none_deterministic_fallback",
        "supported_languages": ["en", "ta"],
    }


@app.post("/api/assess", response_model=AssessmentResponse)
async def assess_symptoms(request: SymptomAssessmentRequest):
    """
    Symptom assessment endpoint with safety-first emergency triage.
    Executes deterministic warning-sign detection first before any optional AI processing.
    """
    result = await ai_service.assess(request)
    
    # Audit log entry with privacy masking (no raw symptom text logged)
    logger.info(
        "Triage complete: age=%s severity=%s duration=%s urgency=%s is_emergency=%s lang=%s",
        request.age_range.value,
        request.severity.value,
        request.duration.value,
        result.urgency_level.value,
        result.is_emergency,
        request.language.value,
    )

    return result
