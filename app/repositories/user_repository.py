from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Dict, Any
from app.models.user import User
from app.utils.security import decrypt_data
import logging


# Set up logging
logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user with encrypted data.
        
        Args:
            user_data: Dictionary containing user data (email, hashed_password, etc.)
            
        Returns:
            User: The created user object
            
        Raises:
            ValueError: If user with email already exists
            Exception: For other database errors
        """
        try:
            if self.email_exists(user_data.get('email')):
                raise ValueError("Email already registered")
                
            user = User(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User created with email: {user_data.get('email')}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise

    # Read
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email (case-insensitive with decryption).
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        # First try exact match (common case)
        user = self.db.query(User).filter(User.email.ilike(f"%{email}%")).first()
        if user:
            try:
                if decrypt_data(user.email).lower() == email.lower():
                    return user
            except Exception as e:
                logger.warning(f"Error decrypting email for user {user.id}: {str(e)}")
        
        # If not found, fall back to checking all users
        users = self.db.query(User).all()
        for user in users:
            try:
                if decrypt_data(user.email).lower() == email.lower():
                    return user
            except Exception as e:
                logger.warning(f"Error decrypting email for user {user.id}: {str(e)}")
                continue
        return None

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get multiple users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of users
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    # Update
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """Update a user's information.
        
        Args:
            user_id: The ID of the user to update
            user_data: Dictionary of fields to update
            
        Returns:
            Optional[User]: The updated user if found, None otherwise
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
                
            for key, value in user_data.items():
                # Don't update the ID
                if key == 'id':
                    continue
                setattr(user, key, value)
                
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User {user_id} updated")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise

    # Delete
    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if user was deleted, False if user not found
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
                
            self.db.delete(user)
            self.db.commit()
            logger.info(f"User {user_id} deleted")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise

    # Business Logic
    def email_exists(self, email: str) -> bool:
        """Check if a user with the given email exists.
        
        Args:
            email: The email to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        return self.get_user_by_email(email) is not None

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password.
        
        Args:
            email: The user's email
            password: The plain text password to verify
            
        Returns:
            Optional[User]: The authenticated user if successful, None otherwise
        """
        from app.services.auth import verify_password
        
        user = self.get_user_by_email(email)
        if not user:
            logger.warning(f"Login attempt failed for non-existent email: {email}")
            return None
            
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password attempt for user: {email}")
            return None
            
        logger.info(f"User authenticated: {email}")
        return user