from datetime import date
import socket


def date_request(request):
    request['date'] = date.today()


def ip_addr(request):
    request['ip_addr'] = f'{socket.gethostbyname(socket.gethostname())}'


fronts = [date_request, ip_addr]
