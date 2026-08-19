import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from src.services.ai_service import ai_service

console = Console()

user_profile = {"username": "CyberSlayer", "score": 0, "solved": set()}

CHALLENGES = {
    1: {
        "title": "SQLi Auth Bypass",
        "category": "sqli",
        "points": 100,
        "flag": "cyber{sqli_bypass}",
        "desc": "Bypass login via vulnerable SQL input.",
        "attempts": 0
    },
    2: {
        "title": "Reflected XSS Portal",
        "category": "xss",
        "points": 250,
        "flag": "cyber{xss_reflected}",
        "desc": "Inject executable script in query param.",
        "attempts": 0
    },
    3: {
        "title": "Base64 Header Secret",
        "category": "crypto",
        "points": 100,
        "flag": "cyber{b64_secret}",
        "desc": "Extract and decode server header token.",
        "attempts": 0
    }
}

def display_header():
    title = f"[bold cyan]🗡️  CYBERSLAYER CLI[/bold cyan]  |  Score: [bold green]{user_profile['score']} PTS[/bold green]"
    console.print(Panel(title, style="bold blue", expand=False))

def list_challenges():
    table = Table(title="Available Challenges", header_style="bold magenta", border_style="dim white")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold white")
    table.add_column("Category", style="yellow")
    table.add_column("Status / Points", justify="center")
    table.add_column("Description", style="dim white")

    for cid, ch in CHALLENGES.items():
        if cid in user_profile["solved"]:
            status = "[bold green]✅ SOLVED[/bold green]"
        else:
            status = f"[bold gold1]🔒 {ch['points']} PTS[/bold gold1]"
        
        table.add_row(str(cid), ch["title"], ch["category"].upper(), status, ch["desc"])

    console.print(table)

def submit_flag():
    list_challenges()
    try:
        cid = IntPrompt.ask("\n[bold cyan]Enter Challenge ID to submit flag[/bold cyan]")
    except Exception:
        return

    if cid not in CHALLENGES:
        console.print("[bold red]❌ Invalid Challenge ID.[/bold red]")
        return

    if cid in user_profile["solved"]:
        console.print("[bold yellow]⚠️ You already solved this challenge![/bold yellow]")
        return

    ch = CHALLENGES[cid]
    flag_input = Prompt.ask(f"[bold white]Enter flag for '[cyan]{ch['title']}[/cyan]'[/bold white]").strip()

    if flag_input == ch["flag"]:
        user_profile["score"] += ch["points"]
        user_profile["solved"].add(cid)
        console.print(Panel(f"[bold green]🎉 CORRECT! You earned +{ch['points']} PTS![/bold green]", style="green", title="Success"))
    else:
        ch["attempts"] += 1
        console.print("[bold red]❌ Incorrect flag.[/bold red]")
        feedback = ai_service.analyze_attempt(ch["title"], flag_input, ch["category"])
        console.print(Panel(f"[italic white]{feedback['feedback']}[/italic white]", title="💡 AI Mentor Feedback", style="magenta"))

def request_hint():
    list_challenges()
    try:
        cid = IntPrompt.ask("\n[bold cyan]Enter Challenge ID for a hint[/bold cyan]")
    except Exception:
        return

    if cid not in CHALLENGES:
        console.print("[bold red]❌ Invalid Challenge ID.[/bold red]")
        return

    ch = CHALLENGES[cid]
    ch["attempts"] += 1
    hint_data = ai_service.generate_hint(
        challenge_title=ch["title"],
        category=ch["category"],
        attempt_count=ch["attempts"]
    )
    console.print(Panel(f"[italic yellow]{hint_data['hint']}[/italic yellow]", title="💡 AI Hint", style="yellow"))

def view_profile():
    rank = "Novice" if user_profile["score"] < 200 else "Cyber Slayer"
    profile_text = (
        f"[bold]Username:[/bold]     {user_profile['username']}\n"
        f"[bold]Total Score:[/bold]  [bold green]{user_profile['score']} PTS[/bold green]\n"
        f"[bold]Solved Count:[/bold] {len(user_profile['solved'])} / {len(CHALLENGES)}\n"
        f"[bold]Current Rank:[/bold] [bold cyan]{rank}[/bold cyan]"
    )
    console.print(Panel(profile_text, title="👤 User Profile", style="cyan", expand=False))

def main():
    while True:
        display_header()
        console.print("[1] View Active Challenges")
        console.print("[2] Submit Challenge Flag")
        console.print("[3] Ask AI Mentor for Hint")
        console.print("[4] View Profile & Stats")
        console.print("[5] Exit\n")
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            list_challenges()
        elif choice == "2":
            submit_flag()
        elif choice == "3":
            request_hint()
        elif choice == "4":
            view_profile()
        elif choice == "5":
            console.print("[bold red]Goodbye, CyberSlayer![/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
