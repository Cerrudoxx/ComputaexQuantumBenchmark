"""
results_handler.py — Rich, animated console output for HPC-QuBench results.

Displays timing, resource-usage, and OS-level metrics using Rich tables,
panels, progress bars, and live displays. Also persists data to CSV.
"""

import os
import csv
import platform
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from datetime import datetime


class ResultsHandler:
    """Handles the display and persistence of benchmark results.

    Uses Rich panels and tables for a visually striking terminal output,
    and writes results to CSV for later analysis.
    """

    CSV_HEADERS = [
        'n', 'iterations_number', 't_grover', 'std_grover',
        'cpu_avg', 'cpu_min', 'cpu_max', 'cpu_p95', 'cpu_median', 'cpu_stdev',
        'ram_avg_pct', 'ram_peak_mb', 'ram_avg_mb', 'ram_min_mb', 'ram_stdev_mb', 'ram_p95_mb', 'ram_median_mb',
        'ctx_switches_vol', 'ctx_switches_invol', 'ctx_switches_total',
        'cores', 'cpu_samples', 'ram_samples',
    ]

    def __init__(self, file_name: str, results_dir: str, console: Console):
        self.file_name = os.path.join(results_dir, file_name + '.csv')
        self.results_dir = results_dir
        self.console = console
        self._ensure_csv_headers()

    # ── CSV ─────────────────────────────────────────────────────────────────

    def _ensure_csv_headers(self) -> None:
        if not os.path.isfile(self.file_name):
            with open(self.file_name, mode='w', newline='') as f:
                csv.writer(f).writerow(self.CSV_HEADERS)

    def save_to_csv(self, d: dict) -> None:
        """Append one row of results to the CSV file."""
        with open(self.file_name, mode='a', newline='') as f:
            csv.writer(f).writerow([d.get(h, 0) for h in self.CSV_HEADERS])
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console.print(f"  💾 Data saved → [bold]{self.file_name}[/bold]  ({ts})", style="dim")

    # ── Rich display ────────────────────────────────────────────────────────

    def display_header(self, algorithm: str, simulator: str, n: int,
                       iterations: int, cores: int) -> None:
        """Print a large header panel at the start of a benchmark run."""
        header = Text()
        header.append("⚛  HPC-QuBench", style="bold bright_cyan")
        header.append("  │  ", style="dim")
        header.append(f"{algorithm}", style="bold bright_magenta")
        header.append("  │  ", style="dim")
        header.append(f"{simulator}", style="bold bright_yellow")

        info_items = [
            f"[bold cyan]Qubits:[/] {n}",
            f"[bold cyan]Iterations:[/] {iterations:,}",
            f"[bold cyan]Cores:[/] {cores}",
            f"[bold cyan]Host:[/] {platform.node()}",
            f"[bold cyan]Total RAM:[/] {psutil.virtual_memory().total / (1024**3):.1f} GB",
            f"[bold cyan]CPU:[/] {psutil.cpu_count(logical=True)} logical cores",
        ]

        panel = Panel(
            Columns(info_items, equal=True, expand=True),
            title=header,
            border_style="bright_blue",
            box=box.DOUBLE_EDGE,
            padding=(1, 2),
        )
        self.console.print()
        self.console.print(panel)

    def display_timing_table(self, data: dict) -> None:
        """Display a detailed timing results table."""
        table = Table(
            title="⏱  Timing Results",
            box=box.ROUNDED,
            title_style="bold bright_cyan",
            border_style="cyan",
            header_style="bold bright_white on dark_blue",
            row_styles=["", "dim"],
            padding=(0, 1),
            show_lines=True,
        )
        table.add_column("Metric", style="bold bright_white", min_width=28)
        table.add_column("Value", justify="right", style="bright_green", min_width=20)

        t = data.get('t_grover', 0)
        std = data.get('std_grover', 0)
        iters = data.get('iterations_number', 0)
        ci_95 = 1.96 * std / (iters ** 0.5) if iters > 0 else 0
        cv = (std / t * 100) if t > 0 else 0

        table.add_row("Mean Execution Time", f"{t:.6f} s")
        table.add_row("Standard Deviation", f"{std:.6f} s")
        table.add_row("Coeff. of Variation (CV)", f"{cv:.2f} %")
        table.add_row("95% Confidence Interval", f"± {ci_95:.6f} s")
        table.add_row("Number of Iterations", f"{iters:,}")

        self.console.print()
        self.console.print(table)

    def display_usage_table(self, data: dict) -> None:
        """Display a detailed CPU / RAM / OS usage table."""

        # ── CPU sub-table ──────────────────────────────────────────────────
        cpu_table = Table(
            title="🖥  CPU Usage",
            box=box.ROUNDED,
            title_style="bold bright_yellow",
            border_style="yellow",
            header_style="bold bright_white on dark_green",
            show_lines=True,
            padding=(0, 1),
        )
        cpu_table.add_column("Metric", style="bold", min_width=22)
        cpu_table.add_column("Value", justify="right", style="bright_green", min_width=16)

        cpu_table.add_row("Average",       f"{data.get('cpu_avg', 0):.2f} %")
        cpu_table.add_row("Median",        f"{data.get('cpu_median', 0):.2f} %")
        cpu_table.add_row("Min",           f"{data.get('cpu_min', 0):.2f} %")
        cpu_table.add_row("Max",           f"{data.get('cpu_max', 0):.2f} %")
        cpu_table.add_row("Std. Deviation",f"{data.get('cpu_stdev', 0):.2f} %")
        cpu_table.add_row("P95",           f"{data.get('cpu_p95', 0):.2f} %")
        cpu_table.add_row("Samples",       f"{data.get('cpu_samples', 0):,}")

        # ── RAM sub-table ──────────────────────────────────────────────────
        ram_table = Table(
            title="🧠 RAM Usage",
            box=box.ROUNDED,
            title_style="bold bright_green",
            border_style="green",
            header_style="bold bright_white on dark_red",
            show_lines=True,
            padding=(0, 1),
        )
        ram_table.add_column("Metric", style="bold", min_width=22)
        ram_table.add_column("Value", justify="right", style="bright_cyan", min_width=16)

        ram_table.add_row("Avg (%)",        f"{data.get('ram_avg_pct', 0):.2f} %")
        ram_table.add_row("Peak",           f"{data.get('ram_peak_mb', 0):.2f} MB")
        ram_table.add_row("Average",        f"{data.get('ram_avg_mb', 0):.2f} MB")
        ram_table.add_row("Median",         f"{data.get('ram_median_mb', 0):.2f} MB")
        ram_table.add_row("Min",            f"{data.get('ram_min_mb', 0):.2f} MB")
        ram_table.add_row("Std. Deviation", f"{data.get('ram_stdev_mb', 0):.2f} MB")
        ram_table.add_row("P95",            f"{data.get('ram_p95_mb', 0):.2f} MB")
        ram_table.add_row("Samples",        f"{data.get('ram_samples', 0):,}")

        # ── OS sub-table ───────────────────────────────────────────────────
        os_table = Table(
            title="⚙  OS Metrics",
            box=box.ROUNDED,
            title_style="bold bright_magenta",
            border_style="magenta",
            header_style="bold bright_white on purple4",
            show_lines=True,
            padding=(0, 1),
        )
        os_table.add_column("Metric", style="bold", min_width=22)
        os_table.add_column("Value", justify="right", style="bright_yellow", min_width=16)

        os_table.add_row("Vol. Ctx Switches",   f"{data.get('ctx_switches_vol', 0):,}")
        os_table.add_row("Invol. Ctx Switches",  f"{data.get('ctx_switches_invol', 0):,}")
        os_table.add_row("Total Ctx Switches",   f"{data.get('ctx_switches_total', 0):,}")
        os_table.add_row("Cores Used",           f"{data.get('cores', 0)}")

        self.console.print()
        self.console.print(Columns([cpu_table, ram_table, os_table], equal=True, expand=True))

    def display_run_summary(self, data: dict) -> None:
        """Display a compact summary panel after a single run."""
        t = data.get('t_grover', 0)
        peak_ram = data.get('ram_peak_mb', 0)
        cpu = data.get('cpu_avg', 0)
        ctx = data.get('ctx_switches_total', 0)

        items = [
            f"[bold green]✓[/] Time: [bold]{t:.4f}s[/]",
            f"[bold green]✓[/] Peak RAM: [bold]{peak_ram:.1f} MB[/]",
            f"[bold green]✓[/] CPU Avg: [bold]{cpu:.1f}%[/]",
            f"[bold green]✓[/] Ctx Switches: [bold]{ctx:,}[/]",
        ]
        summary = Panel(
            Columns(items, equal=True, expand=True),
            title="[bold bright_cyan]Run Summary[/]",
            border_style="bright_green",
            box=box.ROUNDED,
            padding=(0, 1),
        )
        self.console.print()
        self.console.print(summary)

    # ── Console output file ─────────────────────────────────────────────────

    def save_console_output(self) -> None:
        with open(os.path.join(self.results_dir, "out.txt"), "w") as f:
            f.write(self.console.export_text())
