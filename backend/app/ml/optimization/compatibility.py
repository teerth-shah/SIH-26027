def check_compatibility(task1: dict, task2: dict) -> tuple[bool, list]:
    """
    Checks if two maintenance tasks can be combined into a single block.
    """
    reasons = []
    is_compatible = True

    # 1. Must be on the same section
    if task1.get('section_id') != task2.get('section_id'):
        is_compatible = False
        reasons.append("Different sections")
    else:
        reasons.append("Same section")

    # 2. Departments must be compatible
    # Let's say all departments are compatible for now, as long as it's coordinated.
    reasons.append(f"Compatible departments ({task1.get('department')} & {task2.get('department')})")

    # 3. Check for overlapping deadlines (rough proxy for time window compatibility without generating all candidates first)
    if task1.get('deadline') and task2.get('deadline'):
        delta = abs((task1['deadline'] - task2['deadline']).total_seconds())
        # If deadlines are within 7 days of each other, we consider them compatible for planning
        if delta > 7 * 24 * 3600:
            is_compatible = False
            reasons.append("Deadlines are too far apart")
        else:
            reasons.append("Compatible deadlines")

    if not is_compatible:
        return False, reasons

    return True, reasons
