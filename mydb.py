import sqlite3
from contextlib import contextmanager
import datetime

from my_foos import Entry, parse_text_from_input

sqlite_create_categorys_table_query = """
	CREATE TABLE IF NOT EXISTS categorys (
		id INTEGER PRIMARY KEY,
		description TEXT NOT NULL,
		category TEXT NOT NULL
	);
"""

sqlite_create_outcoming_table_query = """
	CREATE TABLE IF NOT EXISTS outcoming (
		id INTEGER PRIMARY KEY,
		value INTEGER NOT NULL,
		description TEXT NOT NULL,
		addingDate DATE);
"""


@contextmanager
def db_open(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()


def create_table(query: str) -> None:
	with db_open("/usr/src/app/db/test.db") as cur:
		cur.execute(query)


def add_description_to_db(description: str, category: str):
	sqlite_insert_query = """
		INSERT INTO categorys(description, category)
		VALUES(?, ?)
	"""
	with db_open("/usr/src/app/db/test.db") as cur:
		cur.execute(sqlite_insert_query)


def is_description_in_db(description: str):
	sql_select_query = f"""
		SELECT id
		FROM categorys
		WHERE description='{description}'
	"""
	with db_open("/usr/src/app/db/test.db") as cur:
		res = cur.execute(sql_select_query)
		answer = res.fetchone()

	return not (answer is None)

def add_entry_to_db(entry: Entry) -> None:
	sqlite_insert_query = """
		INSERT INTO outcoming(value, description, addingDate)
		VALUES(?, ?, ?)
	"""
	with db_open("/usr/src/app/db/test.db") as cur:
		cur.execute(
			sqlite_insert_query,
			(entry.value, entry.description, entry.date)
		)


def view_last_10_entry() -> list[Entry]:
	sql_select_query = """
		SELECT value, description, addingDate
		FROM outcoming
		ORDER BY id DESC
		LIMIT 10;
	"""

	with db_open("/usr/src/app/db/test.db") as cur:
		res = [Entry(e[0], e[1], e[2]) for e in cur.execute(sql_select_query).fetchall()]

	return res


def delete_entry_from_db(entry: Entry) -> None:
	find_id_query = f"""SELECT id
		FROM outcoming
		WHERE value={entry.value}
		AND description='{entry.description}'
		AND addingDate='{entry.date}';"""
	delete_by_id_querry = f"DELETE FROM outcoming WHERE id=?"
	with db_open("/usr/src/app/db/test.db") as cur:
		res = cur.execute(find_id_query).fetchall()
		cur.execute(delete_by_id_querry, res[0])


def edit_entry_in_db(entry: Entry, new_values: str):
	new_entrys_values = parse_text_from_input(new_values)

	find_id_query = f"""SELECT id
		FROM outcoming
		WHERE value={entry.value}
		AND description='{entry.description}'
		AND addingDate='{entry.date}';"""

	update_by_id_querry = f"""UPDATE outcoming
		SET value= ?,
		description= ?
		WHERE id= ?;"""

	with db_open("/usr/src/app/db/test.db") as cur:
		res = cur.execute(find_id_query).fetchall()
		cur.execute(update_by_id_querry, (new_entrys_values.value,
					new_entrys_values.description, res[0][0]))

