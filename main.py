import sys
from sqlite3 import Connection, connect
from password_enc import *
from database import *
from rich.console import Console
from generate_password import generate_password
from rich_components import *
from signal import signal, SIGINT


def main():
    CONSOLE = Console()
    DB_CONNECTION = connect("database.db")
    signal(SIGINT, handler)
    while True:
        if is_initial_setup(DB_CONNECTION):
            try:
                master_password = prompt_password(CONSOLE)
            except EOFError:
                sys.exit()

            PWE = PasswordEnc(master_password)

            if PWE.validate_master():
                command_loop(CONSOLE, PWE, DB_CONNECTION)
            else:
                print_invalid_password(CONSOLE)
        else:
            new_master = input("New master password: ")
            PWE = PasswordEnc(new_master)
            PWE.store_master()
            continue


def handler(signal_received, frame):
    """Handles the CTRL-C event."""
    print("")
    print('CTRL-C detected.\nExiting...')
    sys.exit(0)


def command_loop(console: Console, pwe: PasswordEnc, db_connection: Connection):
    """Main command loop"""
    print_welcome(console)
    cmds = ["add", "view", "delete", "search", "exit"]
    while True:
        console.print("")
        prompt = prompt_choice(cmds, "Command")
        if prompt == "exit":
            sys.exit()
        if prompt == "add":
            cmd_add_login(console, pwe, db_connection)
        if prompt == "view":
            cmd_view_logins(console, pwe, db_connection)
        if prompt == "delete":
            cmd_delete_login(console, pwe, db_connection)
        if prompt == "search":
            cmd_search_logins(console, pwe, db_connection)


def cmd_add_login(console: Console, pwe: PasswordEnc, db_connection: Connection):
    """Adds a new login to the database"""
    data = prompt_add_new_login(console, generate_password)

    name = data["name"]
    username = data["username"]
    password = data["password"]

    enc_password = pwe.encrypt(password)

    try:
        create_table(db_connection)
        insert_login(db_connection, [name, username, enc_password])
    except DatabaseError:
        console.print("[prompt.invalid]Error connecting to the database.[/prompt.invalid]")


def cmd_view_logins(console: Console, pwe: PasswordEnc, db_connection: Connection):
    """Fetch logins from the database and prints as a table"""
    try:
        create_table(db_connection)
        data = get_all_logins(db_connection)

        if data:
            logins = []

            for row in data:
                enc_password = row[3]
                if isinstance(enc_password, str):
                    enc_password = bytes(enc_password, encoding="utf-8")

                dec_password = pwe.decrypt(enc_password)
                logins.append((str(row[0]), str(row[1]), str(row[2]), str(dec_password)))

            logins = tuple(logins)
            print_table(console, logins)
        else:
            console.print("[prompt.invalid]No entries.[/prompt.invalid]")
    except DatabaseError:
        console.print("[prompt.invalid]Error connecting to the database.[/prompt.invalid]")


def cmd_delete_login(console: Console, pwe: PasswordEnc, db_connection: Connection):
    """Deletes a login from the database"""
    login_id = prompt_delete_login(console)

    try:
        status = delete_login(db_connection, login_id)
        if status:
            console.print(f"[green]Login with id = {login_id} deleted.[/green]")
        else:
            console.print(f"[red bold]No entry was found for the given id = {login_id}.[/red bold]")
    except DatabaseError:
        console.print("[prompt.invalid]Error connecting to the database.[/prompt.invalid]")


def cmd_search_logins(console: Console, pwe: PasswordEnc, db_connection: Connection):
    """Search for a login and prints a table output"""
    login_name = prompt_search_login(console)
    try:
        data = search_login(db_connection, login_name)

        if data:
            logins = []

            for row in data:
                enc_password = row[3]
                if isinstance(enc_password, str):
                    enc_password = bytes(enc_password, encoding="utf-8")

                dec_password = pwe.decrypt(enc_password)
                logins.append((str(row[0]), str(row[1]), str(row[2]), str(dec_password)))

            logins = tuple(logins)
            print_table_inline(console, logins)
        else:
            console.print("[bold red]No entries.")
    except DatabaseError:
        console.print("[prompt.invalid]Error connecting to the database.[/prompt.invalid]")


def is_initial_setup(db_connection: Connection):
    """Checks if a master password is set"""
    try:
        with open("configs.json") as file:
            json_dict = json.load(file)
            if json_dict["checkPassword"]:
                return True
            else:
                clear_database(db_connection)
                return False
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    main()
