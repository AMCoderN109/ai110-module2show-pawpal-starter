"""Core data models for the PawPal+ pet-care planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_FREQUENCIES = {"once", "daily", "weekly", "biweekly"}

# These are the main changes made during implementation.
# Tasks now support pet relationships, validation, and biweekly care.
# Pets and owners can manage their tasks, and schedules can sort and find conflicts.


def _time_as_minutes(start_time: str) -> int:
    """Convert a 24-hour HH:MM time into minutes after midnight."""
    try:
        parsed_time = datetime.strptime(start_time, "%H:%M")
    except ValueError as error:
        raise ValueError(
            "Time values must use the 24-hour HH:MM format."
        ) from error
    return parsed_time.hour * 60 + parsed_time.minute


@dataclass
class Task:
    """A care task assigned to a pet."""

    description: str = ""
    start_time: str = ""
    duration_minutes: int = 0
    priority_level: str = "medium"
    frequency: str = "once"
    completed: bool = False
    pet: Pet | None = None
    due_date: date = field(default_factory=date.today)

    def _recurrence_days(self) -> int | None:
        """Return the interval, in days, for this task's recurrence."""
        recurrence_days = {
            "daily": 1,
            "weekly": 7,
            "biweekly": 14,
        }
        return recurrence_days.get(self.frequency)

    def mark_complete(self) -> Task | None:
        """Complete the task and add its next occurrence when it recurs.

        Returns:
            The new incomplete task for a recurring task, or ``None`` for
            one-time tasks, unassigned tasks, or tasks already completed.
        """
        if self.completed:
            return None

        self.completed = True
        days_until_next = self._recurrence_days()
        if days_until_next is None or self.pet is None:
            return None

        next_task = Task(
            description=self.description,
            start_time=self.start_time,
            duration_minutes=self.duration_minutes,
            priority_level=self.priority_level,
            frequency=self.frequency,
            due_date=self.due_date + timedelta(days=days_until_next),
        )
        self.pet.add_task(next_task)
        return next_task

    def update_priority(self, new_priority: str) -> None:
        """Update the task priority after checking its value."""
        normalized_priority = new_priority.strip().lower()
        if normalized_priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}."
            )
        self.priority_level = normalized_priority

    def __post_init__(self) -> None:
        """Validate task values when a task is created."""
        self.update_priority(self.priority_level)
        normalized_frequency = self.frequency.strip().lower()
        if normalized_frequency not in VALID_FREQUENCIES:
            raise ValueError(
                f"Frequency must be one of: {', '.join(sorted(VALID_FREQUENCIES))}."
            )
        self.frequency = normalized_frequency
        if self.duration_minutes < 0:
            raise ValueError("Duration cannot be negative.")
        if self.start_time:
            _time_as_minutes(self.start_time)


@dataclass
class Pet:
    """A pet and its care history."""

    name: str = ""
    species: str = ""
    breed_type: str = ""
    age: int = 0
    medication_history: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task and connect it to this pet."""
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance.")
        if not any(existing_task is task for existing_task in self.tasks):
            self.tasks.append(task)
        task.pet = self

    def add_medical_record(self, record: str) -> None:
        """Add a non-empty medical record for the pet."""
        if not isinstance(record, str) or not record.strip():
            raise ValueError("Medical records must be non-empty text.")
        self.medication_history.append(record.strip())


@dataclass
class Owner:
    """An owner and the pets they care for."""

    first_name: str = ""
    last_name: str = ""
    age: int = 0
    contact_info: str = ""
    insurance_info: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        if not isinstance(pet, Pet):
            raise TypeError("pet must be a Pet instance.")
        if not any(existing_pet is pet for existing_pet in self.pets):
            self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks belonging to the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Schedule:
    """A schedule for an owner's pet-care tasks."""

    owner: Owner
    available_start_time: str = ""
    available_end_time: str = ""

    @staticmethod
    def _task_start_minutes(task: Task) -> int:
        """Convert a task's HH:MM start time to minutes after midnight."""
        return _time_as_minutes(task.start_time)

    @classmethod
    def _task_end_minutes(cls, task: Task) -> int:
        """Return the minutes after midnight when a task ends."""
        return cls._task_start_minutes(task) + task.duration_minutes

    def sort_by_time(self) -> list[Task]:
        """Return all owner tasks sorted by their HH:MM start time.

        Tasks without a start time are placed after tasks with scheduled
        times. The owner's original task lists are not changed.
        """
        tasks = self.owner.get_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (not bool(task.start_time), task.start_time),
        )

    def sort_by_priority(self) -> list[Task]:
        """Return the owner's tasks from highest to lowest priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda task: priority_order[task.priority_level],
        )

    def filter_tasks(self, pet_name: str, completed: bool) -> list[Task]:
        """Return tasks matching both a pet name and completion status.

        Pet-name matching ignores surrounding whitespace and capitalization.
        """
        tasks = self.owner.get_all_tasks()
        normalized_name = pet_name.strip().lower()
        return [
            task
            for task in tasks
            if (
                task.pet is not None
                and task.pet.name.strip().lower() == normalized_name
                and task.completed is completed
            )
        ]

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of scheduled tasks with overlapping time ranges.

        Tasks that start exactly when another task ends are considered
        back-to-back rather than conflicting.
        """
        scheduled_tasks = [
            task for task in self.owner.get_all_tasks() if task.start_time
        ]
        scheduled_tasks.sort(key=lambda task: _time_as_minutes(task.start_time))

        conflicts: list[tuple[Task, Task]] = []
        for index, first_task in enumerate(scheduled_tasks):
            first_end = self._task_end_minutes(first_task)
            for second_task in scheduled_tasks[index + 1 :]:
                second_start = self._task_start_minutes(second_task)
                if second_start >= first_end:
                    break
                conflicts.append((first_task, second_task))
        return conflicts

    def conflict_warnings(self) -> list[str]:
        """Return warning messages for same-pet and different-pet overlaps.

        The method reports conflicts as messages instead of raising errors,
        allowing the caller to display warnings while the program continues.
        """
        warnings = []
        for first_task, second_task in self.detect_conflicts():
            first_pet = first_task.pet.name if first_task.pet else "Unknown pet"
            second_pet = second_task.pet.name if second_task.pet else "Unknown pet"
            if first_task.pet is second_task.pet:
                warnings.append(
                    f"Warning: {first_pet}'s tasks "
                    f"'{first_task.description}' and "
                    f"'{second_task.description}' overlap."
                )
            else:
                warnings.append(
                    f"Warning: {first_task.description} for {first_pet} and "
                    f"{second_task.description} for {second_pet} overlap."
                )
        return warnings