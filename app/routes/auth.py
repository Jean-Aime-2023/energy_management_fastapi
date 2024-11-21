from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "8f0f5ea1f80df5cadb1878fa82294fe5109b0b518c460faebbe788cda69458bbb552640749000eecc399cf59c887ce908eabdd7f1ad79eaf71ebb8fcac245c34"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create token
def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Decode token
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# create user
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create a new User instance, excluding the password from user.dict()
    user_data = user.dict(exclude={"password"})  # Exclude the password field from user.dict()
    new_user = User(**user_data, password=hashed_password)  # Pass the hashed password explicitly
    
    # Add the new user to the database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "User created successfully"}


# Login user
@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# Dependency to get current user
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    print("Authorization Header: ", authorization)  # Add this line to log the header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# Check if the user is an admin
def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True