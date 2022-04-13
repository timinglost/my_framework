from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect
from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import Subject, FileWriter, ConsoleWriter


class News:
    def __init__(self, header, date, text):
        self.header = header
        self.date = date
        self.text = text


class User:
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email


class Admin(User):
    pass


class Buyer(User, DomainObject):
    def __init__(self, login, password, email):
        self.trackings = []
        super().__init__(login, password, email)


class UserFactory:
    types = {
        'buyer': Buyer,
        'admin': Admin
    }

    @classmethod
    def create(cls, type_, login, password, email):
        return cls.types[type_](login, password, email)


class ProductPrototype:
    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype, Subject):

    def __init__(self, name, category, description):
        self.name = name
        self.description = description
        self.category = category
        self.category.products.append(self)
        self.buyers = []
        super().__init__()

    def __getitem__(self, item):
        return self.buyers[item]

    def add_student(self, buyer: Buyer):
        self.buyers.append(buyer)
        buyer.trackings.append(self)
        self.notify()

class PremiumProduct(Product):
    pass


class MiddleProduct(Product):
    pass


class ProductFactory:
    types = {
        'pp': PremiumProduct,
        'mp': MiddleProduct
    }

    @classmethod
    def create(cls, type_, name, category, description):
        return cls.types[type_](name, category, description)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def products_count(self):
        result = len(self.products)
        if self.category:
            result += self.category.products_count()
        return result


class Engine:
    def __init__(self):
        self.admins = []
        self.buyers = []
        self.products = []
        self.categories = []
        self.news = []

    @staticmethod
    def create_user(type_, login, password, email):
        return UserFactory.create(type_, login, password, email)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_product(type_, name, description, category):
        return ProductFactory.create(type_, name, category, description)

    def get_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        return None

    def get_buyer(self, login):
        for item in self.buyers:
            if item.login == login:
                return item

    @staticmethod
    def create_news(header, date, text):
        return News(header, date, text)

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class BuyersMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'buyers'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, login, password, email = item
            buyer = Buyer(login, password, email)
            buyer.id = id
            result.append(buyer)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, login, password, email FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Buyer(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (login, password, email) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.login, obj.password, obj.email,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET login=? WHERE id=?"

        self.cursor.execute(statement, (obj.login, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'buyers': BuyersMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Buyer):

            return BuyersMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


connection = connect('my_db.sqlite')
