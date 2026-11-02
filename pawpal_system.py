"""Core data models for the PawPal+ pet-care planner."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A care task assigned to a pet."""

    description: str = ""
    start_time: str = ""
    duration: str = ""
    priority_level: str = "medium"
    frequency: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def update_priority(self, new_priority: str) -> None:
        pass


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
        pass

    def add_medical_record(self, record: str) -> None:
        pass


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
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


@dataclass
class Schedule:
    """A schedule for an owner's pet-care tasks."""

    owner: Owner

    def sort_by_time(self) -> list[Task]:
        pass

    def sort_by_priority(self) -> list[Task]:
        pass

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        pass