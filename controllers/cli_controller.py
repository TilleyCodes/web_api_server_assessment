from flask import Blueprint
from init import db
from datetime import date
from models import User 


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
             account_open_date=date(2020, 3, 14),
             account_balance=4521546.22
             ),
        User(f_name="Mama",
             l_name="Ti",
             email="mamati@email.com",
             account_open_date=date(2021, 11, 8),
             account_balance=256349.12
             ),
        User(f_name="Yogi",
             l_name="Bear",
             email="yogibear@email.com",
             account_open_date=date(2022, 8, 27),
             account_balance=803241.69
             ),
        User(f_name="Pepe",
             l_name="Poo",
             email="pepepoo@email.com",
             account_open_date=date(2022, 11, 17),
             account_balance=4521546.22
             ),
        User(f_name="Bandit",
             l_name="Boy",
             email="banditboy@email.com",
             account_open_date=date(2024, 5, 8),
             account_balance=4512.58
             )
    ]

    db.session.add_all(users)

    db.session.commit()
    
    print("Tables seeded")
