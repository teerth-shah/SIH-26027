from datetime import datetime, timedelta


def find_possible_windows(
    earliest_start: datetime,
    deadline: datetime,
    duration_minutes: int,
    interval_minutes: int = 60
):
    windows = []

    current_start = earliest_start

    while current_start + timedelta(minutes=duration_minutes) <= deadline:

        current_end = current_start + timedelta(
            minutes=duration_minutes
        )

        windows.append({
            "start": current_start,
            "end": current_end
        })

        current_start += timedelta(minutes=interval_minutes)

    return windows


def check_block_conflict(
    db,
    section_id: int,
    candidate_start,
    candidate_end
):
    from app.models.block import Block

    existing_blocks = db.query(Block).filter(
        Block.section_id == section_id,
        Block.status != "CANCELLED"
    ).all()

    for block in existing_blocks:

        if (
            candidate_start < block.planned_end
            and candidate_end > block.planned_start
        ):
            return True

    return False


def get_available_windows(
    db,
    section_id: int,
    earliest_start: datetime,
    deadline: datetime,
    duration_minutes: int,
    interval_minutes: int = 60
):
    candidate_windows = find_possible_windows(
        earliest_start=earliest_start,
        deadline=deadline,
        duration_minutes=duration_minutes,
        interval_minutes=interval_minutes
    )

    available_windows = []

    for window in candidate_windows:

        conflict = check_block_conflict(
            db=db,
            section_id=section_id,
            candidate_start=window["start"],
            candidate_end=window["end"]
        )

        if not conflict:
            available_windows.append(window)

    return available_windows