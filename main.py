
from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

url_connection = settings.database_url
engine = create_engine(url_connection)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

class Business(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    password: str
    address: str

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!", "status": 200}

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.post("/signup", response_model=Business)
def signup(business: Business, session: session_dep):
    print(business)
    return {"message": "Business signed up successfully", "status": 201}