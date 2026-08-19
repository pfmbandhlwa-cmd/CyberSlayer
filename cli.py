import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from src.database.db import get_connection, create_tables

console = Console()


def get_or_create_user(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("CyberSlayer_CLI",))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (username, score) VALUES (?, ?)", ("CyberSlayer_CLI", 0))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE username = ?", ("CyberSlayer_CLI",))
        user = cursor.fetchone()

    return user


def display_header(user):
    title = f"[bold cyan]🗡️  CYBERSLAYER CLI[/bold cyan]  |  User: [bold white]{user['username']}[/bold white]  |  Score: [bold green]{user['score']} PTS[/bold green]"
    console.print(Panel(title, style="bold blue", expand=False))


def list_challenges(conn, user):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges")
    challenges = cursor.fetchall()

    cursor.execute("SELECT challenge_id FROM user_progress WHERE user_id = ?", (user["id"],))
    solved_ids = {row["challenge_id"] for row in cursor.fetchall()}

    table = Table(title="Available Challenges", header_style="bold magenta", border_style="dim white")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Title", style="bold white")
    table.add_column("Category", style="yellow")
    table.add_column("Difficulty", style="blue")
    table.add_column("Status / Points", justify="center")

    for ch in challenges:
        if ch["id"] in solved_ids:
            status = "[bold green]✅ SOLVED[/bold green]"
        else:
            status = f"[bold gold1]🔒 {ch['points']} PTS[/bold gold1]"

        table.add_row(str(ch["id"]), ch["title"], ch["category"], ch["difficulty"], status)

    console.print(table)
    return challenges, solved_ids


def attempt_challenge(conn, user):
    challenges, solved_ids = list_challenges(conn, user)
    try:
        cid = IntPrompt.ask("\n[bold cyan]Select Challenge ID to play[/bold cyan]")
    except Exception:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges WHERE id = ?", (cid,))
    ch = cursor.fetchone()

    if not ch:
        console.print("[bold red]❌ Invalid Challenge ID.[/bold red]")
        return

    if ch["id"] in solved_ids:
        console.print("[bold yellow]⚠️ You already completed this challenge![/bold yellow]")
        return

    question_text = (
        f"[bold white]{ch['question']}[/bold white]\n\n"
        f"[cyan]A)[/cyan] {ch['option_a']}\n"
        f"[cyan]B)[/cyan] {ch['option_b']}\n"
        f"[cyan]C)[/cyan] {ch['option_c']}\n"
        f"[cyan]D)[/cyan] {ch['option_d']}"
    )
    console.print(Panel(question_text, title=f"📋 {ch['title']} ({ch['points']} PTS)", style="cyan"))

    answer = Prompt.ask("Your answer", choices=["A", "B", "C", "D"], case_sensitive=False).upper()

    if answer == ch["correct_answer"]:
        cursor.execute("INSERT INTO user_progress (user_id, challenge_id) VALUES (?, ?)", (user["id"], ch["id"]))
        cursor.execute("UPDATE users SET score = score + ? WHERE id = ?", (ch["points"], user["id"]))
        conn.commit()

        console.print(Panel(f"[bold green]🎉 CORRECT! You earned +{ch['points']} PTS![/bold green]", style="green"))
    else:
        console.print(Panel(f"[bold red]❌ Incorrect. The correct answer was {ch['correct_answer']}.[/bold red]", style="red"))

    # Display explanation regardless of correctness
    if ch["explanation"]:
        console.print(Panel(f"[italic white]{ch['explanation']}[/italic white]", title="💡 Explanation", style="magenta"))


def main():
    create_tables()
    conn = get_connection()
    user = get_or_create_user(conn)

    try:
        while True:
            user = get_or_create_user(conn)
            display_header(user)

            console.print("[1] List Challenges")
            console.print("[2] Answer Challenge")
            console.print("[3] Exit\n")

            choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

            if choice == "1":
                list_challenges(conn, user)
            elif choice == "2":
                attempt_challenge(conn, user)
            elif choice == "3":
                console.print("[bold red]Goodbye, CyberSlayer![/bold red]")
                break
    finally:
        conn.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
