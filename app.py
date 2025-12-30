import streamlit as st

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
    page_title="Neurodiverse Freelancer Planner",
    layout="centered"
)

# -------------------------------------------------
# Intro
# -------------------------------------------------

st.title("Daily Capacity Planner")
st.write(
    "This tool helps you structure your freelance workday "
    "based on energy, focus, and emotional load — not willpower."
)

# -------------------------------------------------
# 1. Check-in
# -------------------------------------------------

st.header("1. Quick check-in")

energy = st.slider(
    "Energy level",
    min_value=1,
    max_value=5,
    value=3,
    help="Physical and mental energy combined"
)

focus = st.slider(
    "Focus clarity",
    min_value=1,
    max_value=5,
    value=3,
    help="How easy it feels to concentrate"
)

emotional_load = st.slider(
    "Emotional load",
    min_value=1,
    max_value=5,
    value=3,
    help="Stress, anxiety, emotional processing, background noise"
)

# -------------------------------------------------
# 2. Work mode
# -------------------------------------------------

st.header("2. Work context")

work_mode = st.radio(
    "What kind of workday is this?",
    options=["Client Day", "Solo Day"],
    help="Client-facing work often consumes more emotional energy"
)

# -------------------------------------------------
# 3. Capacity interpretation
# -------------------------------------------------

st.header("3. Today’s shape")

capacity_score = calculate_capacity_score(
    energy=energy,
    focus=focus,
    emotional_load=emotional_load
)

day_type = determine_day_type(capacity_score)

st.subheader(f"Today is a **{day_type}**")
st.caption(f"Capacity score: {capacity_score}")

base_structure = get_base_structure(day_type)
final_structure = apply_work_mode_modifier(base_structure, work_mode)

for item in final_structure:
    st.write(f"- {item}")

# -------------------------------------------------
# 4. Define success (gently)
# -------------------------------------------------

st.header("4. Define success")

essential_task = st.text_input(
    "One thing that would make today feel okay:",
    placeholder="Keep this small and concrete"
)

support_task = None
optional_task = None

if day_type in ["Maintenance Day", "Progress Day", "Flow Day"]:
    support_task = st.text_input(
        "One supporting or low-friction task:",
        placeholder="Admin, prep, follow-up, etc."
    )

add_optional = st.checkbox("Add an optional task (only if it feels light)")
if add_optional:
    optional_task = st.text_input(
        "Optional task:",
        placeholder="This is a bonus, not a requirement"
    )

# -------------------------------------------------
# 5. Save / export
# -------------------------------------------------

st.header("5. Save your day")

st.write(
    "You can save this plan as a simple text file. "
    "Nothing is stored or tracked."
)

if st.button("Generate day summary"):
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
        label="Download as .txt",
        data=summary_text,
        file_name="daily_plan.txt",
        mime="text/plain"
    )

# -------------------------------------------------
# 6. Close (optional reflection)
# -------------------------------------------------

st.header("6. Close the loop")

st.checkbox("I worked within my capacity today")
st.text_input("One word for today (optional)")
