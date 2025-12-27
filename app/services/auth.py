
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()
from app.models.user import User
from app.repositories.user_repository import UserRepository


from app.utils.security import encrypt_data, get_password_hash,decrypt_data
def register_new_user(db,email,firstname,lastname,dob,password,phone):
    dob_date = None
    if dob:
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Handle invalid date format
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")
    user_repo=UserRepository(db)
    user_data = {
        'email':encrypt_data(email),
        'hashed_password':get_password_hash(password),
        'firstname':firstname,
        'lastname':lastname,
        'phone':encrypt_data(phone) if phone else None,
        'dob':dob_date
    }
    return user_repo.create_user(user_data)
    
def authenticate_user(db:Session,email: str, password: str):
    
    try:
        user_repo = UserRepository(db)
        users = user_repo.get_users()
        user=None
        
        for u in users:
            try:
                if decrypt_data(u.email).lower()==email.lower():
                    user=u
                    break
            except Exception as e:
                print(f"Error while decrypt the authectication user email: {e}")
                continue
        if not user or not verify_password(password,user.hashed_password):
            return None
        return  {
            "email":email,
            "firstname":user.firstname,
            "lastname":user.lastname
        }
    except Exception as e:
        print(f"Authentication error: {e}")
        return None
        
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        user_repo = UserRepository(db)
        
        users = user_repo.get_users(skip=skip, limit=limit)
        print("---------------------")
        print(users)
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': decrypt_data(user.email) if user.email else None,
                'phone': decrypt_data(user.phone) if user.phone else None,
                'dob': user.dob.isoformat() if user.dob else None
            })
        
        return {"users": result}
    except Exception as e:
        print(f"Error while fetching users: {e}")
        return None