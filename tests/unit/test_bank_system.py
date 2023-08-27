import pytest
from app.bank import Bank
from app.bankAdapter import DatabaseAdapter


def user_factory(session, surname, firstname, email):
    db_adapter = DatabaseAdapter(session)
    bank_app = Bank()
    return bank_app.create_user(surname, firstname, email,db_adapter)

def account_factory(session, user_id):
    """
    Helper function to create account
    """
    db_adapter = DatabaseAdapter(session)
    bank_app = Bank()
    return bank_app.create_account(user_id, adapter=db_adapter)

def card_factory(session, account_id):
    """
    Helper function to register card to a user
    """
    db_adapter = DatabaseAdapter(session)
    bank_app = Bank()
    return  bank_app.register_card(account_id, db_adapter)

@pytest.mark.asyncio
async def test_create_user_account(session):
    """
    Test Account Creating Logic
    """
    print(session)
    #GIVEN
    surname = "Gin"
    firstname = "Dan"
    email = "gin@test.com"
    _user = await user_factory(session, surname, firstname, email)
    #WHEN
    _account = await account_factory(session, _user.id)
    #THEN
    assert _user.id == _account.user_id

@pytest.mark.asyncio
async def test_register_cards(session):

    #GIVEN
    surname = "Lee"
    firstname = "Jim"
    email = "jim@test.com"
    _user = await user_factory(session, surname, firstname, email)
    _account = await account_factory(session, _user.id)
    #WHEN
        # Card Registration Logic
    _card = await card_factory(session, _account.id)
    #THEN
    assert _card is not None
    assert _account.id == _card.account_id


@pytest.mark.asyncio
async def test_disable_card(session):
    #GIVEN
    surname = "Strongman"
    firstname = "Kev"
    email = "kev_s@test.com"
    _user = await user_factory(session, surname, firstname, email)
    _account = await account_factory(session, _user.id)
    _card = card_factory(account_id=_account.id)

    #WHEN
    db_adapter = DatabaseAdapter(session)
    bank_app = Bank()
    _disable = await bank_app.disable_card(_card.id, db_adapter)
    #THEN
    assert _disable.is_enabled is not True

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