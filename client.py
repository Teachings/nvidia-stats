import time
import requests
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box
from rich.text import Text
from requests.exceptions import RequestException

console = Console()

API_URL = "http://127.0.0.1:8881/system_stats"  # Update if needed
REFRESH_INTERVAL = 0.5  # seconds

# Define GPU-Server mapping
GPU_SERVER_MAP = {
    "GPU": [0, 1, 2, 3]  # Aggregate all GPUs under a single "GPU" row
}

def fetch_stats():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}

def colorize_utilization(value):
    """Apply color based on utilization percentage."""
    if value == " x ":
        return Text(value, style="grey50")
    utilization = int(value)
    if utilization == 0:
        return Text("000", style="grey50")
    elif utilization < 50:
        return Text(value.zfill(3), style="green")
    elif utilization < 80:
        return Text(value.zfill(3), style="yellow3")
    else:
        return Text(value.zfill(3), style="red")

def aggregate_gpu_stats(gpu_stats):
    # Aggregate GPU stats for all GPUs under "GPU"
    server_stats = {
        "GPU": {
            "utilization": [" x "] * len(GPU_SERVER_MAP["GPU"]),
            "memory_used": 0,
            "memory_total": 0
        }
    }

    for gpu_index in GPU_SERVER_MAP["GPU"]:
        gpu = gpu_stats[gpu_index]
        utilization = gpu["utilization"].rstrip('%')  # Keep as plain string for now
        server_stats["GPU"]["utilization"][gpu_index] = utilization
        server_stats["GPU"]["memory_used"] += int(gpu["memory_used"].split()[0])
        server_stats["GPU"]["memory_total"] += int(gpu["memory_total"].split()[0])

    # Format VRAM
    server_stats["GPU"]["memory_used"] = f"{server_stats['GPU']['memory_used']} MiB"
    server_stats["GPU"]["memory_total"] = f"{server_stats['GPU']['memory_total']} MiB"

    return server_stats

def create_table(data):
    # Set up the table with optimized column widths
    table = Table(show_header=True, header_style="bold cyan", box=box.DOUBLE_EDGE)

    # Adjusted column widths
    table.add_column("Category", justify="center", style="bold blue", no_wrap=True)
    table.add_column("Utilization", justify="center", no_wrap=True)
    table.add_column("Used (MiB)", justify="right", style="green", width=12)
    table.add_column("Total (MiB)", justify="right", style="magenta", width=12)

    # Handle errors if API fails
    if "error" in data:
        table.add_row("Error", data["error"], "-", "-")
        return table

    # CPU Stats
    cpu_utilization = data["cpu_stats"]["cpu_utilization"]
    ram_used = data["ram_stats"]["ram_used"]
    ram_total = data["ram_stats"]["ram_total"]
    table.add_row("CPU", cpu_utilization, ram_used, ram_total)

    # GPU Stats
    aggregated_stats = aggregate_gpu_stats(data["gpu_stats"])
    gpu_stats = aggregated_stats["GPU"]
    utilization_cells = [colorize_utilization(val) for val in gpu_stats["utilization"]]
    utilization_text = Text(" | ").join(utilization_cells)  # Join the styled Text objects
    table.add_row(
        "GPU",
        utilization_text,  # Show aligned utilizations with colorized values
        gpu_stats["memory_used"],
        gpu_stats["memory_total"]
    )

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
