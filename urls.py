from datetime import date
import socket
from views import Index, About, Shop, Contacts


def date_request(request):
    request['date'] = date.today()


def ip_addr(request):
    request['ip_addr'] = f'{socket.gethostbyname(socket.gethostname())}'


fronts = [date_request, ip_addr]

routes = {
    '/': Index(),
    '/about/': About(),
    '/shop/': Shop(),
    '/contacts/': Contacts()
}
