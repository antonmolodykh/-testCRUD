import sqlite3


class TableProvider(object):
    def __init__(self):

        # Для простоты используется база данных в памяти
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = dict_factory
        c = self.conn.cursor()

        c.execute("create table client (id integer primary key, name varchar, phone varchar, timezone varchar)")
        self.conn.commit()

    def create(self, name, phone, timezone):
        c = self.conn.cursor()
        c.execute("INSERT INTO client(name, phone, timezone) VALUES (?,?,?)", (name, phone, timezone))

    def read(self, id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM client WHERE id = (?)", (id,))
        return c.fetchone()

    def update(self, id, points):
        c = self.conn.cursor()

        keys = points.keys()
        values = list(points.values()) + [id]

        quest = lambda q: '=?,'.join(q) + '=?'
        update = 'UPDATE client SET ' + quest(keys) + ' WHERE id=?'
        c.execute(update, values)

    def delete(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM client WHERE id = ?', (id,))

    def search(self, query):
        c = self.conn.cursor()

        c.execute('SELECT * FROM client WHERE name LIKE ? OR phone LIKE ? OR timezone LIKE ?', (query, query, query))
        return c.fetchall()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d