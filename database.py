import sqlite3
from sqlite3 import Connection


class DatabaseError(Exception):
    """Custom exception for every database error with error message"""

    def __init__(self, error) -> None:
        error = f"Error: {error}"
        super().__init__(error)


def main():
    con = sqlite3.connect("database.db")
    results = get_all_logins(con)

    if results:
        for row in results:
            print(row)
    else:
        print("no data")


def create_table(connection: Connection):
    """Creates the default password table for the given connection"""
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, username TEXT, password TEXT)"
            )
        except sqlite3.Error as err:
            raise DatabaseError(err)


def insert_login(connection: Connection, data: list):
    """Insert the given list of data to the table `passwords`"""
    with connection:
        cursor = connection.cursor()
        data[0] = data[0].lower()
        try:
            cursor.execute(
                "INSERT INTO passwords(name,username,password) VALUES(?,?,?)",
                tuple(data),
            )
        except sqlite3.Error as err:
            raise DatabaseError(err)


def delete_login(connection: Connection, login_id: int | str):
    """Checks if `login_id` exists in password table. If it exists, deletes the row and returns `True` otherwise `False`"""
    if isinstance(login_id, int):
        login_id = str(login_id)

    with connection:
        cursor = connection.cursor()
        try:
            all_login_ids = [str(row[0]) for row in get_all_logins(connection)]

            if login_id in all_login_ids:
                cursor.execute(f"DELETE FROM passwords WHERE id={login_id}")
                return True

            return False
        except sqlite3.Error as err:
            raise DatabaseError(err)


def search_login(connection: Connection, search_key: str):
    """Return a list of all rows where `name` LIKE `search_key`, otherwise returns `False`"""
    with connection:
        cursor = connection.cursor()
        try:
            search_key = f"{search_key}%"
            cursor.execute("SELECT * FROM passwords WHERE name LIKE ?", (search_key,))
            results = cursor.fetchall()

            return results if results else False
        except sqlite3.Error as err:
            raise DatabaseError(err)


def get_all_logins(connection: Connection):
    """Return a list containing all rows"""
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM passwords")
            results = cursor.fetchall()
            return results if results else False
        except sqlite3.Error as err:
            raise DatabaseError(err)


def clear_database(connection: Connection):
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS passwords")
        except sqlite3.Error as err:
            raise DatabaseError(err)


if __name__ == "__main__":
    main()
