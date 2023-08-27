import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.bankAdapter import DatabaseAdapter
from app.bank import Bank

engine = create_engine('sqlite:///../../app/banking.db')
Session = sessionmaker(bind=engine)
session = Session()

db_adapter = DatabaseAdapter(session)
bank_app = Bank()



def account_factory():
    """
    Helper function to create account
    """
    new_user = bank_app.create_user("ena", "test", db_adapter)
    return bank_app.create_account(new_user.id, db_adapter=db_adapter)

def card_factory(account_id):
    """
    Helper function to register card to a user
    """
    return bank_app.register_card(account_id, db_adapter=db_adapter)
    


@pytest.mark.asyncio
async def test_create_user_account():
    """
    Test Account Creating Logic
    """

    #GIVEN
    surname = "So"
    firstname = "Ena"
    email = "ena_1@example.com"
    #WHEN
    new_user = await bank_app.create_user(surname, firstname, email, db_adapter)
    #THEN
    assert new_user.surname == surname
    assert new_user.firstname == firstname

@pytest.mark.asyncio
async def test_register_cards():

    #GIVEN
    _account = account_factory()

    #WHEN
        # Card Registration Logic
    #new_card = await bank_app.register_card(_account.id, db_adapter)
    #THEN
        # Assertion


@pytest.mark.asyncio
async def test_disable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Disabling Logic
    #THEN
        #Assertion

@pytest.mark.asyncio
async def test_enable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Enabling Logic
            
    #THEN
        #Assertion
            


@pytest.mark.asyncio
async def test_deposit_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Saving Logic

    #THEN

@pytest.mark.asyncio
async def test_withdraw_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Withdrawing Logic

    #THEN



@pytest.mark.asyncio
async def test_check_account_balance():
    ...
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Balace checking Logic
            
    #THEN
        #Assertion