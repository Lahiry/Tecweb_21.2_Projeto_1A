from utils import load_data, load_template, build_response
from urllib.parse import unquote_plus
from data.database import Database, Note
import json

def index(request):

    database = Database('data/banco')

    response = build_response()

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus

        if corpo.split('=')[0] == 'delete_id':
            note_id = corpo.split('=')[1]
            database.delete(note_id)

        elif corpo.startswith('update'):
            note = Note(id=corpo.split('&')[0].split('=')[1], title=unquote_plus(corpo.split('&')[1].split('=')[1]), content=unquote_plus(corpo.split('&')[2].split('=')[1]))
            database.update(note)

        else:
            chave_valor = corpo.split('&')
            note = Note(title=unquote_plus(chave_valor[0].split('=')[1]), content=unquote_plus(chave_valor[1].split('=')[1]))
            database.add(note)

        response = build_response(code=303, reason='See Other', headers='Location: /')
        
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=dados.id, title=dados.title, details=dados.content)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return response + load_template('index.html').format(notes=notes).encode()