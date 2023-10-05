from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale

db_username = 'postgres'
db_password = ''
db_host = 'localhost:5432'
db_name = 'declarative_base'


engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}")

Session = sessionmaker(bind=engine)
session = Session()


publisher_name = input("Enter the name or identifier of the publisher: ")

publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()

if publisher:
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Stock, Book.id == Stock.id_book).\
        join(Sale, Stock.id == Sale.id_stock).\
        join(Shop, Stock.id_shop == Shop.id).\
        filter(Book.id_publisher == publisher.id)

    for title, shop_name, price, date_sale in query:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")

else:
    print("Publisher not found.")

session.close()