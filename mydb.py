import sqlite3
from contextlib import contextmanager
import datetime

from my_foos import Entry


@contextmanager
def db_open(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()


def add_to_db(entry: Entry) -> None:
	sqlite_create_table_query = """
		CREATE TABLE IF NOT EXISTS outcoming (
			id INTEGER PRIMARY KEY,
			value INTEGER NOT NULL,
			category TEXT NOT NULL,
			addingDate timestamp);
	"""

	sqlite_insert_query = """
		INSERT INTO outcoming(value, category, addingDate)
		VALUES(?, ?, ?)
	"""
	with db_open("test.db") as cur:
		cur.execute(sqlite_create_table_query)

	with db_open("test.db") as cur:
		cur.execute(
			sqlite_insert_query,
			(entry.value, entry.category, datetime.datetime.now())
		)


def view_last_10_entry() -> list[Entry]:
	sql_is_table_exist_query = """
		SELECT name
		FROM sqlite_master
		WHERE type='table' AND name='outcoming';
	"""

	sql_select_query = """
		SELECT value, category
		FROM outcoming
		ORDER BY id DESC
		LIMIT 10;
	"""

	with db_open("test.db") as cur:
		cur.execute(sql_is_table_exist_query)
		isTableExist = cur.fetchall()

	if isTableExist:
		with db_open("test.db") as cur:
			res = [Entry(e[0], e[1]) for e in cur.execute(sql_select_query).fetchall()]
		return res

	else:
		return []