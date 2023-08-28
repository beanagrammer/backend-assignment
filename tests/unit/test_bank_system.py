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

def card_factory(session, account_id, user_id):
    """
    Helper function to register card to a user
    """
    db_adapter = DatabaseAdapter(session)
    bank_app = Bank()
    return  bank_app.register_card(account_id, user_id, db_adapter)

@pytest.mark.asyncio
async def test_create_user_account(session):
    """
    Test Account Creating Logic
    """
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
    firstname = "Sam"
    email = "lsam@test.com"
    _user = await user_factory(session, surname, firstname, email)
    _account = await account_factory(session, _user.id)
    #WHEN
        # Card Registration Logic
    _card = await card_factory(session, _account.id, _user.id)
    #THEN
    assert _card is not None
    assert _account.id == _card.account_id


@pytest.mark.asyncio
async def test_disable_card(session):
    #GIVEN
    surname = "Lee"
    firstname = "Sam"
    email = "lsam@test.com"
    bank_app = Bank()
    db_adapter = DatabaseAdapter(session)
    _user = await bank_app.get_user(surname=surname, firstname=firstname, adapter=db_adapter)
    _account = await bank_app.get_accounts(_user.id, db_adapter)
    _card = await bank_app.get_card(_account[0].id, db_adapter)

    #WHEN
    await bank_app.disable_card(_card.id, _account[0].id, _user.id, db_adapter)
    is_enabled = await bank_app.is_enabled(_card.id, _account[0].id, _user.id, db_adapter)
    #THEN
    assert is_enabled is not True

@pytest.mark.asyncio
async def test_enable_card(session):
    #GIVEN
    surname = "Lee"
    firstname = "Sam"
    email = "lsam@test.com"
    bank_app = Bank()
    db_adapter = DatabaseAdapter(session)
    _user = await bank_app.get_user(surname=surname, firstname=firstname, adapter=db_adapter)
    _account = await bank_app.get_accounts(_user.id, db_adapter)
    _card = await bank_app.get_card(_account[0].id, db_adapter)

    #WHEN
    await bank_app.enable_card(_card.id, _account[0].id, _user.id, db_adapter)
    is_enabled = await bank_app.is_enabled(_card.id, _account[0].id, _user.id, db_adapter)      
    #THEN
    assert is_enabled is True
            


@pytest.mark.asyncio
async def test_deposit_cash(session):
    #GIVEN
    surname = "Lee"
    firstname = "Sam"
    bank_app = Bank()
    db_adapter = DatabaseAdapter(session)
    _user = await bank_app.get_user(surname=surname, firstname=firstname, adapter=db_adapter)
    _account = await bank_app.get_accounts(_user.id, db_adapter)
    _amount = 50
    #WHEN
    init_bal = await bank_app.check_balance(_account[0].id, db_adapter)
    await bank_app.deposit(_account[0].id, _amount, db_adapter)
    new_bal = await bank_app.check_balance(_account[0].id, db_adapter)
    #THEN
    assert init_bal + _amount == new_bal


@pytest.mark.asyncio
async def test_withdraw_cash(session):
    #GIVEN
    surname = "Lee"
    firstname = "Sam"
    bank_app = Bank()
    db_adapter = DatabaseAdapter(session)
    _user = await bank_app.get_user(surname=surname, firstname=firstname, adapter=db_adapter)
    _account = await bank_app.get_accounts(_user.id, db_adapter)
    _amount = 30

    #WHEN
    init_bal = await bank_app.check_balance(_account[0].id, db_adapter)
    await bank_app.withdraw(_account[0].id, _amount, db_adapter)
    new_bal = await bank_app.check_balance(_account[0].id, db_adapter)

    #THEN
    assert init_bal - _amount == new_bal



@pytest.mark.asyncio
async def test_check_account_balance(session):
    ...
    #GIVEN
    surname = "Lee"
    firstname = "Sam"
    bank_app = Bank()
    db_adapter = DatabaseAdapter(session)
    _user = await bank_app.get_user(surname=surname, firstname=firstname, adapter=db_adapter)
    _account = await bank_app.get_accounts(_user.id, db_adapter)

    #WHEN
    balance = await bank_app.check_balance(_account[0].id, db_adapter)
            
    #THEN
    assert balance is not None