import time
from collections import deque
from enum import StrEnum

from system_state import state

MAX_READINGS = 30

buffer = deque(maxlen=MAX_READINGS)

DISTANCE_THRESHOLD_CM = 5.0


class MotionDirection(StrEnum):
    ENTER = "enter"
    LEAVE = "leave"


def infer_direction(lookback_seconds=15.0) -> MotionDirection | None:
    if not buffer or len(buffer) < 3:
        return None

    now = time.time()
    recent = [d for (t, d) in buffer if now - t <= lookback_seconds]
    if len(recent) < 3:
        # fallback to using all available
        recent = [d for (_t, d) in buffer]
    if len(recent) < 3:
        return None

    half = len(recent) // 2
    older = recent[:half]
    newer = recent[half:]
    older_avg = sum(older) / len(older)
    newer_avg = sum(newer) / len(newer)

    diff = older_avg - newer_avg
    if diff > DISTANCE_THRESHOLD_CM:
        return MotionDirection.ENTER
    if -diff > DISTANCE_THRESHOLD_CM:
        return MotionDirection.LEAVE

    return None


def handle_dus(payload):
    value = payload.get('value')
    try:
        buffer.append((time.time(), float(value)))
        print(f"[DUS] distance={value}")
    except Exception as e:
        print(f"✗ DUS handler error: {e}")
