from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import User
from schemas import UserCreate, UserLogin
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

# Create tables
User.metadata.create_all(bind=engine)

app = FastAPI()

# JWT Settings
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Database dependency
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
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)

    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is protected data"}
