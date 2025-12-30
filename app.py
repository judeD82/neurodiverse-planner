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
# Page config
# -------------------------------------------------

st.set_page_config(
    page_title="Daily Capacity Planner",
    layout="centered"
)

# -------------------------------------------------
# Soft intro
# -------------------------------------------------

st.markdown("## Daily Capacity Planner")
st.markdown(
    "A gentle, capacity-aware planning tool for neurodivergent freelancers.\n\n"
    "This adapts to how you feel **today**. There is nothing to optimise."
)

st.markdown("---")

# -------------------------------------------------
# How this works (optional)
# -------------------------------------------------

with st.expander("How to use this"):
    st.markdown(
        "- Answer honestly. This is for *you*.\n"
        "- The structure responds to your capacity, not willpower.\n"
        "- Low-energy days are valid days.\n"
        "- You can stop at any point."
    )

# -------------------------------------------------
# 1. Check-in
# -------------------------------------------------

st.markdown("### How are you showing up today?")

energy = st.slider(
    "Energy",
    1, 5, 3,
    help="Physical and mental energy combined"
)

focus = st.slider(
    "Focus",
    1, 5, 3,
    help="How easy it feels to concentrate"
)

emotional_load = st.slider(
    "Emotional load",
    1, 5, 3,
    help="Stress, anxiety, background emotional noise"
)

st.markdown("---")

# -------------------------------------------------
# 2. Context
# -------------------------------------------------

st.markdown("### What kind of workday is this?")

work_mode = st.radio(
    "",
    ["Client Day", "Solo Day"],
    horizontal=True
)

st.markdown("---")

# -------------------------------------------------
# 3. Interpretation
# -------------------------------------------------

capacity_score = calculate_capacity_score(
    energy=energy,
    focus=focus,
    emotional_load=emotional_load
)

day_type = determine_day_type(capacity_score)

st.markdown(f"### Today looks like a **{day_type}**")
st.caption("This is descriptive, not a judgement.")

base_structure = get_base_structure(day_type)
final_structure = apply_work_mode_modifier(base_structure, work_mode)

for item in final_structure:
    st.markdown(f"- {item}")

st.markdown("---")

# -------------------------------------------------
# 4. What would be enough?
# -------------------------------------------------

st.markdown("### What would be enough for today?")

essential_task = st.text_input(
    "One essential thing",
    placeholder="Small, concrete, and realistic"
)

support_task = None
optional_task = None

if day_type in ["Maintenance Day", "Progress Day", "Flow Day"]:
    support_task = st.text_input(
        "One supportive or low-effort task",
        placeholder="Admin, prep, follow-up"
    )

add_optional = st.checkbox("Add an optional bonus task")
if add_optional:
    optional_task = st.text_input(
        "Optional task",
        placeholder="Only if it feels genuinely light"
    )

st.markdown("---")

# -------------------------------------------------
# 5. Save
# -------------------------------------------------

st.markdown("### Save your plan")

st.caption(
    "Nothing is stored. This is just for you."
)

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

st.markdown("---")

# -------------------------------------------------
# 6. Gentle close
# -------------------------------------------------

st.markdown("### Closing the day")

st.checkbox("I worked within my capacity today")
st.text_input("One word for today", placeholder="Optional")

st.caption(
    "This is not a productivity system. "
    "It’s a way of listening to your capacity."
)
