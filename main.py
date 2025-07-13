from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime
import os

# Import our custom modules
from database import engine, SessionLocal, Base
from models import User, FormSubmission
from schemas import (
    UserCreate, UserResponse, UserLogin, LoginResponse,
    FormSubmissionCreate, FormSubmissionResponse, FormSubmissionUpdate
)
from auth import verify_token, create_access_token, verify_password, get_password_hash

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API",
    description="API for managing user authentication and form submissions",
    version="1.0.0"
)

security = HTTPBearer()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# API 1: User Authentication API
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with phone number and password
    """
    # Check if user with phone number already exists
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone number already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        phone_number=user.phone_number,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        phone_number=db_user.phone_number,
        full_name=db_user.full_name,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at
    )

@app.post("/api/auth/login", response_model=LoginResponse)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user with phone number and password
    """
    # Find user by phone number
    user = db.query(User).filter(User.phone_number == user_credentials.phone_number).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"user_id": user.id})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            phone_number=user.phone_number,
            full_name=user.full_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
    )

# API 2: Form Submission Management API
@app.post("/api/forms/submit", response_model=FormSubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_form(
    form_data: FormSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a new form with various data fields
    """
    # Create form submission
    db_form = FormSubmission(
        user_id=current_user.id,
        form_type=form_data.form_type,
        title=form_data.title,
        description=form_data.description,
        category=form_data.category,
        priority=form_data.priority,
        status="submitted",
        form_data=form_data.form_data,
        attachments=form_data.attachments,
        submitted_at=datetime.utcnow()
    )
    
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    
    return FormSubmissionResponse(
        id=db_form.id,
        user_id=db_form.user_id,
        form_type=db_form.form_type,
        title=db_form.title,
        description=db_form.description,
        category=db_form.category,
        priority=db_form.priority,
        status=db_form.status,
        form_data=db_form.form_data,
        attachments=db_form.attachments,
        submitted_at=db_form.submitted_at,
        updated_at=db_form.updated_at
    )

@app.get("/api/forms/submissions", response_model=List[FormSubmissionResponse])
def get_user_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    form_type: Optional[str] = None
):
    """
    Get all form submissions for the authenticated user with optional filters
    """
    query = db.query(FormSubmission).filter(FormSubmission.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(FormSubmission.status == status)
    if form_type:
        query = query.filter(FormSubmission.form_type == form_type)
    
    # Get submissions with pagination
    submissions = query.offset(skip).limit(limit).all()
    
    return [
        FormSubmissionResponse(
            id=submission.id,
            user_id=submission.user_id,
            form_type=submission.form_type,
            title=submission.title,
            description=submission.description,
            category=submission.category,
            priority=submission.priority,
            status=submission.status,
            form_data=submission.form_data,
            attachments=submission.attachments,
            submitted_at=submission.submitted_at,
            updated_at=submission.updated_at
        )
        for submission in submissions
    ]

@app.get("/api/forms/submissions/{submission_id}", response_model=FormSubmissionResponse)
def get_submission_by_id(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific form submission by ID
    """
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    return FormSubmissionResponse(
        id=submission.id,
        user_id=submission.user_id,
        form_type=submission.form_type,
        title=submission.title,
        description=submission.description,
        category=submission.category,
        priority=submission.priority,
        status=submission.status,
        form_data=submission.form_data,
        attachments=submission.attachments,
        submitted_at=submission.submitted_at,
        updated_at=submission.updated_at
    )

@app.put("/api/forms/submissions/{submission_id}", response_model=FormSubmissionResponse)
def update_submission(
    submission_id: int,
    form_update: FormSubmissionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a form submission
    """
    submission = db.query(FormSubmission).filter(
        FormSubmission.id == submission_id,
        FormSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form submission not found"
        )
    
    # Update fields
    if form_update.title is not None:
        submission.title = form_update.title
    if form_update.description is not None:
        submission.description = form_update.description
    if form_update.category is not None:
        submission.category = form_update.category
    if form_update.priority is not None:
        submission.priority = form_update.priority
    if form_update.status is not None:
        submission.status = form_update.status
    if form_update.form_data is not None:
        submission.form_data = form_update.form_data
    if form_update.attachments is not None:
        submission.attachments = form_update.attachments
    
    submission.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(submission)
    
    return FormSubmissionResponse(
        id=submission.id,
        user_id=submission.user_id,
        form_type=submission.form_type,
        title=submission.title,
        description=submission.description,
        category=submission.category,
        priority=submission.priority,
        status=submission.status,
        form_data=submission.form_data,
        attachments=submission.attachments,
        submitted_at=submission.submitted_at,
        updated_at=submission.updated_at
    )

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "KPA Form Data API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)