# scripts/create_user.py
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import get_password_hash
from app.repositories.session import SessionLocal  # Fixed path
from app.models.user import User  # This might also need fixing

def create_test_user():
    # Create database session
    db = SessionLocal()

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_user:
            print("User already exists!")
            return

        # Create new user with hashed password
        hashed_password = get_password_hash("password123")
        new_user = User(
            email="admin@example.com",
            password_hash=hashed_password,
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"User created successfully!")
        print(f"Email: admin@example.com")
        print(f"Password: password123")
        print(f"User ID: {new_user.id}")

    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()