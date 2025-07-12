from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

# --- Get DB config from environment variables ---
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

DB_HOST = "db"    # This is the service name in docker-compose.yml
DB_PORT = "5432"

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
)

# --- SQLAlchemy setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Define a sample User table ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# --- Create the table in the database ---
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# --- Route to create a user ---
@app.post("/users")
def create_user(name: str):
    db = SessionLocal()
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"id": new_user.id, "name": new_user.name}

# --- Route to get all users ---
@app.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

# --- Root route ---
@app.get("/")
def read_root():
    return {"message": "Hello from SOC_AI_AGENT backend!"}
