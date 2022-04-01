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
    pass
