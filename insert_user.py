from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import get_password_hash

# Create DB session
db: Session = SessionLocal()

# Define a new user with correct fields
new_user = User(
    phone_number="12345675",
    full_name="Test User",
    email="testuser@example.com",
    hashed_password=get_password_hash("testpass123")
)

# Add and commit
db.add(new_user)
db.commit()
print("✅ User inserted successfully!")
