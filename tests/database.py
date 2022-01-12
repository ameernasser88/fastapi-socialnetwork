import pytest
from jose import jwt
from app import schemas
from app.database import get_db
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:aa00000000@postgres:5432/fastapi_social_network_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

