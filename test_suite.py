import subprocess
import os
import sys
import shutil

SIMULATORS = ['qiskit', 'cirq', 'pennylane', 'qibo', 'qsimov', 'qulacs']
ALGORITHMS = ['grover', 'qft', 'quantumvolume']

def find_conda():
    """Find the conda executable, checking PATH and common locations."""
    conda = shutil.which("conda")
    if conda:
        return conda
    home = os.path.expanduser("~")
    for candidate in [
        os.path.join(home, "anaconda3", "condabin", "conda"),
        os.path.join(home, "miniconda3", "condabin", "conda"),
        os.path.join(home, "anaconda3", "bin", "conda"),
        os.path.join(home, "miniconda3", "bin", "conda"),
    ]:
        if os.path.isfile(candidate):
            return candidate
    print("🔥 FATAL: Could not find conda executable.")
    sys.exit(1)

CONDA = find_conda()

def check_and_install_envs():
    print("=== Checking Conda Environments ===")
    for sim in SIMULATORS:
        try:
            subprocess.run([CONDA, "run", "-n", sim, "echo", "ok"],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"  ✅ Environment '{sim}' is ready.")
        except subprocess.CalledProcessError:
            print(f"  ❌ Environment '{sim}' not found. Installing...")
            try:
                subprocess.run(["python3", "qbench.py", "env", "install", sim], check=True)
                print(f"  ✅ Successfully installed '{sim}'.")
            except subprocess.CalledProcessError:
                print(f"  🔥 FATAL: Failed to install environment '{sim}'.")
                sys.exit(1)

def run_smoke_tests():
    print("\n=== Running Smoke Test Matrix (qubits=3, iterations=1) ===\n")
    success = 0
    total = 0
    failed_runs = []

    for algo in ALGORITHMS:
        print(f"--- Algorithm: {algo} ---")
        for sim in SIMULATORS:
            total += 1
            label = f"{algo:15s} on {sim:10s}"
            sys.stdout.write(f"  ⏳ {label} ... ")
            sys.stdout.flush()

            cmd = ["python3", "qbench.py", "run", algo, sim, "--qubits", "3", "--iterations", "1"]
            try:
                res = subprocess.run(
                    cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                print("✅ PASSED")
                success += 1
            except subprocess.CalledProcessError as e:
                print("❌ FAILED")
                error_detail = (e.stderr or "") + (e.stdout or "")
                failed_runs.append((algo, sim, error_detail))
        print()

    print("=" * 60)
    print(f"Smoke Test Results: {success}/{total} passed")
    print("=" * 60)

    if failed_runs:
        print(f"\n🔴 {len(failed_runs)} failure(s):\n")
        for algo, sim, err in failed_runs:
            print(f"  [{algo} - {sim}]")
            err_lines = err.strip().split('\n')
            for line in err_lines[-30:]:
                print(f"    {line}")
            print()
        sys.exit(1)
    else:
        print("\n🎉 All smoke tests passed successfully!")

if __name__ == "__main__":
    check_and_install_envs()
    run_smoke_tests()
