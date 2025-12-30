import streamlit as st
from datetime import date

from logic import (
    calculate_capacity_score,
    determine_day_type,
    get_base_structure,
    apply_work_mode_modifier,
    build_day_summary
)

# -------------------------------------------------
# Config
# -------------------------------------------------

st.set_page_config(
    page_title="Daily Capacity Planner",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Fancy mappings
# -------------------------------------------------

DAY_TYPE_ICONS = {
    "Survival Day": "🪶",
    "Maintenance Day": "⚖️",
    "Progress Day": "➡️",
    "Flow Day": "🌊"
}

DAY_TYPE_WHISPERS = {
    "Survival Day": "Move gently. The tide is low.",
    "Maintenance Day": "Quiet effort keeps things standing.",
    "Progress Day": "One step is still movement.",
    "Flow Day": "Stay present. Don’t rush the current."
}

STUCK_NUDGES = {
    "Survival Day": "If you’re stuck, try standing up and drinking some water.",
    "Maintenance Day": "If you’re stuck, try opening the task without committing to finishing it.",
    "Progress Day": "If you’re stuck, try setting a 25-minute timer for the priority task.",
    "Flow Day": "If you’re stuck, remove one distraction before you begin."
}

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def soft_card():
    return st.container(border=True)

# -------------------------------------------------
# Intro
# -------------------------------------------------

st.markdown("## Daily Capacity Planner")
st.markdown(
    "A calm, capacity-aware planning tool for neurodivergent freelancers.\n\n"
    "This adapts to how you feel **today**. There is nothing to optimise."
)

with st.expander("How this works"):
    st.markdown(
        "- Answer honestly. This is for *you*.\n"
        "- Structure adapts to capacity, not willpower.\n"
        "- Low-energy days are valid days.\n"
        "- You can stop at any point."
    )

st.markdown("---")

# -------------------------------------------------
# Check-in
# -------------------------------------------------

with soft_card():
    st.markdown("### How are you showing up today?")

    energy = st.slider("Energy", 1, 5, 3)
    focus = st.slider("Focus", 1, 5, 3)
    emotional_load = st.slider("Emotional load", 1, 5, 3)

st.markdown("---")

# -------------------------------------------------
# Context
# -------------------------------------------------

with soft_card():
    st.markdown("### What kind of workday is this?")
    work_mode = st.radio("", ["Client Day", "Solo Day"], horizontal=True)

st.markdown("---")

# -------------------------------------------------
# Interpretation
# -------------------------------------------------

capacity_score = calculate_capacity_score(energy, focus, emotional_load)
day_type = determine_day_type(capacity_score)

icon = DAY_TYPE_ICONS.get(day_type, "")
st.markdown(f"### {icon} {day_type}")
st.caption(DAY_TYPE_WHISPERS.get(day_type, ""))

base_structure = get_base_structure(day_type)
final_structure = apply_work_mode_modifier(base_structure, work_mode)

for item in final_structure:
    st.markdown(f"- {item}")

st.info(STUCK_NUDGES.get(day_type, ""))

st.markdown("---")

# -------------------------------------------------
# Tasks
# -------------------------------------------------

with soft_card():
    st.markdown("### What would be enough for today?")

    essential_task = st.text_input(
        "One essential thing",
        placeholder="Small, concrete, realistic"
    )

    support_task = None
    optional_task = None

    if day_type in ["Maintenance Day", "Progress Day", "Flow Day"]:
        support_task = st.text_input(
            "One supportive or low-effort task",
            placeholder="Admin, prep, follow-up"
        )

    if st.checkbox("Add an optional bonus task"):
        optional_task = st.text_input(
            "Optional task",
            placeholder="Only if it feels genuinely light"
        )

st.markdown("---")

# -------------------------------------------------
# Save
# -------------------------------------------------

with soft_card():
    st.markdown("### Save your plan")
    st.caption("Nothing is stored. This is just for you.")

    if not essential_task:
        st.caption("Add an essential task to enable export.")

    if st.button("Create text summary") and essential_task:
        summary_text = build_day_summary(
            energy=energy,
            focus=focus,
            emotional_load=emotional_load,
            work_mode=work_mode,
            day_type=day_type,
            structure=final_structure,
            essential_task=essential_task,
            support_task=support_task,
            optional_task=optional_task
        )

        st.download_button(
            "Download .txt",
            summary_text,
            file_name=f"daily_plan_{date.today().isoformat()}.txt",
            mime="text/plain"
        )

        st.success("Your plan is ready. You can stop here if you want.")

st.markdown("---")

# -------------------------------------------------
# Close
# -------------------------------------------------

st.markdown("### Closing the day")
st.checkbox("I worked within my capacity today")
st.text_input("One word for today", placeholder="Optional")

st.progress(1.0, text="That’s enough for today.")

st.caption(
    "This is not a productivity system. "
    "It’s a way of listening to your capacity."
)
