"""Core data models for the PawPal+ pet-care planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_FREQUENCIES = {"once", "daily", "biweekly"}

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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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

    def sort_by_time(self) -> list[Task]:
        """Return the owner's tasks in time order."""
        tasks = self.owner.get_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                _time_as_minutes(task.start_time)
                if task.start_time
                else float("inf")
            ),
        )

    def sort_by_priority(self) -> list[Task]:
        """Return the owner's tasks from highest to lowest priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda task: priority_order[task.priority_level],
        )

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose scheduled times overlap."""
        scheduled_tasks = [
            task for task in self.owner.get_all_tasks() if task.start_time
        ]
        scheduled_tasks.sort(key=lambda task: _time_as_minutes(task.start_time))

        conflicts: list[tuple[Task, Task]] = []
        for index, first_task in enumerate(scheduled_tasks):
            first_start = _time_as_minutes(first_task.start_time)
            first_end = first_start + first_task.duration_minutes
            for second_task in scheduled_tasks[index + 1 :]:
                second_start = _time_as_minutes(second_task.start_time)
                if second_start >= first_end:
                    break
                conflicts.append((first_task, second_task))
        return conflicts