import subprocess
import os

configs = [
    "configs/standard.json",
    "configs/low_fps.json"
]

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

for config in configs:
    print(f"\n▶️ Running sim with config: {config}")
    config_name = os.path.splitext(os.path.basename(config))[0]

    result = subprocess.run(
        ["python3", "sim/simulator.py", "--config", config, "--no-gui", "--max-ticks", "1500"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    with open(f"logs/{config_name}_stdout.txt", "w") as f:
        f.write(result.stdout)
    with open(f"logs/{config_name}_stderr.txt", "w") as f:
        f.write(result.stderr)

    print(f"✅ Finished {config}. Output saved to logs/{config_name}_stdout.txt")
