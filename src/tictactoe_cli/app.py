"""Application entry point."""

from rich.console import Console


def main() -> None:
    """Run the TicTacToe CLI game."""
    console = Console()
    console.print("[bold cyan]TicTacToe CLI[/bold cyan] v0.1.0")
    console.print("[dim]Game coming soon...[/dim]")
