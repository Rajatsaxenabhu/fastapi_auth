from sqlalchemy.orm import Session
from models.user import User,Data
from passlib.context import CryptContext
from schema.user import UserCreate,UserVerify
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        hashed_password = self.hash_password(user_data.password)
        db_user = User(Username=user_data.username, email=user_data.email, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        db_user.password = None  
        return db_user

    def verify_user(self, user_data: UserVerify) -> bool:
        db_user = self.get_user_by_email(user_data.email)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not self.verify_password(user_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        return True

class DataService:
    def __init__(self, db: Session):
        self.db = db
    
    def add_value(self, data: Data) -> Data:
        db_data = Data(name=data.name, age=data.age, Mobile=data.Mobile, email=data.email, gender=data.gender)
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)
        return db_data.id
    
    def delete_value(self, data:int) -> bool:
        db_data = self.db.query(Data).filter(Data.id == data).first()
        if not db_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found"
            )
        self.db.delete(db_data)
        self.db.commit()
        return True