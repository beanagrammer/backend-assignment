# Welcome To Beringlab Coding Assignment!

## Bering Bank
Build a simulation of 'Bering Bank' that allows users to perform the following operations:
- Create user account
- Register cards(plural!)
- Disable card
- Enable card
- Check account balance
- Withdraw cash
- Deposit cash

## You can:
- Use ANY Relational Database you prefer.
- Install dependencies you find necessary.

## To qualify your expertise you are to:
- Write code under 'app' project
- Complete the tests(using pytest)


## Extra Credit
- Use Port and Adapater architecture(To qualify your seniority.)
- Apply 'State pattern' to manage card's state (reference: https://refactoring.guru/design-patterns/state/python/example)
- Proper implementation of logging
- Special case handling(Be creative!) such as event notification on withdrawal of money that's more than a certain amount of money.

### How to Run the Simulator 
```
python3 app/load_database.py # Runs ORM to load models
python3 -v # should be running <= 3.11.1
pip install -r requirements.txt
python3 -m app.async_simulator
```

### How to Run the Test
```
pytest -v --log-level=DEBUG
```
Tet Result 
![Example Image](./tests/Screenshot%202023-08-28%20at%2009.15.23.png)

