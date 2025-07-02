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

## July 2 Notes (Used ChatGPT to summarize)

Today was a big one. I got both the simulation logic and my first bit of cloud integration up and running.

### 🧱 Pygame Sim Update

I started by implementing two key components: the `Car` class and the `Intersection` class.

- The **`Car` class** now has its own position, speed, direction, and ID. Each car knows how to move itself and can draw itself on the screen. Right now, they’re just going straight, but this is enough to visualize traffic on a basic level.
- The **`Intersection` class** is pretty barebones, but it defines a rectangle and can track which cars are inside it. Eventually it’ll help handle rules like who has the right of way or whether a car has to stop.

In the `simulator.py`, I updated the main loop to:
- Maintain a list of `Car` objects
- Move and draw each car every frame
- Remove cars once they move off-screen (using a list comprehension to filter them)
- Add basic printing to debug each car’s current state

This really helped me understand how to structure objects in a game loop and was a clean first step toward more realistic traffic logic.

---

### ☁️ AWS Integration — First Cloud Milestone!

I also created an AWS account and generated a new IAM user specifically for programmatic access to S3. I gave that user `AmazonS3FullAccess`, then used the CLI (`aws configure`) to store my access keys securely.

Once that was done, I wrote a Python script using **Boto3** to upload a file to S3. I tested it with a dummy file, and it worked!

#### What did you learn about S3/Boto3?
It's fairly simple to set up a bucket and upload files! Access management and the entire process is not much different than what I've done before on Azure — once your credentials are in place, `boto3` just works. The CLI configuration makes development smooth, and I didn’t have to hardcode any secrets.

#### What does `upload_file()` abstract away?
Initially, I thought the main benefit was skipping the need to log in or manually upload via the console. That’s true — but it actually does a lot more behind the scenes. `upload_file()` abstracts away several steps I’d otherwise have to implement myself: 

- Opening and reading the file  
- Splitting it into chunks for large files  
- Retrying failed uploads  
- Reconnecting on network hiccups  
- Setting content metadata or permissions  

It lets me focus on integrating the upload into my app’s workflow instead of worrying about all the infrastructure details.

#### How could this be extended for your sim logs?
As the simulation is running, I’ll log car data (positions, timestamps, maybe even intersection congestion) to a local JSON file. After the simulation ends, that file can be uploaded to S3 automatically. Then next time the simulation runs, it can either overwrite the previous file or create a new version with a timestamped filename. This gives me versioned logs for later analysis without storing anything long-term on my local machine. Eventually, I might explore using these uploads as part of a CI/CD pipeline or cloud-based data processing setup.

---

### ✅ Summary of the Day

- [x] Created `Car` and `Intersection` classes  
- [x] Updated Pygame loop to handle multiple cars and filtering  
- [x] Created an AWS IAM user and configured CLI access  
- [x] Successfully uploaded a test file to Amazon S3  
- [x] Reflected on what’s really happening under the hood of `upload_file()`

Tomorrow, I’ll start logging actual simulation data and test uploading that to S3. I’d also like to begin thinking about how to simulate real traffic flow — maybe stoplights, congestion, or prioritizing certain directions at intersections.
