# client.py
import time
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box
from requests.exceptions import RequestException

console = Console()

API_URL = "http://127.0.0.1:8881/system_stats"  # Update if needed
REFRESH_INTERVAL = 0.5  # seconds

def fetch_stats():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}

def create_table(data):
    table = Table(show_header=True, header_style="bold cyan", box=box.MINIMAL_DOUBLE_HEAD)

    table.add_column("CPU/GPU", justify="center")
    table.add_column("Utilization", justify="center")
    table.add_column("Used (MiB)", justify="center")
    table.add_column("Total (MiB)", justify="center")

    # Handle errors if API fails
    if "error" in data:
        table.add_row("Error", data["error"])
        return table

    # CPU Stats
    cpu_utilization = data["cpu_stats"]["cpu_utilization"]
    ram_used = data["ram_stats"]["ram_used"]
    ram_total = data["ram_stats"]["ram_total"]
    table.add_row("CPU", cpu_utilization, ram_used, ram_total)
    table.add_row("─" * 13, "─" * 13, "─" * 13, "─" * 13)  # Separator line after CPU

    # GPU Stats
    for i, gpu in enumerate(data["gpu_stats"]):
        gpu_name = gpu["name"].split()[-1]  # Only show model, e.g., "3090"
        table.add_row(
            f"GPU {i+1} - {gpu_name}",
            gpu["utilization"],
            gpu["memory_used"],
            gpu["memory_total"]
        )

    # Bottom border under last GPU entry
    table.add_row("─" * 13, "─" * 13, "─" * 13, "─" * 13)

    return table

def main():
    try:
        with Live(auto_refresh=True, refresh_per_second=0.5) as live:
            while True:
                data = fetch_stats()
                table = create_table(data)
                live.update(table)
                time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        console.print("\nExiting gracefully. Goodbye!")

if __name__ == "__main__":
    main()
