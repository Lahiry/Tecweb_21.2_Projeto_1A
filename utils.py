import os
import json
import codecs
from data.database import Database

def extract_route(request):
    return request.split('\n')[0].split(' ')[1].replace('/', '', 1)

def read_file(path):
    with open(path, 'rb') as file:
        return file.read()

def load_data(database_name='banco'):
    database = Database('data/' + database_name)
    return database.get_all()
    
def load_template(template_file):
    with codecs.open('templates/' + template_file, 'r', 'UTF-8') as file:
        return file.read()

def build_response(body='', code=200, reason='OK', headers=''):
    if headers != '' and body != '':
        response = ('HTTP/1.1 ' + str(code) + ' ' + reason + '\n' + headers + '\n\n' + body).encode()
    elif headers != '':
        response = ('HTTP/1.1 ' + str(code) + ' ' + reason + '\n' + headers + '\n\n').encode()
    elif body != '':
        response = ('HTTP/1.1 ' + str(code) + ' ' + reason + '\n\n' + body).encode()
    else:
        response = ('HTTP/1.1 ' + str(code) + ' ' + reason + '\n\n').encode()
    return response