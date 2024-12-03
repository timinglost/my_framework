from copy import deepcopy
from quopri import decodestring


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


class Buyer(User):
    pass


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


class Product(ProductPrototype):

    def __init__(self, name, category, description):
        self.name = name
        self.description = description
        self.category = category
        self.category.products.append(self)


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

    @staticmethod
    def create_news(header, date, text):
        return News(header, date, text)

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')
