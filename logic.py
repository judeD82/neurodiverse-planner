from datetime import date
import json
import os
import numpy as np
from sklearn.cluster import KMeans

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
# Structures
# -------------------------------------------------

def get_base_structure(day_type):
    return {
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
    }.get(day_type, [])


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
# Local pattern memory
# -------------------------------------------------

def save_day_entry(day_type, work_mode, capacity_score, energy, focus, emotional_load):
    entry = {
        "date": date.today().isoformat(),
        "day_type": day_type,
        "work_mode": work_mode,
        "capacity": capacity_score,
        "energy": energy,
        "focus": focus,
        "emotional_load": emotional_load
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


# -------------------------------------------------
# ML Pattern Clustering (OPT-IN)
# -------------------------------------------------

def generate_ml_reflection():
    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if len(data) < 6:
        return None

    features = []
    for d in data:
        work_mode_encoded = 1 if d["work_mode"] == "Client Day" else 0
        features.append([
            d["energy"],
            d["focus"],
            d["emotional_load"],
            d["capacity"],
            work_mode_encoded
        ])

    X = np.array(features)

    try:
        kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
        labels = kmeans.fit_predict(X)
    except Exception:
        return None

    recent_label = labels[-1]
    cluster_count = list(labels).count(recent_label)

    return (
        "Some of your days naturally group together.\n\n"
        f"This current pattern has appeared **{cluster_count} times** recently.\n\n"
        "This isn’t a prediction or recommendation — just a reflection of lived patterns."
    )


# -------------------------------------------------
# Export
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
