from sqlalchemy import Column, Integer, String, Date
from ..config.db import Base  # Updated import to use relative import

class User(Base):
    """
    User model representing a user in the system.
    
    Attributes:
        id: Primary key
        firstname: User's first name
        lastname: User's last name
        email: User's email (unique)
        hashed_password: Hashed password
        dob: Date of birth (optional)
        phone: Phone number (optional, max 15 chars)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)  # bcrypt hash is 60 chars, but leaving room
    dob = Column(Date, nullable=True)
    phone = Column(String(15), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"