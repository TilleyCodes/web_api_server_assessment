# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=bad-indentation

from datetime import date

from flask import Blueprint

from init import db
from models import User, Stock, Order, Portfolio, Transaction, Watchlist
from enums import OrderType, OrderStatus, TransactionType


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
     users = [
          User(f_name="Papa",
               l_name="Li",
               email="papali@email.com",
               account_open_date=date(2020,3,14),
               account_balance=4521546.22
          ),
          User(f_name="Mama",
               l_name="Ti",
               email="mamati@email.com",
               account_open_date=date(2021,11,8),
               account_balance=256349.12
          ),
          User(f_name="Yogi",
               l_name="Bear",
               email="yogibear@email.com",
               account_open_date=date(2022,8, 7),
               account_balance=803241.69
          ),
          User(f_name="Pepe",
               l_name="Poo",
               email="pepepoo@email.com",
               account_open_date=date(2022,11,7),
               account_balance=4521546.22
          ),
          User(f_name="Bandit",
               l_name="Boy",
               email="banditboy@email.com",
               account_open_date=date(2024,5,8),
               account_balance=4512.58
               )
     ]

     db.session.add_all(users)

     stocks = [
          Stock(stock_name="Commonwealth Bank",
               ticker="CBA",
               stock_price=142.93
          ),
          Stock(stock_name="CSL Limited",
               ticker="CSL",
               stock_price=287.46
          ),
          Stock(stock_name="ANZ Group Holdings Limited",
               ticker="ANZ",
               stock_price=31.22
          ),
          Stock(stock_name="Westpac Banking Group",
               ticker="WBC",
               stock_price=32.01
          ),
          Stock(stock_name="Rio Tinto",
               ticker="RIO",
               stock_price=120.31
          ),
          Stock(stock_name="Macquarie Group Limited",
               ticker="MQG",
               stock_price=231.37
          ),
          Stock(stock_name="Telstra Group Limited",
               ticker="TLS",
               stock_price=3.83
          ),
          Stock(stock_name="Xero",
               ticker="XRO",
               stock_price=150.00
          ),
          Stock(stock_name="ResMed Inc",
               ticker="RMD",
               stock_price=37.32
          ),
          Stock(stock_name="Coles Group Limited",
               ticker="COL",
               stock_price=17.70
          )
     ]

     db.session.add_all(stocks)

     db.session.commit() # flossing

     orders = [
          Order(trade_date=date(2024,10,30),
               order_type=OrderType.BUY,
               quantity=50,
               net_amount=7146.50,
               order_status=OrderStatus.PENDING,
               user_id=5,
               stock_id=1,
          ),
          Order(trade_date=date(2024,6,4),
               order_type=OrderType.BUY,
               quantity=42,
               net_amount=4210.85,
               order_status=OrderStatus.EXECUTED,
               user_id=2,
               stock_id=5,
          ),
          Order(trade_date=date(2024,1,6),
               order_type=OrderType.BUY,
               quantity=20,
               net_amount=354.00,
               order_status=OrderStatus.EXECUTED,
               user_id=3,
               stock_id=10,
          ),
          Order(trade_date=date(2023,12,22),
               order_type=OrderType.BUY,
               quantity=10,
               net_amount=373.20,
               order_status=OrderStatus.EXECUTED,
               user_id=4,
               stock_id=9,
          ),
          Order(trade_date=date(2023,12,12),
               order_type=OrderType.BUY,
               quantity=12,
               net_amount=2776.44,
               order_status=OrderStatus.EXECUTED,
               user_id=1,
               stock_id=6,
          ),
          Order(trade_date=date(2023,12,6),
               order_type=OrderType.BUY,
               quantity=15,
               net_amount=468.30,
               order_status=OrderStatus.EXECUTED,
               user_id=4,
               stock_id=3,
          ),
          Order(trade_date=date(2023,11,4),
               order_type=OrderType.BUY,
               quantity=20,
               net_amount=3000.00,
               order_status=OrderStatus.EXECUTED,
               user_id=3,
               stock_id=8,
          ),
          Order(trade_date=date(2023,10,18),
               order_type=OrderType.BUY,
               quantity=63,
               net_amount=241.29,
               order_status=OrderStatus.EXECUTED,
               user_id=2,
               stock_id=7,
          ),
          Order(trade_date=date(2023,9,23),
               order_type=OrderType.BUY,
               quantity=8,
               net_amount=1850.96,
               order_status=OrderStatus.EXECUTED,
               user_id=2,
               stock_id=6,
          ),
          Order(trade_date=date(2023,9,19),
               order_type=OrderType.BUY,
               quantity=72,
               net_amount=2247.84,
               order_status=OrderStatus.EXECUTED,
               user_id=1,
               stock_id=3
          )
     ]

     db.session.add_all(orders)

     portfolios = [
          Portfolio(number_of_units=20,
                    user_id=2,
                    stock_id=2,
          ),
          Portfolio(number_of_units=15,
                    user_id=4,
                    stock_id=3,
          ),
          Portfolio(number_of_units=42,
                    user_id=5,
                    stock_id=4,
          ),
          Portfolio(number_of_units=35,
                    user_id=2,
                    stock_id=5,
          ),
          Portfolio(number_of_units=20,
                    user_id=3,
                    stock_id=10,
          ),
          Portfolio(number_of_units=12,
                    user_id=1,
                    stock_id=6,
          ),
          Portfolio(number_of_units=20,
                    user_id=3,
                    stock_id=8,
          ),
          Portfolio(number_of_units=10,
                    user_id=4,
                    stock_id=9,
          ),
          Portfolio(number_of_units=63,
                    user_id=2,
                    stock_id=7,
          ),
          Portfolio(number_of_units=8,
                    user_id=2,
                    stock_id=6,
          ),
          Portfolio(number_of_units=72,
                    user_id=1,
                    stock_id=3,
          )
     ]

     db.session.add_all(portfolios)

     transactions = [
          Transaction(transaction_date=date(2024,10,30),
                      transaction_type=TransactionType.BUY,
                      amount=7146.50,
                      user_id=5,
                      order_id=1,
          ),
          Transaction(transaction_date=date(2024,10,30),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=7146.50,
                      user_id=5,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2024,6,14),
                      transaction_type=TransactionType.BUY,
                      amount=1344.42,
                      user_id=5,
                      order_id=4,
          ),
          Transaction(transaction_date=date(2024,5,12),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=5857,
                      user_id=5,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2024,3,12),
                      transaction_type=TransactionType.BUY,
                      amount=5749.20,
                      user_id=2,
                      order_id=2,
          ),
          Transaction(transaction_date=date(2024,3,20),
                      transaction_type=TransactionType.SELL,
                      amount=468.30,
                      user_id=4,
                      order_id=3,
          ),
          Transaction(transaction_date=date(2024,2,3),
                      transaction_type=TransactionType.BUY,
                      amount=4210.85,
                      user_id=2,
                      order_id=5,
          ),
          Transaction(transaction_date=date(2024,1,6),
                      transaction_type=TransactionType.BUY,
                      amount=354.00,
                      user_id=3,
                      order_id=10,
                                          ),
          Transaction(transaction_date=date(2024,1,4),
                      transaction_type=TransactionType.WITHDRAWAL,
                      amount=5000,
                      user_id=1,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2023,12,22),
                      transaction_type=TransactionType.BUY,
                      amount=373.20,
                      user_id=4,
                      order_id=9,
          ),
          Transaction(transaction_date=date(2023,12,12),
                      transaction_type=TransactionType.BUY,
                      amount=2776.44,
                      user_id=1,
                      order_id=6,
          ),
          Transaction(transaction_date=date(2023,12,6),
                      transaction_type=TransactionType.BUY,
                      amount=468.30,
                      user_id=4,
                      order_id=3,
          ),
          Transaction(transaction_date=date(2023,11,29),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=6073.28,
                      user_id=4,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2023,11,4),
                      transaction_type=TransactionType.BUY,
                      amount=3000.00,
                      user_id=3,
                      order_id=8,
          ),
          Transaction(transaction_date=date(2023,11,2),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=806595.69,
                      user_id=3,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2023,10,26),
                      transaction_type=TransactionType.WITHDRAWAL,
                      amount=2000,
                      user_id=2,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2023,10,18),
                      transaction_type=TransactionType.BUY,
                      amount=241.29,
                      user_id=2,
                      order_id=7,
          ),
          Transaction(transaction_date=date(2023,9,23),
                      transaction_type=TransactionType.BUY,
                      amount=1850.96,
                      user_id=2,
                      order_id=6,
          ),
          Transaction(transaction_date=date(2023,9,19),
                      transaction_type=TransactionType.BUY,
                      amount=2247.84,
                      user_id=1,
                      order_id=3,
          ),
          Transaction(transaction_date=date(2023,8,8),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=270401.42,
                      user_id=2,
                      order_id=None,
          ),
          Transaction(transaction_date=date(2023,7,17),
                      transaction_type=TransactionType.DEPOSIT,
                      amount=4531570.50,
                      user_id=1,
                      order_id=None,
          ),
     ]

     db.session.add_all(transactions)

     watchlists = [
          Watchlist(user_id=4,
                    stock_id=5,
          ),
          Watchlist(user_id=1,
                    stock_id=7,
               ),
          Watchlist(user_id=3,
                    stock_id=6,
               ),
          Watchlist(user_id=5,
                    stock_id=8,
               ),
          Watchlist(user_id=2,
                    stock_id=10,
               ),
          Watchlist(user_id=3,
                    stock_id=4,
               ),
          Watchlist(user_id=2,
                    stock_id=10,
               ),
          Watchlist(user_id=1,
                    stock_id=4,
               ),
     ]

     db.session.add_all(watchlists)

     db.session.commit() # flossing

     print("Tables seeded")
