class Bank:
    async def create_user(self, surname, firstname, email, adapter):
        return await adapter.create_user(surname, firstname, email)

    async def create_account(self, user_id, adapter):
        return await adapter.create_account(user_id)
    
    async def get_accounts(self, user_id, adapter):
        return await adapter.get_accounts(user_id)

    async def get_user(self, firstname: str, surname: str, adapter):
        return await adapter.get_user(firstname, surname)

    async def register_card(self, account_id, adapter):
        return await adapter.register_card(account_id)
    
    async def get_card(self, account_id, adapter):
        return await adapter.get_card(account_id)

    async def disable_card(self, card_id, adapter):
        return await adapter.disable_card(card_id)

    async def enable_card(self, card_id, adapter):
        return await adapter.enable_card(card_id)

    async def withdraw(self, account_id: int, amount: float, adapter):
        return await adapter.withdraw(account_id, amount)

    async def deposit(self, account_id: int, amount: float, adapter):
        return await adapter.deposit(account_id, amount)

    async def check_balance(self, account_id: int, adapter):
        print("APP: ", account_id, adapter)
        return await adapter.check_balance(account_id)