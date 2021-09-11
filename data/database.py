import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database():

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name + '.db'
        self.conn = sqlite3.connect(self.database_name)
        self.conn.execute('CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)')

    def add(self, note: Note) -> None:
        self.conn.execute(f'INSERT INTO note (title, content) VALUES ("{note.title}", "{note.content}")')
        self.conn.commit()

    def get_all(self) -> Note(list):
        notes = []
        cursor = self.conn.execute('SELECT id, title, content FROM note')
        for linha in cursor:
            notes.append(Note(id=linha[0], title=linha[1], content=linha[2]))
        return notes

    def update(self, entry) -> None:
        self.conn.execute(f'UPDATE note SET title = "{entry.title}", content = "{entry.content}" WHERE id = "{entry.id}"')
        self.conn.commit()

    def delete(self, note_id) -> None:
        self.conn.execute(f'DELETE FROM note WHERE id = "{note_id}"')
        self.conn.commit()
    

