from beringbankdb import User, Account, Card

class DatabaseAdapter:
	def __init__(self, session):
		self.session = session
		
	def create_user(self, surname, firstname, email):
		new_user = User()
		new_user.create_user(self.session, surname, firstname, email)
		print(new_user.firstname, new_user.surname)
		return new_user

	def create_account(self, user_id):
		new_account = Account()
		new_account.create_account(self.session, user_id)
		return new_account

	def register_card(self, account_id):
		new_card = Card()
		new_card.register_card(self.session, account_id)
		return new_card

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
