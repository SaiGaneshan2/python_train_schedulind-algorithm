import heapq
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

def time_to_minutes(time_str):
    """Convert HH:MM format to total minutes."""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

def minutes_to_time(minutes):
    """Convert total minutes back to HH:MM format."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"

def min_platforms_greedy(arrivals, departures, verbose=True):
    """
    Greedy approach to find the minimum number of platforms needed.
    Uses a min-heap to track ongoing train departures.
    """
    events = sorted([(t, 'a') for t in arrivals] + [(t, 'd') for t in departures])
    max_platforms = 0
    current_platforms = 0

    if verbose:
        console.print("\n[bold cyan]Processing Events (Sorted by Time):[/bold cyan]")
        for time, event in events:
            console.print(f" • {minutes_to_time(time)} - {'Arrival' if event == 'a' else 'Departure'}")

    for time, event in events:
        if event == 'a':
            current_platforms += 1  # New train arrives
        else:
            current_platforms -= 1  # A train departs
        max_platforms = max(max_platforms, current_platforms)

    return max_platforms


def min_platforms_divide_conquer(arrivals, departures, verbose=True):
    """
    Divide and conquer approach to find the minimum number of platforms needed.
    Recursively divides train schedules into halves and merges results.
    """
    def merge_and_count(arr1, dep1, arr2, dep2):
        merged_arrivals = sorted(arr1 + arr2)
        merged_departures = sorted(dep1 + dep2)

        platform_needed, max_platforms = 0, 0
        i, j = 0, 0
        while i < len(merged_arrivals) and j < len(merged_departures):
            if merged_arrivals[i] < merged_departures[j]:
                platform_needed += 1
                max_platforms = max(max_platforms, platform_needed)
                i += 1
            else:
                platform_needed -= 1
                j += 1
        
        return max_platforms, merged_arrivals, merged_departures

    def divide_and_conquer(arrivals, departures):
        if len(arrivals) == 1:
            return 1, arrivals, departures
        
        mid = len(arrivals) // 2
        left_count, left_arr, left_dep = divide_and_conquer(arrivals[:mid], departures[:mid])
        right_count, right_arr, right_dep = divide_and_conquer(arrivals[mid:], departures[mid:])
        
        return merge_and_count(left_arr, left_dep, right_arr, right_dep)

    result, _, _ = divide_and_conquer(arrivals, departures)
    return result


def display_comparison_table(greedy_result, dc_result):
    """
    Displays a rich table comparing Greedy and Divide & Conquer approaches.
    """
    table = Table(title="🔍 Algorithm Comparison", show_lines=True)
    
    table.add_column("Factor", style="bold magenta")
    table.add_column("Greedy Approach", style="bold cyan")
    table.add_column("Divide & Conquer", style="bold yellow")

    table.add_row("Time Complexity", "O(N log N)", "O(N log N)")
    table.add_row("Space Complexity", "O(1)", "O(N) (Recursion)")
    table.add_row("Ease of Implementation", "✅ Simple & Intuitive", "⚠ More Complex")
    table.add_row("Performance", f"🏆 {greedy_result} Platforms", f"🏆 {dc_result} Platforms")
    
    console.print("\n")
    console.print(table)


def main():
    console.print("[bold green]🚄 Welcome to the Train Platform Calculator! 🚄[/bold green]\n")

    arrivals = input("Enter arrival times (space-separated, HH:MM format): ").split()
    departures = input("Enter departure times (space-separated, HH:MM format): ").split()

    if len(arrivals) != len(departures):
        console.print("[bold red]❌ Error: Arrival and departure lists must have the same length![/bold red]")
        return

    arrivals = [time_to_minutes(t) for t in arrivals]
    departures = [time_to_minutes(t) for t in departures]

    console.print("\n[bold blue]🔍 Running Greedy Approach...[/bold blue]")
    greedy_result = min_platforms_greedy(arrivals, departures)

    console.print("\n[bold yellow]🔍 Running Divide & Conquer Approach...[/bold yellow]")
    dc_result = min_platforms_divide_conquer(arrivals, departures)

    display_comparison_table(greedy_result, dc_result)


if __name__ == "__main__":
    main()
