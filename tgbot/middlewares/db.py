from sqlalchemy import create_engine, Column, String, INTEGER, Date
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///tgbot/models/data_base.db?check_same_thread=False', echo=True)

Base = declarative_base()


class MainCoursesBase(Base):
    __tablename__ = "Main_courses"

    id = Column("ID", INTEGER, primary_key=True)
    dish_name = Column("Dish_name", String, nullable=False, unique=True)
    price = Column("Price", INTEGER, nullable=False)

    # контсруктор класса (перегрузка создания экземпляра)
    def __init__(self, dish_name, price):

        self.dish_name = dish_name
        self.price = price

    # метод для отображения информации об объекте класса в режиме отладки
    def __repr__(self):
        return f"{self.__class__}: {self.dish_name}, {self.price}"


class BakeryBase(Base):
    __tablename__ = "Bakery_courses"

    id = Column("ID", INTEGER, primary_key=True)
    dish_name = Column("Dish_name", String, nullable=False, unique=True)
    price = Column("Price", INTEGER, nullable=False)

    def __init__(self, dish_name, price):

        self.dish_name = dish_name
        self.price = price

    def __repr__(self):
        return f"{self.__class__}: {self.dish_name}, {self.price}"


class OrdersBase(Base):
    __tablename__ = "Orders_courses"

    id = Column("id", INTEGER, primary_key=True)
    full_name = Column("Full_name", String, nullable=False)
    order = Column("Order", String, nullable=False)
    total_price = Column("Total_price", INTEGER, nullable=False)

    def __init__(self,  full_name, order, total_price):

        self.full_name = full_name
        self.order = order
        self.total_price = total_price

    def __repr__(self):
        return f"{self.__class__}: {self.full_name}, {self.order}, {self.total_price}"


Base.metadata.create_all(bind=engine)


# соединение сессии базы данных
Session = sessionmaker(bind=engine)