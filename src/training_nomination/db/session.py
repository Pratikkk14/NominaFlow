"""Database engine, session management, initialization and seeding."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from training_nomination.config import settings
from training_nomination.db.base import Base
from training_nomination.models.audit_event import AuditEvent  # noqa: F401
from training_nomination.models.document import Document  # noqa: F401
from training_nomination.models.nomination import TrainingNomination  # noqa: F401
from training_nomination.models.role import Role, RoleType
from training_nomination.models.user import User

# Engine creation: handles sqlite threading and pool settings
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_initial_data(db: Session) -> None:
    """Seed baseline roles and demo user accounts for friction-free evaluation."""
    from training_nomination.core.security import get_password_hash

    # 1. Seed Roles
    roles_map: dict[str, Role] = {}
    for role_type in RoleType:
        role = db.query(Role).filter(Role.name == role_type.value).first()
        if not role:
            role = Role(name=role_type.value)
            db.add(role)
            db.flush()
        roles_map[role_type.value] = role

    # 2. Seed Default Demo Users
    demo_users = [
        {
            "name": "Alex Mercer (Employee)",
            "email": "employee@nominaflow.com",
            "password": "password123",
            "role_name": RoleType.EMPLOYEE.value,
        },
        {
            "name": "Sarah Jenkins (Reviewer)",
            "email": "reviewer@nominaflow.com",
            "password": "password123",
            "role_name": RoleType.REVIEWER.value,
        },
        {
            "name": "Admin User (Administrator)",
            "email": "admin@nominaflow.com",
            "password": "password123",
            "role_name": RoleType.ADMIN.value,
        },
    ]

    for user_info in demo_users:
        existing_user = db.query(User).filter(User.email == user_info["email"]).first()
        if not existing_user:
            new_user = User(
                name=user_info["name"],
                email=user_info["email"],
                password_hash=get_password_hash(user_info["password"]),
                role_id=roles_map[user_info["role_name"]].id,
            )
            db.add(new_user)

    db.commit()


def init_db() -> None:
    """Create all tables and seed default data."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_initial_data(db)
