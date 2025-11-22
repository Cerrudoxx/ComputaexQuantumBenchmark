# lib/ui.py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import print as rprint

console = Console()

ASCII_ART = """
  _   _  ____   _____           ____          ____                  _     
 | | | ||  _ \ / ____|         / __ \        |  _ \                | |    
 | |_| || |_) | |       ______| |  | |_   _  | |_) | ___ _ __   ___| |__  
 |  _  ||  __/| |      |______| |  | | | | | |  _ < / _ \ '_ \ / __| '_ \ 
 | | | || |   | |____         | |__| | |_| | | |_) |  __/ | | | (__| | | |
 |_| |_||_|    \_____|         \___\_\\\\__,_| |____/ \___|_| |_|\___|_| |_|
"""


def show_header():
    """Clears screen and shows the logo."""
    console.clear()
    text = Text(ASCII_ART, style="bold cyan")
    panel = Panel(text, subtitle="Centralized Benchmark Suite", border_style="blue")
    console.print(panel)


def show_menu():
    """Displays the main menu and returns the user choice."""
    show_header()
    rprint("[bold yellow]Select an option:[/bold yellow]")
    rprint("1. [green]Run Benchmark (Assisted Mode)[/green]")
    rprint("2. [cyan]Install Conda Environments (Auto)[/cyan]")
    rprint("3. [magenta]Uninstall Conda Environments[/magenta]")
    rprint("4. [blue]List Supported Simulators[/blue]")
    rprint("5. [red]Exit[/red]")

    choice = Prompt.ask("Option", choices=["1", "2", "3", "4", "5"], default="1")
    return choice


def wait_for_user():
    """Pauses execution so the user can read output."""
    console.print()
    console.input("[bold dim]Press Enter to return to the menu...[/bold dim]")


def print_error(msg):
    console.print(f"[bold red]ERROR:[/bold red] {msg}")


def print_info(msg):
    console.print(f"[bold blue]INFO:[/bold blue] {msg}")


def print_success(msg):
    console.print(f"[bold green]SUCCESS:[/bold green] {msg}")


def print_warning(msg):
    console.print(f"[bold yellow]WARNING:[/bold yellow] {msg}")