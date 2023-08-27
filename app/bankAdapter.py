from beringbankdb import User, Account, Card

class DatabaseAdapter:
	def __init__(self, session):
		self.session = session
		
	def create_user(self, surname, firstname, email):
		new_user = User()
		new_user.create_user(self.session, surname, firstname, email)
		print(new_user.firstname, new_user.surname)
		return new_user
	
	def get_user(self, firstname: str, surname: str):
		try:
			user = User()
			return user.get_user(self.session, surname, firstname)
		except Exception as e:
			print(f"Error getting user: {e}")
			return None

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

	def withdraw(self, account_id: int, amount: float):
		account = self.session.query(Account).filter_by(id=account_id).first()
		if account and account.balance >= amount:
			account.balance -= amount
			self.session.commit()
			return True
		return False

	def deposit(self, account_id: int, amount: float):
		account = self.session.query(Account).filter_by(id=account_id).first()
		if account:
			account.balance += amount
			self.session.commit()
			return True
		return False

	def check_balance(self, account_id: int):
		account = self.session.query(Account).filter_by(id=account_id).first()
		if account:
			return account.balance
		return 0.0
