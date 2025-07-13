# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship 
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with form submissions
    form_submissions = relationship("FormSubmission", back_populates="user")

class FormSubmission(Base):
    __tablename__ = "form_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    form_type = Column(String(50), nullable=False)  # e.g., "incident_report", "feedback", "request"
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # e.g., "safety", "hr", "it"
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, urgent
    status = Column(String(20), nullable=False, default="submitted")  # submitted, in_progress, completed, rejected
    form_data = Column(JSON, nullable=True)  # Store dynamic form fields as JSON
    attachments = Column(JSON, nullable=True)  # Store file paths/URLs as JSON array
    submitted_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with user
    user = relationship("User", back_populates="form_submissions")