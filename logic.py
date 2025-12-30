from datetime import date
import json
import os

DATA_FILE = "pattern_memory.json"


# -------------------------------------------------
# Capacity model
# -------------------------------------------------

def calculate_capacity_score(energy, focus, emotional_load):
    return energy + focus - emotional_load


def determine_day_type(capacity_score):
    if capacity_score <= 3:
        return "Survival Day"
    elif capacity_score <= 6:
        return "Maintenance Day"
    elif capacity_score <= 8:
        return "Progress Day"
    else:
        return "Flow Day"


# -------------------------------------------------
# Day structures
# -------------------------------------------------

def get_base_structure(day_type):
    structures = {
        "Survival Day": [
            "One essential task only",
            "One grounding or body-based activity",
            "Permission to stop early"
        ],
        "Maintenance Day": [
            "Two to three light or administrative tasks",
            "One short focused block",
            "One intentional break"
        ],
        "Progress Day": [
            "One priority task",
            "One supporting task",
            "One optional stretch task"
        ],
        "Flow Day": [
            "One deep work block",
            "One creative or revenue-generating task",
            "One intentional closing ritual"
        ]
    }
    return structures.get(day_type, [])


def apply_work_mode_modifier(structure, work_mode):
    modified = structure.copy()

    if work_mode == "Client Day":
        modified.append("Buffer time between interactions")
        modified.append("Low-demand task after client work")
    else:
        modified.append("Protect uninterrupted focus")
        modified.append("Optional exploratory or creative time")

    return modified


# -------------------------------------------------
# Pattern memory (local, ethical)
# -------------------------------------------------

def save_day_entry(day_type, work_mode, capacity_score):
    entry = {
        "date": date.today().isoformat(),
        "day_type": day_type,
        "work_mode": work_mode,
        "capacity": capacity_score
    }

    data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = []

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_pattern_reflection():
    if not os.path.exists(DATA_FILE):
        return None

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return None

    if len(data) < 5:
        return None

    recent = data[-10:]
    day_types = [d["day_type"] for d in recent]
    work_modes = [d["work_mode"] for d in recent]

    most_common_day = max(set(day_types), key=day_types.count)

    reflections = [
        f"Recently, **{most_common_day}** days have been most common."
    ]

    if work_modes.count("Client Day") > work_modes.count("Solo Day"):
        reflections.append(
            "Client-facing days appear frequently. These often carry hidden emotional load."
        )

    reflections.append(
        "Patterns are information, not instructions. Nothing here needs fixing."
    )

    return " ".join(reflections)


# -------------------------------------------------
# Text export
# -------------------------------------------------

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
    lines = [
        "NEURODIVERSE FREELANCER DAILY PLAN",
        f"Date: {date.today().isoformat()}",
        "",
        f"Work mode: {work_mode}",
        f"Day type: {day_type}",
        f"Capacity score: {calculate_capacity_score(energy, focus, emotional_load)}",
        "",
        "SUGGESTED STRUCTURE:"
    ]

    for item in structure:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("TASKS:")
    lines.append(f"* Essential: {essential_task}")

    if support_task:
        lines.append(f"* Support: {support_task}")
    if optional_task:
        lines.append(f"* Optional: {optional_task}")

    lines.append("")
    lines.append(
        "This plan reflects capacity, not worth. "
        "Doing less than planned is still valid."
    )

    return "\n".join(lines)
