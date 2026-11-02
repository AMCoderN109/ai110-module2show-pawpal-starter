from pawpal_system import Pet, Task


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