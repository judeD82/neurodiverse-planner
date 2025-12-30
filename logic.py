def calculate_day_type(energy, focus, emotional_load):
    capacity_score = energy + focus - emotional_load

    if capacity_score <= 3:
        return "Survival Day"
    elif capacity_score <= 6:
        return "Maintenance Day"
    elif capacity_score <= 8:
        return "Progress Day"
    else:
        return "Flow Day"


def day_structure(day_type):
    structures = {
        "Survival Day": [
            "Choose one essential task only",
            "Do one grounding or body-based activity",
            "Stopping early is allowed"
        ],
        "Maintenance Day": [
            "Complete 2–3 light or admin tasks",
            "One short focused block (25 minutes)",
            "One reset or transition break"
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
