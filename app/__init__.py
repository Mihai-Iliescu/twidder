import os
import sqlite3

from flask import Flask, g

app=Flask(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'database/database.db'),
	SCHEMA=os.path.join(app.root_path, 'database/database.schema')
	))

from app import server
from app import database_helpers

@app.teardown_appcontext
def close_database_connection(error):
	if hasattr(g,'db'):
		g.db.close()