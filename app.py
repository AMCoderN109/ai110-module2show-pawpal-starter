import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(first_name=owner_name)

owner = st.session_state["owner"]
owner.first_name = owner_name

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.success(f"{pet_name} was added to {owner.first_name}'s pets.")

if owner.pets:
    st.write("Pets:")
    st.write(", ".join(pet.name for pet in owner.pets))
else:
    st.info("No pets yet. Add a pet before scheduling a task.")

st.markdown("### Tasks")
st.caption("Schedule a care task for one of your pets.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    start_time = st.text_input("Start time (HH:MM)", value="08:00")

frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "biweekly"])

if owner.pets:
    selected_pet_name = st.selectbox(
        "Pet for this task",
        [pet.name for pet in owner.pets],
    )

    if st.button("Schedule task"):
        selected_pet = next(
            pet for pet in owner.pets if pet.name == selected_pet_name
        )
        scheduled_task = Task(
            description=task_title,
            start_time=start_time,
            duration_minutes=int(duration),
            priority_level=priority,
            frequency=frequency,
        )
        selected_pet.add_task(scheduled_task)
        st.success(f"{task_title} was scheduled for {selected_pet.name}.")

if owner.get_all_tasks():
    st.write("Scheduled tasks:")
    st.table(
        [
            {
                "Pet": task.pet.name if task.pet else "Unknown",
                "Task": task.description,
                "Time": task.start_time,
                "Duration": task.duration_minutes,
                "Priority": task.priority_level,
                "Frequency": task.frequency,
            }
            for task in owner.get_all_tasks()
        ]
    )
else:
    st.info("No scheduled tasks yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an ordered schedule from the tasks you created.")

if st.button("Generate schedule"):
    schedule = Schedule(owner)
    scheduled_tasks = schedule.sort_by_time()
    st.write("Today's schedule:")
    for task in scheduled_tasks:
        pet_name = task.pet.name if task.pet else "Unknown"
        st.write(
            f"{task.start_time} - {task.description} for {pet_name} "
            f"({task.duration_minutes} minutes, {task.priority_level} priority)"
        )

    conflicts = schedule.detect_conflicts()
    if conflicts:
        st.warning(f"{len(conflicts)} scheduling conflict reminder(s) found.")
