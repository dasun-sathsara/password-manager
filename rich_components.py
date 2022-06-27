from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.markdown import Markdown
from rich.table import Table
from rich.padding import Padding
from generate_password import InvalidLength


def main():
    CONSOLE = Console()
    # a = prompt_choice(["hello", "hi", "bye"], "Choose: ")
    # b = prompt_password(CONSOLE)
    # c = prompt_add_new_login(CONSOLE)
    # d = prompt_delete_login(CONSOLE)
    # e = prompt_search_login(CONSOLE)

    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)

    print_table_inline(CONSOLE, (("facebook", "user@example.com", "pdh4%DJH4"),
                       ("youtube", "user@example.com", "sdgdsDJH4"), ("facebook", "user@example.com", "pdh4%DJH4"), ("youtube", "user@example.com", "sdgdsDJH4")))


def print_welcome(console: Console) -> None:
    """Prints the welcome text"""
    MARKDOWN = (
        "Following list shows all the commands to interact with the password manager: \n"
        "* add -> Add a new login\n* view -> Show all stored logins\n* search -> Search for logins\n* delete -> Delete the selected login\n"
        "* quit -> Exit out of the program"
    )

    markdown_text = Markdown(MARKDOWN, style="json.key")
    panel = Panel(
        Padding(markdown_text, 1), title="Password Manager V1", style="bold magenta"
    )
    console.print(Padding(panel, 1))


def print_invalid_password(console: Console) -> None:
    """Prints that the master password is invalid"""
    console.print("[italic red]Invalid master password\n[/italic red]")


def prompt_choice(choices: list, prompt: str) -> str:
    """A Prompt for getting a choice fromo the given `choices` list`"""
    choice = Prompt.ask(f"[white]{prompt}: [/white]", choices=choices)
    return choice


def prompt_password(console: Console) -> str:
    """A Prompt for getting the master password."""
    while True:
        password = Prompt.ask(prompt="[white]Master password:[/white] ", password=True)
        if len(password) != 0:
            return password
        console.print("[prompt.invalid]Password can't be empty.[/prompt.invalid]")


def prompt_add_new_login(console: Console, generate_password) -> dict:
    """A prompt to get `name`, `username` and `passsowrd`"""
    while True:
        name = Prompt.ask("Name: ")
        if len(name) == 0:
            console.print("[prompt.invalid]Name is required.[/prompt.invalid]")
            continue
        break
    while True:
        username = Prompt.ask("Username: ")
        if len(username) == 0:
            console.print("[prompt.invalid]Username is required.[/prompt.invalid]")
            continue
        break

    if Confirm.ask("Do you want to generate a new password? ", default=True):
        while True:
            length = IntPrompt.ask("Length: ", default=10, show_default=True)
            no_chars = IntPrompt.ask("No. of letter: ", default=5, show_default=True)
            no_digits = IntPrompt.ask("No. of digits: ", default=3, show_default=True)
            no_special_characters = IntPrompt.ask("No. of special characters: ", default=2, show_default=True)

            try:
                password = generate_password(length, no_chars, no_digits, no_special_characters)
                break
            except InvalidLength:
                console.print(
                    "[prompt.invalid]Sum of characters, digits and special characters should not exceed the length of the password")
                continue
    else:
        while True:
            password = Prompt.ask("Enter your password: ")
            if len(password) == 0:
                console.print(
                    "[prompt.invalid]Password can't be empty.[/prompt.invalid]"
                )
                continue
            break

    return {"name": name, "username": username, "password": password}


def prompt_delete_login(console: Console) -> int:
    """A prompt to get the ID of a login"""
    while True:
        login_id = IntPrompt.ask("ID of the login: ")
        if login_id:
            return login_id

        console.print("[prompt.invalid]ID can't be empty.[/prompt.invalid]")


def prompt_search_login(console: Console) -> str:
    """A prompt to get the name of a login to serach for."""
    while True:
        name = Prompt.ask("Name: ")
        if len(name) > 0 and name.isalpha():
            name = name.lower()
            return name

        console.print("[prompt.invalid]Invalid value.[/prompt.invalid]")


def print_table(console: Console, data: tuple[str]) -> None:
    """Prints the password table in a alternate screen."""
    text = Text("Logins", style="bold magenta")
    table = Table(title=text, expand=True, show_lines=True, padding=(
        0, 2, 0, 2), row_styles=["white", "yellow"])
    table.add_column(Text('ID', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Name', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Username', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Password', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)

    for t in data:
        table.add_row(t[0], t[1], t[2], t[3])

    with console.screen() as screen:
        panels = Group(Padding(table, 1), Padding(Text("press any key to continue...", style="blink"), 1))
        screen.update(panels)

        input()


def print_table_inline(console: Console, data: tuple[str]) -> None:
    """Prints the password table in the current terminal screen."""

    text = Text("Logins", style="bold magenta")
    table = Table(title=text, expand=True, show_lines=True, padding=(
        0, 1, 0, 1), row_styles=["white", "yellow"])
    table.add_column(Text('ID', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Name', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Username', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)
    table.add_column(Text('Password', justify="center"), justify="left", header_style="bar.pulse", no_wrap=True)

    for t in data:
        table.add_row(t[0], t[1], t[2], t[3])

    console.print(Padding(table, 1))


if __name__ == "__main__":
    main()
