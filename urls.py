from datetime import date
import socket
from views import Index, About, Shop, Contacts, CreateNews, \
    CreateUser, CreateCategory, CreateProduct, CopyProduct


def date_request(request):
    request['date'] = date.today()


def ip_addr(request):
    request['ip_addr'] = f'{socket.gethostbyname(socket.gethostname())}'


fronts = [date_request, ip_addr]

routes = {
    '/': Index(),
    '/about/': About(),
    '/shop/': Shop(),
    '/contacts/': Contacts(),
    '/create_news/': CreateNews(),
    '/create_category/': CreateCategory(),
    '/create_product/': CreateProduct(),
    '/create_users/': CreateUser(),
    '/copy_product/': CopyProduct()
}
