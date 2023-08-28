from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, UniqueConstraint, and_, select
from sqlalchemy.orm import sessionmaker
import random

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    firstname = Column(String)
    email = Column(String, unique=True)
    __table_args__ = (UniqueConstraint('surname', 'firstname', name='unique_surname_firstname'),)
    accounts = relationship("Account", back_populates="user")

    async def create_user(self, session, surname, firstname, email):
        self.surname = surname
        self.firstname = firstname
        self.email = email
        session.add(self)
        await session.commit()

    @staticmethod
    async def get_user(session, surname, firstname):
        return await session.run_sync(lambda session: session.query(User).filter_by(surname=surname, firstname=firstname).first())

        return await session.query(User).filter_by(surname=surname, firstname=firstname).first()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Float)

    user = relationship("User", back_populates="accounts")
    cards = relationship("Card", back_populates="account")

    async def create_account(self, session, user_id):
        self.user_id = user_id
        self.balance = 0.0  # Initial balance
        session.add(self)
        await session.commit()

    @staticmethod
    async def get_account_by_id(session, account_id):
        return await session.run_sync(lambda session: session.query(Account).filter_by(id=account_id).first())

    
    async def check_balance(session, account_id):
        balance = await session.run_sync(lambda session: session.query(Account).filter_by(id=account_id).first())
        return balance

    async def withdraw(self, amount, session):
        self.balance -= amount
        await session.commit()
        return self.balance

    async def deposit(self, amount, session):
        self.balance += amount
        await session.commit()
        return self.balance

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    test_col = Column(Integer, default=100)
    card_number = Column(Integer)
    enabled = Column(Boolean, default=False)

    account = relationship("Account", back_populates="cards")
    user = relationship("User")

    def luhn_checksum(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
            
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
            
        return checksum % 10

    def generate_card_number(self, bin="123456"):
        first_15_digits = f"{bin}{random.randint(10**(14-len(bin))-1, 10**(15-len(bin))-1)}"
        checksum = self.luhn_checksum(int(first_15_digits))
        last_digit = 10 - checksum if checksum != 0 else 0
        card_number = f"{first_15_digits}{last_digit}"
        return card_number
    
    async def register_card(self, session, account_id, user_id):
        self.user_id = user_id
        self.account_id = account_id
        self.card_number = self.generate_card_number() 
        self.enabled = True 
        session.add(self)
        await session.commit()
        return self.card_number

    @staticmethod
    async def disable_card(session, card_id, account_id, user_id):
        card = await session.run_sync(lambda session: session.query(Card).filter_by(id=card_id, account_id=account_id, user_id=user_id).first())
        if card is None:
            return "Card not found"
        card.enabled = False
        session.add(card)
        await session.commit()
        print(card.enabled)
        return card

    @staticmethod
    async def enable_card(session, card_id, account_id, user_id):
        card = await session.run_sync(lambda session: session.query(Card).filter_by(id=card_id, account_id=account_id, user_id=user_id).first())
        card.enabled = True
        session.add(card)
        await session.commit()
        print("ENABLE: ", card.enabled)
        return card

    @staticmethod
    async def is_enabled(session, card_id, account_id, user_id):
        card = await session.run_sync(lambda session: session.query(Card).filter_by(id=card_id, account_id=account_id, user_id=user_id).first())
        print(card)
        if card is None:
            return "Card not found"
        return card.enabled

