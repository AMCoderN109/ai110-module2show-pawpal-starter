# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
==========================================
           TODAY'S SCHEDULE
==========================================
Owner: Amelia

7:30 AM
------------------------------------------
  Task:      Walk Toffee
  Pet:       Toffee
  Duration:  30 minutes
  Priority:  High
  Frequency: Daily

  Task:      Walk Chuy
  Pet:       Chuy
  Duration:  30 minutes
  Priority:  High
  Frequency: Daily


6:00 PM
------------------------------------------
  Task:      Bathe Toffee
  Pet:       Toffee
  Duration:  30 minutes
  Priority:  Medium
  Frequency: Every two weeks


6:30 PM
------------------------------------------
  Task:      Bathe Chuy
  Pet:       Chuy
  Duration:  30 minutes
  Priority:  Medium
  Frequency: Every two weeks


7:15 PM
------------------------------------------
  Task:      Cut Toffee's nails
  Pet:       Toffee
  Duration:  15 minutes
  Priority:  Low
  Frequency: Every two weeks


7:30 PM
------------------------------------------
  Task:      Cut Chuy's nails
  Pet:       Chuy
  Duration:  15 minutes
  Priority:  Low
  Frequency: Every two weeks

==========================================
CONFLICT REMINDERS
==========================================
- Reminder: Walk Toffee and Walk Chuy overlap.
```

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Schedule.sort_by_time()` | Sorts all owner tasks by their start time in `HH:MM` format. Tasks without a time go at the end. |
| Filtering | `Schedule.filter_tasks()` | Shows tasks for one pet and checks whether they are completed or incomplete. |
| Conflict handling | `Schedule.detect_conflicts()` and `Schedule.conflict_warnings()` | Checks whether task times overlap based on each task's start time and duration. It checks tasks for the same pet and different pets, then returns a warning instead of stopping the program. |
| Recurring tasks | `Task.mark_complete()` and `Task._recurrence_days()` | When a daily, weekly, or biweekly task is completed, it creates a new task for the next due date. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
