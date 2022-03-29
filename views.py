from my_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None))


class Shop:
    def __call__(self, request):
        return '200 OK', render('examples.html', date=request.get('date', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))
