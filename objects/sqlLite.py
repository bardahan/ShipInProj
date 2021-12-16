import sqlite3
from flask import g

from db.db import DB


class SqlLite(DB):

    def __init__(self, db_name: str = "example.sqlite3"):
        self.db_name = db_name
        self.db = self.get_db()

    def setup_db(self):
        # this sets up the database (creates if necessary) in the file DATABASE_FILE.
        # data is saved to the file between runs
        db = sqlite3.connect(self.db_name)
        db.execute('PRAGMA foreign_keys = ON;')
        db.execute('CREATE TABLE IF NOT EXISTS ship(id integer primary key autoincrement, name text, type text)')
        db.execute('CREATE TABLE IF NOT EXISTS locations(id integer primary key autoincrement, shipid int NOT NULL, '
                   'latitude REAL, longitude REAL, date_created default current_timestamp, '
                   'FOREIGN KEY(shipid) REFERENCES ship(id))')
        return db

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.setup_db()
        return db

    def select(self, query, params=()):
        res = self.db.execute(query, params)
        return {'rows': res.fetchall()}

    def insert(self, query, params):
        self.db.execute(query, params)
        self.db.commit()
