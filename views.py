from my_framework.templator import render
from patterns.сreational_patterns import Engine

site = Engine()


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None), news_list=site.news)


class About:
    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None), news_list=site.news)


class Shop:
    def __call__(self, request):
        return '200 OK', render('examples.html', date=request.get('date', None),
                                categories_list=site.categories,
                                product_list=site.products,
                                news_list=site.news)


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contact.html',
                                date=request.get('date', None),
                                news_list=site.news)


class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('examples.html',
                                    categories_list=site.categories,
                                    product_list=site.products,
                                    date=request.get('date', None),
                                    news_list=site.news)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=site.categories,
                                    date=request.get('date', None),
                                    news_list=site.news)


class CreateNews:
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            header = data['header']
            date = data['date']
            text = data['text']
            header = site.decode_value(header)
            date = site.decode_value(date)
            text = site.decode_value(text)
            if len(header) > 0 and len(date) > 0 and len(text) > 0:
                new_news = site.create_news(header, date, text)

                site.news.append(new_news)

            return '200 OK', render('create_news.html', date=request.get('date', None), news_list=site.news)
        else:
            return '200 OK', render('create_news.html', date=request.get('date', None), news_list=site.news)


class CreateProduct:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            description = data['description']
            type_ = data['type_']
            try:
                category_id = data['category']
            except KeyError:
                return '200 OK', render('create_category.html',
                                    categories=site.categories,
                                    date=request.get('date', None),
                                    news_list=site.news)
            name = site.decode_value(name)
            description = site.decode_value(description)
            type_ = site.decode_value(type_)
            category_id = site.decode_value(category_id)
            category = site.find_category_by_id(int(category_id))
            new_product = site.create_product(type_, name, description, category)
            site.products.append(new_product)
            return '200 OK', render('examples.html',
                                    categories_list=site.categories,
                                    product_list=site.products,
                                    date=request.get('date', None),
                                    news_list=site.news)
        else:
            return '200 OK', render('create_product.html',
                                    categories_list=site.categories,
                                    date=request.get('date', None),
                                    news_list=site.news)


class CreateUser:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            login = data['login']
            password = data['password']
            email = data['email']
            type_ = data['type_']
            login = site.decode_value(login)
            password = site.decode_value(password)
            email = site.decode_value(email)
            type_ = site.decode_value(type_)
            new_user = site.create_user(type_, login, password, email)
            if type_ == 'buyer':
                site.buyers.append(new_user)
            else:
                site.admins.append(new_user)
            return '200 OK', render('index.html',
                                    buyers_list=site.buyers,
                                    admins_list=site.admins,
                                    date=request.get('date', None),
                                    news_list=site.news)
        else:
            return '200 OK', render('create_users.html',
                                    categories_list=site.categories,
                                    date=request.get('date', None),
                                    news_list=site.news)


class CopyProduct:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_product(name)
            if old_course:
                new_name = f'copy_{name}'
                new_product = old_course.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render('examples.html',
                                    categories_list=site.categories,
                                    product_list=site.products,
                                    date=request.get('date', None),
                                    news_list=site.news,
                                    name=new_product.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
