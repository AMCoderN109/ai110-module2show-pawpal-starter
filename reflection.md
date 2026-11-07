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

My schedule considers task start time, task duration, priority level, completion status, pet assingment, and tasks frequency. The start times and task duration are used to sort tasks and identify conflicts within the schedule. It also check for completed tasks and supports daily, weekly, and biweekly reappearence of tasks. 

- How did you decide which constraints mattered most?

I consider all the contraints matter because they are all useful for the application to work. But the ones I think have more matter are start time, task duration  because it helps us determine any conflicts/overlapping tasks within the scehdule. 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff my schedule makes is that it checks for any overlapping tasks instead of only checking whether two or more tasks have the exact same start time. With the note that this may cause it to create more warnings.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable for this scenario because users (pet owners) would prefer to receive multiple warnings and reminders rather than miss one and get informed at the last minute that two or more tasks need equal attention at the same time.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I use AI for multple things, i use it to give me suggestions of how do design a UML diagram, how they would approch improving the code, and explain concepts that were overcomplicated to have a better understand of what was the task or question at hand. 

- What kinds of prompts or questions were most helpful?
I think the kinds of prompts and questions that were most helpful where suggesttions where you ask AI how would you do, or how would you create this. Then analyze the result to figure if they are worth or how to find an even more simpler way to do it. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

I think the moment I didn't accept AI suggestion is when they suggest something that was an overcomplicate suggestion of adding a method that made the whole program uncessary complex for the level of program we have and what codepath was asking for. 

- How did you evaluate or verify what the AI suggested?

I evaluate and veyf what the AI suggested by what the goal was in each phase and part in the codepath instructions, but, also when AI tested a piece of code, I will also do it myself, testing the termeral. 


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

The behaviors I tested were task completion, sorting, task filtering, and confliction detction to name a few. 

- Why were these tests important?

These are important because they are some of the main functions of the application, without these things, things would be chaos. For instance, you would know which task of was completed, and you woudn't know if two of the task were overlapping due at the same time. 


**b. Confidence**

- How confident are you that your scheduler works correctly?

I am moderiately confident that my schdule works correctly, it pass all the terminal tests and doesn't show any errors. However as we update and upgrade feature we are bound to find some bugs that need some fixing. 

- What edge cases would you test next if you had more time?

Other edge cases I would have tested if I had more time, would be testing for negative value inputs, tasks without an assign pet, and extenting the time frame of more than a day, week, and biweek. 


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of this project I'm most satisfied with is the UML mermaid diagram because without in the start we would have the application as it is now.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If had another iteration, I would make the application maybe have a way easier maybe even faster way of delete tasks and any other information like owner information if they decide not to use the application anymore or just to update the information more easily.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

A couple of things I learn about designing systems and workign with AI is that is always a great I to get an idea, plan it, but be opening minded to add changes to as you go along. As well double check your work even if you get help with AI. 

