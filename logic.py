from datetime import date


# -----------------------------
# Core capacity calculation
# -----------------------------

def calculate_capacity_score(energy, focus, emotional_load):
    """
    Simple, transparent capacity model.
    Higher emotional load reduces usable capacity.
    """
    return energy + focus - emotional_load


def determine_day_type(capacity_score):
    """
    Maps capacity score to a named day type.
    Names are intentionally non-judgemental.
    """
    if capacity_score <= 3:
        return "Survival Day"
    elif capacity_score <= 6:
        return "Maintenance Day"
    elif capacity_score <= 8:
        return "Progress Day"
    else:
        return "Flow Day"


# -----------------------------
# Day structure logic
# -----------------------------

def get_base_structure(day_type):
    """
    Returns the baseline structure for each day type.
    Uses blocks and intentions, not time schedules.
    """
    structures = {
        "Survival Day": [
            "One essential task only",
            "One grounding or body-based activity",
            "Permission to stop early"
        ],
        "Maintenance Day": [
            "Two to three light or administrative tasks",
            "One short focused block (around 25 minutes)",
            "One intentional break or reset"
        ],
        "Progress Day": [
            "One priority task",
            "One supporting task",
            "One optional stretch task"
        ],
        "Flow Day": [
            "One deep work block (60–90 minutes)",
            "One creative or revenue-generating task",
            "One intentional closing ritual"
        ]
    }

    return structures.get(day_type, [])


def apply_work_mode_modifier(structure, work_mode):
    """
    Adjusts the structure slightly depending on whether
    the day is client-facing or solo.
    """
    modified = structure.copy()

    if work_mode == "Client Day":
        modified.append("Buffer time between interactions")
        modified.append("Low-demand task after client work")

    elif work_mode == "Solo Day":
        modified.append("Protect uninterrupted focus where possible")
        modified.append("Optional creative or exploratory time")

    return modified


# -----------------------------
# Gentle pattern reflection
# -----------------------------

def generate_pattern_reflection(day_type, work_mode):
    """
    Provides a soft reflective prompt.
    No tracking or judgement. Purely optional insight.
    """
    reflections = {
        "Survival Day": (
            "If days like this repeat, it may be a signal to reduce load "
            "or increase recovery. Today itself requires no fixing."
        ),
        "Maintenance Day": (
            "These days often keep everything running quietly in the background. "
            "They are more productive than they look."
        ),
        "Progress Day": (
            "You may notice these days appear when structure meets compassion. "
            "That balance is worth protecting."
        ),
        "Flow Day": (
            "Flow is welcome, but not required to justify rest later. "
            "Avoid borrowing energy from tomorrow."
        )
    }

    mode_note = (
        "Client-facing work often consumes more emotional energy than expected."
        if work_mode == "Client Day"
        else
        "Solo days can reveal natural rhythms when pressure is low."
    )

    return reflections.get(day_type, "") + " " + mode_note


# -----------------------------
# Text output builder
# -----------------------------

def build_day_summary(
    energy,
    focus,
    emotional_load,
    work_mode,
    day_type,
    structure,
    essential_task,
    support_task=None,
    optional_task=None
):
    """
    Produces a calm, human-readable .txt summary of the day.
    """

    today = date.today().isoformat()
    capacity_score = calculate_capacity_score(energy, focus, emotional_load)
    reflection = generate_pattern_reflection(day_type, work_mode)

    lines = []

    lines.append("NEURODIVERSE FREELANCER DAILY PLAN")
    lines.append(f"Date: {today}")
    lines.append("")
    lines.append(f"Work mode: {work_mode}")
    lines.append(f"Day type: {day_type}")
    lines.append(f"Capacity score: {capacity_score}")
    lines.append("")

    lines.append("SUGGESTED DAY STRUCTURE:")
    for item in structure:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("TASKS:")
    if essential_task:
        lines.append(f"* Essential: {essential_task}")
    if support_task:
        lines.append(f"* Support: {support_task}")
    if optional_task:
        lines.append(f"* Optional: {optional_task}")

    lines.append("")
    lines.append("REFLECTION:")
    lines.append(reflection)

    lines.append("")
    lines.append(
        "Reminder: This plan reflects capacity, not worth. "
        "Doing less than planned is still valid."
    )

    return "\n".join(lines)
