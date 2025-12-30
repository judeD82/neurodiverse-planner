import streamlit as st
from datetime import date

from logic import (
    calculate_capacity_score,
    determine_day_type,
    get_base_structure,
    apply_work_mode_modifier,
    build_day_summary,
    save_day_entry,
    generate_ml_reflection
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
# Visual language
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
    "Progress Day": "If you’re stuck, try setting a 25-minute timer.",
    "Flow Day": "If you’re stuck, remove one distraction before starting."
}


def soft_card():
    return st.container(border=True)


# -------------------------------------------------
# Intro
# -------------------------------------------------

st.markdown("## Daily Capacity Planner")
st.markdown(
    "A calm, capacity-aware planning tool for neurodivergent freelancers.\n\n"
    "**This tool listens. It does not optimise.**"
)

with st.expander("About patterns & learning"):
    st.markdown(
        "**Quiet mode:** The tool notices recurring shapes over time.\n\n"
        "**Plain mode:** It groups similar days to reflect patterns.\n\n"
        "**Explicit mode:** This uses simple machine learning to group similar days.\n\n"
        "Nothing is predicted. Nothing is judged. Nothing is sent anywhere."
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

st.markdown(f"### {DAY_TYPE_ICONS.get(day_type, '')} {day_type}")
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
    essential_task = st.text_input("One essential thing")

    support_task = None
    optional_task = None

    if day_type in ["Maintenance Day", "Progress Day", "Flow Day"]:
        support_task = st.text_input("One supportive task")

    if st.checkbox("Add optional bonus task"):
        optional_task = st.text_input("Optional task")

st.markdown("---")

# -------------------------------------------------
# Save + Learn
# -------------------------------------------------

with soft_card():
    st.markdown("### Save your plan")

    enable_learning = st.checkbox(
        "Allow this tool to notice patterns over time (local only)",
        value=False
    )

    if st.button("Create text summary") and essential_task:
        if enable_learning:
            save_day_entry(
                day_type,
                work_mode,
                capacity_score,
                energy,
                focus,
                emotional_load
            )

        summary_text = build_day_summary(
            energy,
            focus,
            emotional_load,
            work_mode,
            day_type,
            final_structure,
            essential_task,
            support_task,
            optional_task
        )

        st.download_button(
            "Download .txt",
            summary_text,
            file_name=f"daily_plan_{date.today().isoformat()}.txt",
            mime="text/plain"
        )

        st.success("Your plan is ready. You can stop here.")

st.markdown("---")

# -------------------------------------------------
# ML Reflection (OPT-IN RESULT)
# -------------------------------------------------

st.markdown("### Quiet patterns")

ml_reflection = generate_ml_reflection()
if ml_reflection:
    st.info(ml_reflection)
else:
    st.caption("Patterns will appear here gently over time.")

st.markdown("---")

# -------------------------------------------------
# Close
# -------------------------------------------------

st.markdown("### Closing the day")
st.checkbox("I worked within my capacity today")
st.text_input("One word for today")

st.progress(1.0, text="That’s enough for today.")

st.caption(
    "This tool reflects experience. "
    "You remain in control."
)
