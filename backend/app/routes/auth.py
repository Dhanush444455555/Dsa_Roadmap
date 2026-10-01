from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserSettings
from app.schemas import UserCreate, UserLogin, Token, UserOut, UserSettingsUpdate, UserSettingsOut
from app.services.auth import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def _build_token_response(user: User, settings: UserSettings) -> dict:
    return {
        "access_token": create_access_token(data={"sub": str(user.id), "email": user.email}),
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "settings": {
                "timezone": settings.timezone,
                "reminder_time": settings.reminder_time,
                "paused": settings.paused,
                "duration_months": settings.duration_months,
                "level": settings.level,
                "daily_count": settings.daily_count,
                "source_type": settings.source_type,
            },
        },
    }


def _ensure_settings(user: User, db: Session) -> UserSettings:
    if user.settings:
        return user.settings
    s = UserSettings(
        user_id=user.id,
        timezone="UTC",
        reminder_time="09:00",
        paused=False,
        duration_months=6,
        level="Average",
        daily_count=1,
        source_type="default",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    user = User(
        email=user_in.email.lower(),
        name=user_in.name.strip(),
        date_of_birth=user_in.date_of_birth,
        hashed_password="",
    )
    db.add(user)
    db.flush()

    settings = UserSettings(
        user_id=user.id,
        timezone="UTC",
        reminder_time="09:00",
        paused=False,
        duration_months=6,
        level="Average",
        daily_count=1,
        source_type="default",
    )
    db.add(settings)
    db.commit()
    db.refresh(user)

    return _build_token_response(user, settings)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Passwordless login: match by email + name + date_of_birth.
    - If no account exists → auto-create one (first login = registration).
    - If account exists → verify name AND date_of_birth match.
    """
    user = db.query(User).filter(User.email == credentials.email.lower()).first()

    if not user:
        # Auto-register on first login
        user = User(
            email=credentials.email.lower(),
            name=credentials.name.strip(),
            date_of_birth=credentials.date_of_birth,
            hashed_password="",
        )
        db.add(user)
        db.flush()
        settings = UserSettings(
            user_id=user.id,
            timezone="UTC",
            reminder_time="09:00",
            paused=False,
            duration_months=6,
            level="Average",
            daily_count=1,
            source_type="default",
        )
        db.add(settings)
        db.commit()
        db.refresh(user)
    else:
        # Verify name matches
        if user.name and user.name.strip().lower() != credentials.name.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Name does not match the email on record.",
            )
        # Verify date of birth matches
        if user.date_of_birth and user.date_of_birth != credentials.date_of_birth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Date of birth does not match the email on record.",
            )

    settings = _ensure_settings(user, db)
    return _build_token_response(user, settings)


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/settings", response_model=UserSettingsOut)
def update_user_settings(
    settings_in: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = current_user.settings
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)

    if settings_in.timezone is not None:
        settings.timezone = settings_in.timezone
    if settings_in.reminder_time is not None:
        settings.reminder_time = settings_in.reminder_time
    if settings_in.paused is not None:
        settings.paused = settings_in.paused
    if settings_in.duration_months is not None:
        settings.duration_months = settings_in.duration_months
    if settings_in.level is not None:
        settings.level = settings_in.level
    if settings_in.daily_count is not None:
        settings.daily_count = settings_in.daily_count
    if settings_in.source_type is not None:
        settings.source_type = settings_in.source_type

    db.commit()
    db.refresh(settings)
    return settings
