# core_logic.py

class Bank:
	def create_user(self, surname, firstname, email, adapter):
		return adapter.create_user(surname, firstname, email)
		
	def create_account(self, user_id, adapter):
		return adapter.create_account(user_id)

	def get_user(self, firstname: str, surname: str, adapter):
		return adapter.get_user(firstname, surname)

	def register_card(self, account_id, adapter):
		return adapter.register_card(account_id)

	def disable_card(self, card_id, adapter):
		return adapter.disable_card(card_id)

	def enable_card(self, card_id, adapter):
		return adapter.enable_card(card_id)

	def withdraw(self, account_id: int, amount: float, adapter):
		return adapter.withdraw(account_id, amount)

	def deposit(self, account_id: int, amount: float, adapter):
		return adapter.deposit(account_id, amount)

	def check_balance(self, account_id: int, adapter):
		return adapter.check_balance(account_id)