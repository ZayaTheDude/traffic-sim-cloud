# Traffic Simulation — Cloud Deployable

A Pygame-based traffic simulator for modeling cars and intersections with cloud integration. Created as an interview prep project for Torc Robotics.

## 🔧 Stack
- Python 3
- Pygame for sim visuals
- JSON for logging state
- Cloud deployment via AWS (WIP)

## 🎯 Goals
- [x] Visual traffic with Pygame
- [x] Intersections
- [ ] Traffic rules (lights, stop signs)
- [ ] Cloud deployment
- [ ] Upload sim logs to cloud

## 📂 Folder Structure
- `sim/`: Main simulation code
- `data/`: Log output
- `cloud/`: Upload scripts




## July 1 Notes
I am going to watch these two videos right now to get some exposure to cloud computing and AWS

Video 1 Cloud 101: Basics for Understanding Cloud Computing
https://www.youtube.com/watch?v=cTRALS3vHsY&ab_channel=NewYorkStateBoardofElections

This one was just a nice little general refresher on what cloud computing actually is. No new info.

Video 2 Cloud Deep Dive
https://www.youtube.com/watch?v=kYn_5QD4Ltw&ab_channel=NewYorkStateBoardofElections

Ok I am halfway through this and I do feel like I am not the target audience. I have spend some time in the past week watching videos like these and feel I already have this base level knowledge so I am going to move along.

What is Amazon Web Services (AWS)?
https://www.youtube.com/watch?v=EgAoarq_aic&ab_channel=KodeKloud

This should be better for me. I have used Azure but never AWS so this will be fun to learn.

Good analogy of cloud computing being like going to a pizza shop for pizza and traditional IT being like making the pizza yourself with all of the individual componants.

I also really liked the way he was very honest about how no one really knows EVERYTHING there is to know here.

So when I'm thinking about what would be a good way to use the cloud in my project I think if we could get logs to store in a database and if we could get pipelines setup to run throughout the day with different situations in our simulation that would be good.