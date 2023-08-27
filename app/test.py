from bank import Bank
from bankAdapter import DatabaseAdapter
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Initialize database
engine = create_engine('sqlite:///banking.db')

# Assume your models and methods like disable_card, enable_card etc. are already defined

# For this example, import them appropriately
# from models import Account, Card, User

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

bank_app = Bank()
db_adapter = DatabaseAdapter(session)

bank_app.create_user("Gin", "Dan", "d@test.com", db_adapter)