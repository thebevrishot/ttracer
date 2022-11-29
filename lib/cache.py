from .client import CLIENT
from rethinkdb import RethinkDB

R = RethinkDB()

R.connect( "localhost", 28015 ).repl()

DB = R.db("torn")