import json

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, tick, car_states):
        self.logs.append({
            "tick": tick,
            "cars": car_states
        })

    def write_to_file(self, path="data/sim_log.json"):
        with open(path, "w") as f:
            json.dump(self.logs, f, indent=2)
