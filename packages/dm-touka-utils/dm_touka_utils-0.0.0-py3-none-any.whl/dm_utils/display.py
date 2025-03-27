from rich.console import Console
from rich.panel import Panel

console = Console()


def display_string_by_rich(data: str, title: str, style="dodger_blue1") -> None:
    data_panel = Panel(data, title=title, style=style)
    console.print(data_panel, markup=False)
