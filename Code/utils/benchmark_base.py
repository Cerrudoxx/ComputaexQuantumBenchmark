"""
benchmark_base.py — Common benchmark execution logic for HPC-QuBench.

Provides a mixin / helper that any Runner (Grover, QFT, QV) can call to
wrap the actual simulation with Rich live progress, resource monitoring,
context-switch tracking, and advanced metric collection.
"""

import math
import statistics
import time
import psutil
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import box


def run_benchmark(runner, console: Console) -> dict:
    """Execute a benchmark run with full instrumentation.

    *runner* must expose:
      - n                (int)
      - num_iterations   (int)
      - cores            (int)
      - cpu_monitor      (CPUMonitor | None)
      - ram_monitor      (RAMMonitor | None)
      - _run_simulation(num_executions) -> list[float]   (times in ns)

    Returns a rich dict with all metrics.
    """
    process = psutil.Process()
    start_ctx = process.num_ctx_switches()
    wall_start = time.perf_counter()

    # ── start monitors ─────────────────────────────────────────────────────
    if runner.cpu_monitor:
        runner.cpu_monitor.start()
    if runner.ram_monitor:
        runner.ram_monitor.start()

    # ── Phase 1: warm-up / initial sampling ────────────────────────────────
    n_warmup = 10

    with Progress(
        SpinnerColumn("dots", style="bright_cyan"),
        TextColumn("[bold bright_cyan]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="bright_green"),
        TextColumn("[bright_yellow]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Phase 1 — Warm-up sampling", total=n_warmup)
        t_for_loop = []
        for _ in range(n_warmup):
            times = runner._run_simulation(1)
            t_for_loop.extend(times)
            progress.advance(task)

    t_mean = statistics.mean(t_for_loop) / 1e9 if t_for_loop else 0
    t_std = statistics.stdev(t_for_loop) / 1e9 if len(t_for_loop) > 1 else 0

    # ── time limit guard ───────────────────────────────────────────────────
    if t_mean > 8640:
        console.print(
            Panel("[bold red]⚠  Algorithm exceeds 1-day limit. Aborting.[/]",
                  border_style="red", box=box.HEAVY),
        )
        raise SystemExit(0)

    # ── Phase 2: statistically-driven additional iterations ────────────────
    optimal_n = (
        math.ceil((2 * 1.96 * t_std) / (0.05 * t_mean)) ** 2
        if t_mean > 0 else n_warmup
    )
    console.print(
        f"  🔬 Statistically optimal iterations: [bold bright_cyan]{optimal_n}[/]"
    )

    remaining = max(0, optimal_n - n_warmup)
    if remaining > 0:
        with Progress(
            SpinnerColumn("dots", style="bright_magenta"),
            TextColumn("[bold bright_magenta]{task.description}"),
            BarColumn(bar_width=40, style="magenta", complete_style="bright_green"),
            TextColumn("[bright_yellow]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Phase 2 — Main sampling", total=remaining)
            for _ in range(remaining):
                times = runner._run_simulation(1)
                t_for_loop.extend(times)
                progress.advance(task)
    else:
        optimal_n = n_warmup

    # ── stop monitors ──────────────────────────────────────────────────────
    end_ctx = process.num_ctx_switches()
    wall_end = time.perf_counter()

    if runner.cpu_monitor:
        runner.cpu_monitor.stop()
    if runner.ram_monitor:
        runner.ram_monitor.stop()

    # ── compute timing stats ───────────────────────────────────────────────
    t_seconds = [t / 1e9 for t in t_for_loop]
    t_final = statistics.mean(t_seconds) if t_seconds else 0
    std_final = statistics.stdev(t_seconds) if len(t_seconds) > 1 else 0

    # ── assemble result dict ───────────────────────────────────────────────
    ctx_vol = end_ctx.voluntary - start_ctx.voluntary
    ctx_inv = end_ctx.involuntary - start_ctx.involuntary

    result = {
        'n':                  runner.n,
        'iterations_number':  optimal_n,
        't_grover':           t_final,
        'std_grover':         std_final,

        # CPU
        'cpu_avg':            runner.cpu_monitor.average()       if runner.cpu_monitor else 0,
        'cpu_min':            runner.cpu_monitor.min_usage()     if runner.cpu_monitor else 0,
        'cpu_max':            runner.cpu_monitor.max_usage()     if runner.cpu_monitor else 0,
        'cpu_p95':            runner.cpu_monitor.percentile(95)  if runner.cpu_monitor else 0,
        'cpu_median':         runner.cpu_monitor.median()        if runner.cpu_monitor else 0,
        'cpu_stdev':          runner.cpu_monitor.stdev()         if runner.cpu_monitor else 0,
        'cpu_samples':        runner.cpu_monitor.samples_count() if runner.cpu_monitor else 0,

        # RAM
        'ram_avg_pct':        runner.ram_monitor.average()               if runner.ram_monitor else 0,
        'ram_peak_mb':        runner.ram_monitor.max_memory_usage_in_mb() if runner.ram_monitor else 0,
        'ram_avg_mb':         runner.ram_monitor.average_mb()            if runner.ram_monitor else 0,
        'ram_min_mb':         runner.ram_monitor.min_mb()                if runner.ram_monitor else 0,
        'ram_stdev_mb':       runner.ram_monitor.stdev_mb()              if runner.ram_monitor else 0,
        'ram_p95_mb':         runner.ram_monitor.percentile_mb(95)       if runner.ram_monitor else 0,
        'ram_median_mb':      runner.ram_monitor.median_mb()             if runner.ram_monitor else 0,
        'ram_samples':        runner.ram_monitor.samples_count()         if runner.ram_monitor else 0,

        # OS
        'ctx_switches_vol':   ctx_vol,
        'ctx_switches_invol': ctx_inv,
        'ctx_switches_total': ctx_vol + ctx_inv,

        'cores':              runner.cores,
    }
    return result
