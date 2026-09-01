"""NominaFlow Application Entry Point.

Week 4 Milestone: Initial Python application skeleton and health check probe.
Business logic, database persistence, and workflow services will be introduced
incrementally in subsequent development sprints.
"""

from fastapi import FastAPI

app = FastAPI(
    title="NominaFlow - Training Nomination Workflow",
    description="Centralized Training Nomination Workflow Management System",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Root endpoint providing service identification."""
    return {
        "project": "NominaFlow",
        "description": "Training Nomination Workflow System",
        "status": "Repository Initialized",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint for liveness and deployment verification."""
    return {
        "status": "healthy",
        "service": "training_nomination",
    }
