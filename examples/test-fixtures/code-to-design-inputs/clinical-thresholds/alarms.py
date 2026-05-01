"""Alarm management for neonatal SpO2 and heart rate monitoring."""


# Alarm threshold constants
ALARM_SPO2_LOW_CRITICAL = 80
ALARM_SPO2_LOW_WARNING = 88
ALARM_SPO2_HIGH_WARNING = 97
ALARM_HR_LOW_CRITICAL = 80
ALARM_HR_HIGH_CRITICAL = 200
THRESHOLD_APNEA_SECONDS = 20


def evaluate_spo2_alarm(spo2: float, gestational_age_weeks: int) -> str:
    """Evaluate SpO2 value against alarm thresholds.

    Returns alarm severity: CRITICAL, WARNING, or NONE.
    """
    if spo2 < ALARM_SPO2_LOW_CRITICAL:
        return "CRITICAL"
    elif spo2 < ALARM_SPO2_LOW_WARNING:
        return "WARNING"
    elif spo2 > ALARM_SPO2_HIGH_WARNING:
        return "WARNING"
    return "NONE"


def evaluate_heart_rate_alarm(heart_rate: int) -> str:
    """Evaluate heart rate against alarm thresholds."""
    if heart_rate < ALARM_HR_LOW_CRITICAL:
        return "CRITICAL"
    if heart_rate > ALARM_HR_HIGH_CRITICAL:
        return "CRITICAL"
    return "NONE"


def calculate_alarm_delay(severity: str) -> int:
    """Calculate delay before alarm activation (seconds)."""
    if severity == "CRITICAL":
        return 0  # immediate
    return 10  # WARNING: 10-second delay
