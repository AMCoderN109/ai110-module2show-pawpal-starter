from pawpal_system import Owner, Pet, Schedule, Task


# These helpers make the terminal schedule easier to read.
def format_frequency(frequency: str) -> str:
    labels = {
        "once": "Once",
        "daily": "Daily",
        "weekly": "Weekly",
        "biweekly": "Every two weeks",
    }
    return labels[frequency]


def format_time(time_value: str) -> str:
    hour, minute = (int(value) for value in time_value.split(":"))
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d} {suffix}"


def main() -> None:
    # Create the owner, pets, and their care tasks for the sample schedule.
    owner = Owner(first_name="Amelia")
    toffee = Pet(
        name="Toffee",
        species="dog",
        breed_type="black and brown mixed breed",
    )
    chuy = Pet(
        name="Chuy",
        species="dog",
        breed_type="purebred Yorkshire Terrier",
    )

    owner.add_pet(toffee)
    owner.add_pet(chuy)

    toffee.add_task(
        Task(
            description="Bathe Toffee",
            start_time="18:00",
            duration_minutes=30,
            priority_level="medium",
            frequency="biweekly",
            completed=True,
        )
    )
    chuy.add_task(
        Task(
            description="Bathe Chuy",
            start_time="18:30",
            duration_minutes=30,
            priority_level="medium",
            frequency="biweekly",
        )
    )
    chuy.add_task(
        Task(
            description="Walk Chuy",
            start_time="07:30",
            duration_minutes=30,
            priority_level="high",
            frequency="daily",
        )
    )
    toffee.add_task(
        Task(
            description="Cut Toffee's nails",
            start_time="19:15",
            duration_minutes=15,
            priority_level="low",
            frequency="biweekly",
        )
    )
    toffee.add_task(
        Task(
            description="Walk Toffee",
            start_time="07:30",
            duration_minutes=30,
            priority_level="high",
            frequency="daily",
        )
    )
    chuy.add_task(
        Task(
            description="Cut Chuy's nails",
            start_time="19:30",
            duration_minutes=15,
            priority_level="low",
            frequency="biweekly",
        )
    )

    schedule = Schedule(owner)
    scheduled_tasks = schedule.sort_by_time()

    print("=" * 42)
    print("           TODAY'S SCHEDULE")
    print("=" * 42)
    print(f"Owner: {owner.first_name}")

    current_time = None
    for task in scheduled_tasks:
        if task.start_time != current_time:
            current_time = task.start_time
            print(f"\n{format_time(current_time)}")
            print("-" * 42)

        pet_name = task.pet.name if task.pet else "Unknown pet"
        print(f"  Task:      {task.description}")
        print(f"  Pet:       {pet_name}")
        print(f"  Duration:  {task.duration_minutes} minutes")
        print(f"  Priority:  {task.priority_level.title()}")
        print(f"  Frequency: {format_frequency(task.frequency)}")
        print()

    filtered_tasks = schedule.filter_tasks(
        pet_name="Toffee",
        completed=False,
    )
    print("=" * 42)
    print("INCOMPLETE TASKS FOR TOFFEE")
    print("=" * 42)
    for task in scheduled_tasks:
        if task in filtered_tasks:
            print(f"- {format_time(task.start_time)} - {task.description}")

    conflict_warnings = schedule.conflict_warnings()
    print("=" * 42)
    print("CONFLICT REMINDERS")
    print("=" * 42)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"- {warning}")
    else:
        print("No overlapping tasks detected.")


if __name__ == "__main__":
    main()