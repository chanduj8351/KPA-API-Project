# schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict, Any, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    phone_number: str
    full_name: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Simple phone number validation
        if not v.isdigit() or len(v) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    phone_number: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Form Submission Schemas
class FormSubmissionBase(BaseModel):
    form_type: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: str = "medium"
    form_data: Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None
    
    @validator('form_type')
    def validate_form_type(cls, v):
        allowed_types = ['incident_report', 'feedback', 'request', 'complaint', 'suggestion']
        if v not in allowed_types:
            raise ValueError(f'Form type must be one of: {", ".join(allowed_types)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed_priorities = ['low', 'medium', 'high', 'urgent']
        if v not in allowed_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(allowed_priorities)}')
        return v
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            allowed_categories = ['safety', 'hr', 'it', 'facilities', 'finance', 'general']
            if v not in allowed_categories:
                raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v

class FormSubmissionCreate(FormSubmissionBase):
    pass

class FormSubmissionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    form_data: Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            allowed_priorities = ['low', 'medium', 'high', 'urgent']
            if v not in allowed_priorities:
                raise ValueError(f'Priority must be one of: {", ".join(allowed_priorities)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['submitted', 'in_progress', 'completed', 'rejected']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            allowed_categories = ['safety', 'hr', 'it', 'facilities', 'finance', 'general']
            if v not in allowed_categories:
                raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v

class FormSubmissionResponse(FormSubmissionBase):
    id: int
    user_id: int
    status: str
    submitted_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Error Response Schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# Success Response Schema
class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None