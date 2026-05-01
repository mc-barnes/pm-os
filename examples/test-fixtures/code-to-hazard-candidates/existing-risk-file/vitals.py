"""Vitals processing module with threshold checks and EHR integration."""


def check_heart_rate(hr: int) -> str:
    """Check heart rate against alarm thresholds."""
    if hr < 80:
        trigger_alarm("bradycardia", hr)
        return "CRITICAL"
    if hr > 200:
        trigger_alarm("tachycardia", hr)
        return "CRITICAL"
    return "NORMAL"


def check_temperature(temp: float) -> str:
    """Check temperature against clinical thresholds."""
    if temp < 36.0:
        return "hypothermia"
    if temp > 38.5:
        return "fever"
    return "normal"


def write_vitals_to_ehr(patient_id: str, vitals: dict):
    """Write vitals observation to EHR via FHIR Observation resource."""
    observation = Observation(patient_id=patient_id, values=vitals)
    ehr.write(observation)


def trigger_alarm(alarm_type: str, value: float):
    """Trigger clinical alarm."""
    print(f"ALARM: {alarm_type} = {value}")
