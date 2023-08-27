import logging
from datetime import datetime

from bank import Bank
from bankAdapter import DatabaseAdapter
from beringbankdb import User, Account, Card
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class State:
    def handle(self, context):
        pass

class LoggedOutState(State):
    def handle(self, context):
        print("1: Create User")
        print("2: Login")
        print("9: Quit")
        choice = input("Enter your choice [1 or 2 or 9]: ")
        logging.info(f"User choice: {choice}")
        if choice == '1':
            surname = input("Enter surname: ")
            firstname = input("Enter firstname: ")
            email = input("Enter email: ")
            context.user = context.bank_app.create_user(surname, firstname, email, context.db_adapter)
            context.state = LoggedInState()
            logging.info("Transitioned to LoggedInState.")
        elif choice == '2':
            surname = input("Enter surname: ")
            firstname = input("Enter firstname: ")
            user = context.bank_app.get_user(firstname, surname, context.db_adapter)
            if user:
                context.user = user
                context.state = LoggedInState()
                logging.info("Transitioned to LoggedInState.")
            else:
                logging.info(f"{surname}, {firstname} not found.")
        elif choice == '9':
            logging.info("Goodbye!")
            context.running = False

class LoggedInState(State):
    def handle(self, context):
        logging.info(f"Welcome, {context.user.firstname}")
        print("1: Create Account")
        print("2: Choose Account")
        print("3: Logout")
        print("9: Quit")
        choice = input("Enter your choice: ")
        logging.info(f"User choice: {choice}")
        if choice == '1':
            context.bank_app.create_account(context.user.id, context.db_adapter)
            logging.info("Account successfully created.")
        elif choice == '2':
            accounts = context.db_adapter.session.query(Account).filter_by(user_id=context.user.id).all()
            if accounts:
                for idx, account in enumerate(accounts):
                    logging.info(f"{idx + 1}. Account ID: {account.id}, Balance: {account.balance}")
                account_choice = int(input("Choose an account: ")) - 1
                context.selected_account = accounts[account_choice]
                logging.info(f"Account selected: {context.selected_account.id}")
                context.state = AccountSelectedState()
                logging.info("Transitioned to AccountSelectedState.")
            else:
                logging.info("No accounts found.")
        elif choice == '3':
            context.state = LoggedOutState()
            logging.info("Transitioned to LoggedOutState.")
        elif choice == '9':
            context.state = LoggedOutState()
            logging.info("Transitioned to LoggedOutState.")
            logging.info("Goodbye!")
            context.running = False

class AccountSelectedState(State):
    def handle(self, context):
        logging.info(f"Account ID: {context.selected_account.id}, Balance: {context.selected_account.balance}")
        print("1: Withdraw")
        print("2: Deposit")
        print("3: Register Card")
        print("4: Enable Card")
        print("5: Disable Card")
        print("6: Check Balance")
        print("7: Go back")
        choice = input("Enter your choice: ")
        logging.info(f"User choice: {choice}")
        if choice == '1':
            amount = float(input("Enter amount to withdraw: "))
            logging.info(f"Amount entered: {amount}")
            current_balance = context.bank_app.check_balance(context.selected_account.id, context.db_adapter)
            if amount > current_balance:
                logging.info("Insufficient funds.")
            context.bank_app.withdraw(context.selected_account.id, amount, context.db_adapter)
        elif choice == '2':
            amount = float(input("Enter amount to deposit: "))
            logging.info(f"Amount entered: {amount}")
            context.bank_app.deposit(context.selected_account.id, amount, context.db_adapter)
        elif choice == '3':
            card = context.db_adapter.session.query(Card).filter_by(account_id=context.selected_account.id).first()
            if card:
                logging.info("Card already registered for this account.")
            else:
                context.bank_app.register_card(context.selected_account.id, context.db_adapter)
        elif choice == '4':
            card = context.db_adapter.session.query(Card).filter_by(account_id=context.selected_account.id).first()
            if card and not card.is_enabled:
                context.bank_app.enable_card(card.id, context.db_adapter)
            else:
                logging.info("Card is already enabled or not found.")
        elif choice == '5':
            card = context.db_adapter.session.query(Card).filter_by(account_id=context.selected_account.id).first()
            if card and card.is_enabled:
                context.bank_app.disable_card(card.id, context.db_adapter)
            else:
                logging.info("Card is already disabled or not found.")
        elif choice == "6":
            current_balance = context.bank_app.check_balance(context.selected_account.id, context.db_adapter)
            logging.info(f"Current account balance: {current_balance}")
        elif choice == '7':
            context.state = LoggedInState()
            logging.info("Transitioned to LoggedInState.")

def initialize_database():
    engine = create_engine('sqlite:///banking.db')
    Session = sessionmaker(bind=engine)
    return Session()

class SimulatorContext:
    def __init__(self):
        self.state = LoggedOutState()
        self.user = None
        self.selected_account = None
        self.running = True
        self.session = initialize_database()
        self.bank_app = Bank()
        self.db_adapter = DatabaseAdapter(self.session)

    def run(self):
        while self.running:
            try:
                self.state.handle(self)
            except Exception as e:
                logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    from logging.handlers import TimedRotatingFileHandler
    # Define the logging configuration
    log_filename = f"../log/bering_bank.log"
    handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)
    stream_handler = logging.StreamHandler()

    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #stream_handler.setFormatter(formatter)
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler, stream_handler], level=logging.INFO)

    SimulatorContext().run()