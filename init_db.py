# init_db.py
from database import Base, engine
import models

# This will create all tables based on your models
Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully.")
