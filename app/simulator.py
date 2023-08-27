from bank import Bank
from bankAdapter import DatabaseAdapter
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Initialize database
engine = create_engine('sqlite:///banking.db')

# Assume your models and methods like disable_card, enable_card etc. are already defined
# For this example, import them appropriately
# from models import Account, Card, User

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Initialize core logic and adapter
bank_app = Bank()
db_adapter = DatabaseAdapter(session)

while True:
    print("1: Create User")
    print("2: Create Account")
    print("3: Register Card")
    print("4: Disable Card")
    print("5: Enable Card")
    print("6: Withdraw")
    print("7: Deposit")
    print("8: Check Balance")
    print("9: Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        surname = input("Enter surname: ")
        firstname = input("Enter firstname: ")
        email = input("Enter email: ")
        bank_app.create_user(surname, firstname, email, db_adapter)

    elif choice == '2':
        user_id = int(input("Enter User ID: "))
        bank_app.create_account(user_id, db_adapter)

    elif choice == '3':
        account_id = int(input("Enter Account ID: "))
        bank_app.register_card(account_id, db_adapter)

    elif choice == '4':
        card_id = int(input("Enter Card ID: "))
        bank_app.disable_card(card_id, db_adapter)

    elif choice == '5':
        card_number = int(input("Enter Card Number: "))
        card_no = bank_app.enable_card(card_number, db_adapter)
        print(f"Card {card_no} is registered")

    elif choice == '6':
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter amount to withdraw: "))
        bank_app.withdraw(account_id, amount, db_adapter)

    elif choice == '7':
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter amount to deposit: "))
        bank_app.deposit(account_id, amount, db_adapter)

    elif choice == '8':
        account_id = int(input("Enter Account ID: "))
        balance = bank_app.check_balance(account_id, db_adapter)
        print(f"Account balance: {balance}")

    elif choice == '9':
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
