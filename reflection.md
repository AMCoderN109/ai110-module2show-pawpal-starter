# PawPal+ Project Reflection

## 1. System Design

Core Actions:
- Register a pet
- Schedule tasks about the pet
- Sort the schedule and making it viewable.

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design is simply connecting objects to organize pet care: an owner has pets, pets have tasks, and schedule manager organizes all the information.

- What classes did you include, and what responsibilities did you assign to each?

Class: Owner, Pet, Tasks, and Schedule.
Owner class: Manages the users profiles information (name, contact information, insurance), it also contain a list of the user's pets on the app record.
Pet class: Stores each individual animal detaisl (name, bred type, age, medical hisotry), as well tracks each task that was assigned to them from the pet's owner.
Tasks class: Holds care activity details (start time of the task, duration, priority levle, completion status).
Schedule class: Response for sorting each of the task in order of priority, chronologically, and inspecting for schedule conflicts. 


**b. Design changes**

- Did your design change during implementation?

Yes, I made changes to classes skeletion after review it with my AI coding assistant. 

- If yes, describe at least one change and why you made it.

the changes I have made with AI are: adding a direct pet relationship to task, so the program can identify which task belongs to which pet. Set a default task frequency, so the tasks can supporot the planned value of "once" and "daily", as well as the default value of one-time tasks when they are new task inputed. Final change is added owner avaiability to schedule class, so the schedule class can determine when an owner is avialable or not.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff my schedule makes is that it checks for any overlapping tasks instead of only checking whether two or more tasks have the exact same start time. With the note that this may cause it to create more warnings.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable for this scenario because users (pet owners) would prefer to receive multiple warnings and reminders rather than miss one and get informed at the last minute that two or more tasks need equal attention at the same time.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
