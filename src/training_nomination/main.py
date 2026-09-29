"""NominaFlow Main Application Entry Point.

Centralized Training Nomination Workflow Application combining FastAPI REST API
and interactive responsive Web UI.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from training_nomination.api.admin import router as admin_router
from training_nomination.api.auth import router as auth_router
from training_nomination.api.documents import router as documents_router
from training_nomination.api.nominations import router as nominations_router
from training_nomination.api.reviewer import router as reviewer_router
from training_nomination.config import settings
from training_nomination.core.dependencies import get_current_user_optional
from training_nomination.db.session import init_db
from training_nomination.models.user import User

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context initializing DB schema and demo seed data."""
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Centralized Training Nomination Workflow Management System",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware for open testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include API Routers
app.include_router(auth_router)
app.include_router(nominations_router)
app.include_router(documents_router)
app.include_router(reviewer_router)
app.include_router(admin_router)


# ---------------------------------------------------------------------------
# Frontend Web Routes
# ---------------------------------------------------------------------------


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Health check endpoint for liveness and deployment verification."""
    return {
        "status": "healthy",
        "service": "training_nomination",
        "version": settings.APP_VERSION,
    }


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    current_user: User | None = Depends(get_current_user_optional),
):
    """Root redirecting to role portal if authenticated, or login screen."""
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    role_name = current_user.role.name if current_user.role else "EMPLOYEE"
    if role_name == "EMPLOYEE":
        return RedirectResponse(url="/employee", status_code=status.HTTP_302_FOUND)
    elif role_name == "REVIEWER":
        return RedirectResponse(url="/reviewer", status_code=status.HTTP_302_FOUND)
    elif role_name == "ADMIN":
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    return RedirectResponse(url="/employee", status_code=status.HTTP_302_FOUND)


@app.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    current_user: User | None = Depends(get_current_user_optional),
):
    """Render user authentication screen."""
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"current_user": None},
    )


@app.get("/employee", response_class=HTMLResponse)
def employee_page(
    request: Request,
    current_user: User | None = Depends(get_current_user_optional),
):
    """Render Employee training nomination portal."""
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="employee.html",
        context={"current_user": current_user},
    )


@app.get("/reviewer", response_class=HTMLResponse)
def reviewer_page(
    request: Request,
    current_user: User | None = Depends(get_current_user_optional),
):
    """Render Reviewer evaluation portal."""
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="reviewer.html",
        context={"current_user": current_user},
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_page(
    request: Request,
    current_user: User | None = Depends(get_current_user_optional),
):
    """Render Administrator dashboard."""
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"current_user": current_user},
    )

