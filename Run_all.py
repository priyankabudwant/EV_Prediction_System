import os
import signal
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def make_env(extra=None):
    env = os.environ.copy()
    if extra:
        env.update(extra)
    return env


SERVICES = [
    {
        "name": "failure-backend",
        "cmd": [sys.executable, "-m", "uvicorn", "ev_failure.app:app", "--port", "8003", "--reload"],
        "cwd": ROOT,
    },
    {
        "name": "main-backend",
        "cmd": [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000", "--reload"],
        "cwd": ROOT / "EV-Charging-Demand-System" / "backend",
    },
    {
        "name": "cost-carbon-backend",
        "cmd": [sys.executable, "-m", "uvicorn", "ev_cost_carbon.main:app", "--port", "8002", "--reload"],
        "cwd": ROOT,
    },
    {
        "name": "adoption-backend",
        "cmd": [sys.executable, "app.py"],
        "cwd": ROOT / "ev-adoption-growth",
    },
    {
        "name": "main-dashboard-frontend",
        "cmd": ["cmd", "/c", "npm", "start"],
        "cwd": ROOT / "ev-dashboard",
        "env": {"PORT": "3000", "BROWSER": "none"},
    },
    {
        "name": "failure-dashboard-frontend",
        "cmd": ["cmd", "/c", "npm", "start"],
        "cwd": ROOT / "ev_failure" / "ev-dashboard",
        "env": {"PORT": "3001", "BROWSER": "none"},
    },
    {
        "name": "failure-dashboard-frontend",
        "cmd": ["cmd", "/c", "npm", "start"],
        "cwd": ROOT / "EV-Charging-Demand-System" / "frontend",
        "env": {"PORT": "3003", "BROWSER": "none"},
    },
    {
        "name": "adoption-frontend",
        "cmd": ["cmd", "/c", "npm", "start"],
        "cwd": ROOT / "ev-adoption-growth" / "frontend",
        "env": {"PORT": "3002", "BROWSER": "none"},
    },

    {
        "name": "cost-carbon-frontend",
        "cmd": ["cmd", "/c", "npm", "start"],
        "cwd": ROOT / "ev_cost_carbon" / "frontend",
        "env": {"PORT": "3004", "BROWSER": "none"},
    },
]


def start_service(service):
    cwd = Path(service["cwd"])
    if not cwd.exists():
        raise FileNotFoundError(f"Missing service folder: {cwd}")

    env = make_env(service.get("env"))
    process = subprocess.Popen(
        service["cmd"],
        cwd=str(cwd),
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    print(f"Started {service['name']} (PID {process.pid})")
    return process


def stop_process(process):
    if process.poll() is not None:
        return

    try:
        process.send_signal(signal.CTRL_BREAK_EVENT)
        process.wait(timeout=10)
        return
    except Exception:
        pass

    try:
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        process.wait(timeout=10)
        return
    except Exception:
        pass

    try:
        process.terminate()
        process.wait(timeout=5)
    except Exception:
        try:
            process.kill()
        except Exception:
            pass


def main():
    processes = []

    try:
        for service in SERVICES:
            processes.append((service["name"], start_service(service)))

        for name, process in processes:
            exit_code = process.wait()
            if exit_code != 0:
                print(f"{name} exited with code {exit_code}")
                break
    except KeyboardInterrupt:
        print("\nStopping all services...")
    finally:
        for _, process in reversed(processes):
            stop_process(process)


if __name__ == "__main__":
    main()
