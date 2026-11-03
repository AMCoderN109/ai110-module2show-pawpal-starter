from datetime import date, timedelta

from pawpal_system import Owner, Pet, Schedule, Task


# This test checks that a task can be marked as completed.
def test_task_completion_changes_status() -> None:
    task = Task(description="Morning walk")

    task.mark_complete()

    assert task.completed is True


# This test checks that a pet receives a new task.
def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Toffee")
    task = Task(description="Bath")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_completing_recurring_task_adds_next_occurrence() -> None:
    pet = Pet(name="Toffee")
    task = Task(
        description="Walk",
        frequency="weekly",
        due_date=date(2026, 11, 3),
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is not None
    assert task.completed is True
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 11, 10)
    assert next_task.pet is pet
    assert len(pet.tasks) == 2


def test_recurring_task_intervals_match_frequency() -> None:
    expected_intervals = {
        "daily": 1,
        "weekly": 7,
        "biweekly": 14,
    }

    for frequency, days in expected_intervals.items():
        pet = Pet(name="Toffee")
        task = Task(
            description="Care",
            frequency=frequency,
            due_date=date(2026, 11, 3),
        )
        pet.add_task(task)

        next_task = task.mark_complete()

        assert next_task is not None
        assert next_task.due_date == date(2026, 11, 3) + timedelta(days=days)


def test_completing_once_task_does_not_add_another_task() -> None:
    pet = Pet(name="Toffee")
    task = Task(description="Bath", due_date=date(2026, 11, 3))
    pet.add_task(task)

    assert task.mark_complete() is None
    assert task.mark_complete() is None
    assert len(pet.tasks) == 1


def test_conflict_warnings_identify_same_pet_overlaps() -> None:
    pet = Pet(name="Toffee")
    pet.add_task(Task(description="Walk", start_time="08:00", duration_minutes=30))
    pet.add_task(Task(description="Medication", start_time="08:15", duration_minutes=10))
    owner = Owner(pets=[pet])

    warnings = Schedule(owner).conflict_warnings()

    assert warnings == [
        "Warning: Toffee's tasks 'Walk' and 'Medication' overlap."
    ]


def test_conflict_warnings_identify_different_pet_overlaps() -> None:
    toffee = Pet(name="Toffee")
    chuy = Pet(name="Chuy")
    toffee.add_task(Task(description="Walk Toffee", start_time="08:00", duration_minutes=30))
    chuy.add_task(Task(description="Feed Chuy", start_time="08:15", duration_minutes=10))
    owner = Owner(pets=[toffee, chuy])

    warnings = Schedule(owner).conflict_warnings()

    assert warnings == [
        "Warning: Walk Toffee for Toffee and Feed Chuy for Chuy overlap."
    ]


def test_back_to_back_tasks_do_not_create_conflict_warning() -> None:
    pet = Pet(name="Toffee")
    pet.add_task(Task(description="Walk", start_time="08:00", duration_minutes=30))
    pet.add_task(Task(description="Feed", start_time="08:30", duration_minutes=10))
    owner = Owner(pets=[pet])

    assert Schedule(owner).conflict_warnings() == []