# core_logic.py

class Bank:
	def create_user(self, surname, firstname, email, repo):
		return repo.create_user(surname, email, firstname)
		
	def create_account(self, user_id, repo):
		return repo.create_account(user_id)
		
	def register_card(self, account_id, repo):
		return repo.register_card(account_id)

	def disable_card(self, card_id, repo):
		return repo.disable_card(card_id)

	def enable_card(self, card_id, repo):
		return repo.enable_card(card_id)

	def withdraw(self, account_id, amount, repo):
		return repo.withdraw(account_id, amount)

	def deposit(self, account_id, amount, repo):
		return repo.deposit(account_id, amount)

	def check_balance(self, account_id, repo):
		return repo.check_balance(account_id)