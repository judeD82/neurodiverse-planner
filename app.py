import streamlit as st
from logic import calculate_day_type, day_structure

st.set_page_config(page_title="Neurodiverse Freelancer Planner")

st.title("Daily Capacity Planner")
st.write("A gentle way to structure your freelance day based on how you actually feel.")

st.header("1. Quick check-in")

energy = st.slider("Energy level", 1, 5, 3)
focus = st.slider("Focus clarity", 1, 5, 3)
emotional_load = st.slider("Emotional load", 1, 5, 3)

st.header("2. Today’s shape")

day_type = calculate_day_type(energy, focus, emotional_load)

st.subheader(f"Today is a **{day_type}**")

structure = day_structure(day_type)
for item in structure:
    st.write(f"- {item}")

st.header("3. Define success (gently)")

essential_task = st.text_input("One thing that would make today feel okay:")

if day_type in ["Progress Day", "Flow Day"]:
    support_task = st.text_input("One supporting task:")
else:
    support_task = None

optional = st.checkbox("Add an optional task")
optional_task = st.text_input("Optional task (only if it feels light)") if optional else None

st.header("4. Close the loop")

st.checkbox("I worked within my capacity today")
st.text_input("One word for today")
