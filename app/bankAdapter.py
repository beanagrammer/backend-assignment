from app.beringbankdb import User, Account, Card

class DatabaseAdapter:
    def __init__(self, session):
        self.session = session

    async def create_user(self, surname, firstname, email):
        new_user = User()
        await new_user.create_user(self.session, surname, firstname, email)
        return new_user

    async def get_user(self, firstname: str, surname: str):
        try:
            user = await User.get_user(self.session, surname, firstname)
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def get_accounts(self, user_id):
        accounts = await self.session.run_sync(lambda session: session.query(Account).filter_by(user_id=user_id).all())
        return accounts
    
    async def create_account(self, user_id):
        new_account = Account()
        await new_account.create_account(self.session, user_id)
        return new_account
    

    async def register_card(self, account_id):
        new_card = Card()
        await new_card.register_card(self.session, account_id)
        return new_card
    
    async def get_card(self, account_id):
        card = await self.session.run_sync(lambda session: session.query(Card).filter_by(account_id=account_id).first())
        return card


    async def disable_card(self, card_id, repo):
        return await repo.disable_card(card_id)

    async def enable_card(self, card_id, repo):
        return await repo.enable_card(card_id)

    async def withdraw(self, account_id: int, amount: float):
        account =  await Account.get_account_by_id(self.session, account_id)
        if account and account.balance >= amount:
            account.balance -= amount
            await self.session.commit()
            return True
        return False

    async def deposit(self, account_id: int, amount: float):
        account =  await Account.get_account_by_id(self.session, account_id)
        if account:
            account.balance += amount
            await self.session.commit()
            return True
        return False

    async def check_balance(self, account_id: int):
        print("ADPY: ", account_id)
        account = await  Account.check_balance(self.session, account_id)
        #account = await self.session.query(Account).filter_by(id=account_id).first()
        if account:
            return account.balance
        return 0.0