# Traffic Simulation — Cloud Deployable

A Pygame-based traffic simulator for modeling cars, intersections, and traffic behavior, with cloud integration for data logging. Created as a hands-on interview prep project for the Simulation Services team at Torc Robotics.

---

## 🔧 Tech Stack

- **Python 3**
- **Pygame** for simulation and rendering
- **JSON** for state logging
- **AWS S3** for cloud-based log storage

---

## 📁 Folder Structure

- `sim/` — Simulation files
- `models/` — Core simulation classes (`Car`, `Intersection`)
- `cloud/` — AWS S3 upload logic
- `data/` — Locally stored JSON logs
- `configs/` — Parameterized config files for different run modes

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the simulation

```bash
python simulator.py --config configs/standard.json
```

Or try a different configuration:

```bash
python simulator.py --config configs/low_fps.json
```

---

## 🎯 Project Goals

- [x] Visualize traffic behavior in a 2D simulation
- [x] Implement intersections with rule-based control
- [x] Create cloud integration for log uploads
- [ ] Introduce more realistic traffic rules (e.g., stop signs, traffic prioritization)
- [ ] Automate cloud runs with parameterized traffic scenarios

---

## 🗓 Dev Log

### July 1 — Laying the Groundwork

I started by watching a few videos on cloud computing and AWS. I’ve used Azure before, but this gave me a solid refresher and helped me frame how I want to use cloud tools in this project. The most useful resource was this [KodeKloud AWS intro](https://www.youtube.com/watch?v=EgAoarq_aic), which clarified how S3 works and what Boto3 abstracts away.

This gave me the idea to have the simulation run locally, generate structured logs, and upload those logs to an S3 bucket at the end of each run — a clean cloud-ready workflow that mimics real simulation tooling.

---

### July 2 — First Cloud Upload & Core Simulation

Big day. I implemented two foundational systems: the `Car` and `Intersection` classes.

- The `Car` class handles position, direction, speed, and ID. It knows how to move and draw itself, and logs its current state.
- The `Intersection` class tracks whether a car is inside the intersection and manages light state.

I also:
- Created an AWS IAM user for S3 access and configured the CLI locally
- Wrote a Boto3 script that successfully uploaded a test file to my bucket
- Reflected on what `upload_file()` abstracts — chunking, retries, metadata, etc.
- Designed the logging workflow I’d like to evolve into a pipeline

---

### July 3 — Logging + First Rules of the Road

I added dynamic car spawning using a tick counter and randomized spawn delays. This made the sim more interesting and gave me an easy entry point for modeling traffic flow.

The `Logger` class now records every car’s state at each tick. At the end of a run, this is saved as a JSON file and uploaded to S3 automatically.

I also gave intersections actual behavior by implementing stoplight logic:
- The `Intersection` class cycles between red and green on a timer
- Cars check the light state before entering the box
- If the light is red and they’re touching the intersection, they stop and increment a `wait_time`
- `should_stop()` encapsulates this logic in the car itself

This was a big moment because it added decision-making into the simulation — cars now respond to their environment. The sim went from being a visualizer to a rule-based system.

---

### July 3 (continued) — Full Turning Logic

This was the most complex implementation so far — and the most rewarding. I extended the simulation to support **both left and right turns** for cars coming from **any direction**.

Each car spawns with a `turn_direction` (`"left"`, `"right"`, or `None`), and turn logic is handled in the `Car` class based on:
- The car’s current `direction`
- A fixed zone near the intersection where a turn can be triggered
- Manual shape adjustments post-turn (to account for rotated dimensions)

Key improvements:
- All turn scenarios (8 total) are now handled
- Cars adjust their rectangle shape and bumper logic mid-turn
- Collision detection still works as expected after turning
- Cars are color-coded by spawn direction for easy visual tracking

While the turns are currently snap-based (no curves or interpolation), they demonstrate the kind of mid-simulation decision-making I’d want in a scalable system.

---

## ✅ Summary of What’s Working

- Real-time traffic simulation with dynamic cars
- Intersection control via timed lights
- Cars that obey stoplights, collide realistically, and wait appropriately
- Turn logic that covers every possible entry/exit configuration
- Logging that captures state each tick and uploads to S3 for later analysis

---

## 🧭 Next Steps

- Fix edge cases where cars stall mid-turn or get stuck at the intersection
- Refactor turn logic into a cleaner, direction-agnostic handler
- Explore smooth turn behavior (e.g., interpolation or angle-based motion)
- Use logs to generate performance metrics (e.g., average wait time, congestion mapping)
- Design pipeline or trigger system to automate multiple runs with varying inputs

---

## 📦 Final Thoughts

This project has been incredibly valuable for deepening my understanding of cloud-integrated simulations. Every feature added so far ties directly back to core principles in simulation services: visual accuracy, decision modeling, state logging, and scalable infrastructure. It’s helped me build not just technical familiarity, but a stronger instinct for designing reactive, testable systems.
