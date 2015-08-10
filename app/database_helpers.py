from app import app
from flask import g 
import sqlite3


def init_db():
    with app.app_context():
        db = get_database()
        with app.open_resource(app.config['SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_database().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def db_connect():
	db=sqlite3.connect(app.config['DATABASE'])
	db.row_factory = sqlite3.Row
	return db

def get_database():
	if not hasattr(g,'db'):
		g.db=db_connect()
	return g.db

def insert_db(query, args=(), one=False):
    cur = get_database().execute(query, args)
    get_database().commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv