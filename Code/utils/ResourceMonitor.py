"""
ResourceMonitor.py — Advanced resource monitoring for HPC-QuBench.

Provides CPU and RAM monitoring threads with rich, time-series data collection,
statistical analysis, and publication-quality plotting.
"""

import threading
import time
import psutil
import csv
import os
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from rich.console import Console

console = Console()


# ─── CPU Monitor ──────────────────────────────────────────────────────────────

class CPUMonitor:
    """Monitors per-process and system-wide CPU usage in a background thread.

    Collects time-stamped readings of both system-wide CPU percentage and
    per-core utilisation so that downstream analysis can report min/max/p95
    alongside the mean.
    """

    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.readings: list[float] = []
        self.per_core_readings: list[list[float]] = []
        self.timestamps: list[float] = []
        self._monitoring = False
        self._start_time: float = 0.0

    # ── lifecycle ──────────────────────────────────────────────────────────

    def start(self):
        """Start sampling in a daemon thread."""
        psutil.cpu_percent(interval=None)          # prime the first call
        psutil.cpu_percent(interval=None, percpu=True)
        self._monitoring = True
        self._start_time = time.perf_counter()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    def stop(self):
        """Signal the thread to stop and wait for it."""
        self._monitoring = False
        self._thread.join()

    # ── internals ──────────────────────────────────────────────────────────

    def _monitor(self):
        while self._monitoring:
            self.readings.append(psutil.cpu_percent(interval=None))
            self.per_core_readings.append(psutil.cpu_percent(interval=None, percpu=True))
            self.timestamps.append(time.perf_counter() - self._start_time)
            time.sleep(self.interval)

    # ── statistics ─────────────────────────────────────────────────────────

    def average(self) -> float:
        return statistics.mean(self.readings) if self.readings else 0.0

    def min_usage(self) -> float:
        return min(self.readings) if self.readings else 0.0

    def max_usage(self) -> float:
        return max(self.readings) if self.readings else 0.0

    def stdev(self) -> float:
        return statistics.stdev(self.readings) if len(self.readings) > 1 else 0.0

    def percentile(self, p: float) -> float:
        """Return the *p*-th percentile (0–100) of the readings."""
        if not self.readings:
            return 0.0
        s = sorted(self.readings)
        k = (len(s) - 1) * (p / 100.0)
        f = int(k)
        c = f + 1
        if c >= len(s):
            return s[f]
        return s[f] + (k - f) * (s[c] - s[f])

    def median(self) -> float:
        return statistics.median(self.readings) if self.readings else 0.0

    def samples_count(self) -> int:
        return len(self.readings)


# ─── RAM Monitor ──────────────────────────────────────────────────────────────

class RAMMonitor:
    """Monitors process-level RAM usage in a background thread.

    Stores both percentage *and* absolute MB readings so that all derived
    metrics (peak, average, stdev, percentiles) are immediately available
    without post-hoc conversion.
    """

    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.readings_pct: list[float] = []
        self.readings_mb: list[float] = []
        self.timestamps: list[float] = []
        self._monitoring = False
        self._start_time: float = 0.0

    # ── lifecycle ──────────────────────────────────────────────────────────

    def start(self):
        self._monitoring = True
        self._start_time = time.perf_counter()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    def stop(self):
        self._monitoring = False
        self._thread.join()

    # ── internals ──────────────────────────────────────────────────────────

    def _monitor(self):
        process = psutil.Process()
        while self._monitoring:
            mem_info = process.memory_info()
            self.readings_pct.append(process.memory_percent())
            self.readings_mb.append(mem_info.rss / (1024 * 1024))
            self.timestamps.append(time.perf_counter() - self._start_time)
            time.sleep(self.interval)

    # ── percentage helpers (legacy compat) ─────────────────────────────────

    def average(self) -> float:
        return statistics.mean(self.readings_pct) if self.readings_pct else 0.0

    def max_memory_usage(self) -> float:
        return max(self.readings_pct) if self.readings_pct else 0.0

    def max_memory_usage_in_mb(self) -> float:
        return max(self.readings_mb) if self.readings_mb else 0.0

    # ── advanced MB statistics ─────────────────────────────────────────────

    def average_mb(self) -> float:
        return statistics.mean(self.readings_mb) if self.readings_mb else 0.0

    def min_mb(self) -> float:
        return min(self.readings_mb) if self.readings_mb else 0.0

    def stdev_mb(self) -> float:
        return statistics.stdev(self.readings_mb) if len(self.readings_mb) > 1 else 0.0

    def percentile_mb(self, p: float) -> float:
        if not self.readings_mb:
            return 0.0
        s = sorted(self.readings_mb)
        k = (len(s) - 1) * (p / 100.0)
        f = int(k)
        c = f + 1
        if c >= len(s):
            return s[f]
        return s[f] + (k - f) * (s[c] - s[f])

    def median_mb(self) -> float:
        return statistics.median(self.readings_mb) if self.readings_mb else 0.0

    def samples_count(self) -> int:
        return len(self.readings_mb)

    # ── real-time CSV writer (keeps backward compat) ───────────────────────

    def real_time_memory_usage(self, file_name: str):
        process = psutil.Process()
        if not os.path.isfile(file_name):
            with open(file_name, mode='w', newline='') as csv_file:
                csv.writer(csv_file).writerow(['Time', 'RAM Usage (MB)'])

        with open(file_name, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            start = time.perf_counter()
            while self._monitoring:
                elapsed = time.perf_counter() - start
                mem = process.memory_info().rss / (1024 * 1024)
                writer.writerow([f"{elapsed:.3f}", mem])
                csv_file.flush()
                time.sleep(max(0, (elapsed + self.interval) - (time.perf_counter() - start)))


# ═══════════════════════════════════════════════════════════════════════════════
# Plotting helpers
# ═══════════════════════════════════════════════════════════════════════════════

_STYLE = {
    'figure.facecolor': '#1e1e2e',
    'axes.facecolor':   '#1e1e2e',
    'axes.edgecolor':   '#cdd6f4',
    'axes.labelcolor':  '#cdd6f4',
    'text.color':       '#cdd6f4',
    'xtick.color':      '#cdd6f4',
    'ytick.color':      '#cdd6f4',
    'grid.color':       '#45475a',
    'grid.alpha':       0.5,
}

def _apply_style():
    matplotlib.rcParams.update(_STYLE)


def plot_ram_avg_from_results(file_name: str):
    """RAM Average (MB) vs Qubits — dark-themed, publication-quality."""
    _apply_style()
    try:
        qubits, ram_mb = [], []
        with open(file_name) as f:
            reader = csv.reader(f)
            hdr = next(reader)
            n_i = hdr.index('n') if 'n' in hdr else 0
            r_i = hdr.index('ram_mb') if 'ram_mb' in hdr else 6
            for row in reader:
                qubits.append(int(row[n_i]))
                ram_mb.append(float(row[r_i]))

        if not qubits:
            return
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.fill_between(qubits, ram_mb, alpha=0.25, color='#a6e3a1')
        ax.plot(qubits, ram_mb, '-o', color='#a6e3a1', linewidth=2, markersize=6)
        ax.set_xlabel('Number of Qubits', fontsize=12)
        ax.set_ylabel('Peak RAM Usage (MB)', fontsize=12)
        ax.set_title('Peak RAM Usage vs Number of Qubits', fontsize=14, fontweight='bold')
        ax.grid(True)
        fig.tight_layout()
        out = file_name.replace('.csv', '_ram_avg_qubits.png')
        fig.savefig(out, dpi=150)
        plt.close(fig)
        console.print(f"  📊 RAM plot saved → {out}", style="green")
    except Exception as e:
        console.print(f"  ⚠ RAM plot error: {e}", style="bold red")


def plot_cpu_avg_from_results(file_name: str):
    """CPU Average (%) vs Qubits — dark-themed."""
    _apply_style()
    try:
        qubits, cpu_avg = [], []
        with open(file_name) as f:
            reader = csv.reader(f)
            hdr = next(reader)
            n_i = hdr.index('n') if 'n' in hdr else 0
            c_i = hdr.index('cpu_avg') if 'cpu_avg' in hdr else 4
            for row in reader:
                qubits.append(int(row[n_i]))
                cpu_avg.append(float(row[c_i]))

        if not qubits:
            return
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.fill_between(qubits, cpu_avg, alpha=0.25, color='#fab387')
        ax.plot(qubits, cpu_avg, '-o', color='#fab387', linewidth=2, markersize=6)
        ax.set_xlabel('Number of Qubits', fontsize=12)
        ax.set_ylabel('CPU Average Usage (%)', fontsize=12)
        ax.set_title('CPU Average Usage vs Number of Qubits', fontsize=14, fontweight='bold')
        ax.grid(True)
        fig.tight_layout()
        out = file_name.replace('.csv', '_cpu_avg_qubits.png')
        fig.savefig(out, dpi=150)
        plt.close(fig)
        console.print(f"  📊 CPU plot saved → {out}", style="green")
    except Exception as e:
        console.print(f"  ⚠ CPU plot error: {e}", style="bold red")


def plot_time_from_csv(file_name: str):
    """Execution Time (s) vs Qubits — dark-themed with error bars when std is available."""
    _apply_style()
    try:
        ns, times, stds = [], [], []
        with open(file_name) as f:
            reader = csv.reader(f)
            hdr = next(reader)
            n_i = hdr.index('n') if 'n' in hdr else 0
            t_i = hdr.index('t_grover') if 't_grover' in hdr else 2
            s_i = hdr.index('std_grover') if 'std_grover' in hdr else 3
            for row in reader:
                ns.append(int(row[n_i]))
                times.append(float(row[t_i]))
                stds.append(float(row[s_i]))

        if not ns:
            return
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.errorbar(ns, times, yerr=stds, fmt='-o', color='#f38ba8',
                     ecolor='#f5c2e7', elinewidth=1.5, capsize=4,
                     linewidth=2, markersize=6, label='Mean ± Std')
        ax.fill_between(ns,
                         [t - s for t, s in zip(times, stds)],
                         [t + s for t, s in zip(times, stds)],
                         alpha=0.15, color='#f38ba8')
        ax.set_xlabel('Number of Qubits', fontsize=12)
        ax.set_ylabel('Execution Time (s)', fontsize=12)
        ax.set_title('Execution Time vs Number of Qubits', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True)
        fig.tight_layout()
        out = file_name.replace('.csv', '_time_qubits.png')
        fig.savefig(out, dpi=150)
        plt.close(fig)
        console.print(f"  📊 Time plot saved → {out}", style="green")
    except Exception as e:
        console.print(f"  ⚠ Time plot error: {e}", style="bold red")


def plot_combined_dashboard(file_name: str):
    """Generate a 2×2 dashboard plot combining Time, RAM, CPU and Context Switches."""
    _apply_style()
    try:
        data: dict[str, list] = {'n': [], 't_grover': [], 'std_grover': [],
                                  'cpu_avg': [], 'ram_peak_mb': [], 'ctx_switches_total': []}
        with open(file_name) as f:
            reader = csv.reader(f)
            hdr = next(reader)
            idx = {col: hdr.index(col) for col in data if col in hdr}
            for row in reader:
                for col, i in idx.items():
                    val = float(row[i]) if col != 'n' else int(row[i])
                    data[col].append(val)

        if not data['n']:
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        ns = data['n']

        # Time
        ax = axes[0][0]
        ax.errorbar(ns, data['t_grover'], yerr=data['std_grover'], fmt='-o',
                     color='#f38ba8', ecolor='#f5c2e7', capsize=4, linewidth=2, markersize=5)
        ax.set_ylabel('Exec Time (s)')
        ax.set_title('Execution Time', fontweight='bold')
        ax.grid(True)

        # RAM
        ax = axes[0][1]
        ax.fill_between(ns, data['ram_peak_mb'], alpha=0.25, color='#a6e3a1')
        ax.plot(ns, data['ram_peak_mb'], '-o', color='#a6e3a1', linewidth=2, markersize=5)
        ax.set_ylabel('Peak RAM (MB)')
        ax.set_title('Peak RAM Usage', fontweight='bold')
        ax.grid(True)

        # CPU
        ax = axes[1][0]
        ax.fill_between(ns, data['cpu_avg'], alpha=0.25, color='#fab387')
        ax.plot(ns, data['cpu_avg'], '-o', color='#fab387', linewidth=2, markersize=5)
        ax.set_xlabel('Number of Qubits')
        ax.set_ylabel('CPU Avg (%)')
        ax.set_title('CPU Average Usage', fontweight='bold')
        ax.grid(True)

        # Context Switches
        ax = axes[1][1]
        ax.bar(ns, data['ctx_switches_total'], color='#89b4fa', alpha=0.8, width=0.6)
        ax.set_xlabel('Number of Qubits')
        ax.set_ylabel('Context Switches')
        ax.set_title('OS Context Switches', fontweight='bold')
        ax.grid(True, axis='y')

        fig.suptitle('HPC-QuBench Performance Dashboard', fontsize=16, fontweight='bold', y=0.98)
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        out = file_name.replace('.csv', '_dashboard.png')
        fig.savefig(out, dpi=150)
        plt.close(fig)
        console.print(f"  📊 Dashboard saved → {out}", style="bold green")
    except Exception as e:
        console.print(f"  ⚠ Dashboard error: {e}", style="bold red")
