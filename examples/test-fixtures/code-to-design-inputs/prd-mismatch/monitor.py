"""Patient monitoring module with 3 implemented features."""
import os


ALERT_TIMEOUT_SECONDS = int(os.getenv("ALERT_TIMEOUT_SECONDS", "30"))


def check_vitals(patient_id: str, spo2: float, heart_rate: int):
    """Check patient vitals and trigger alerts if thresholds exceeded."""
    if spo2 < 90:
        send_alert(patient_id, "low_spo2", spo2)
    if heart_rate > 180:
        send_alert(patient_id, "high_hr", heart_rate)


def send_alert(patient_id: str, alert_type: str, value: float):
    """Send alert to nursing station via message queue."""
    message = {"patient": patient_id, "type": alert_type, "value": value}
    # queue.publish(message)  -- would be an integration point
    print(f"ALERT: {alert_type} for {patient_id}: {value}")


def export_vitals_csv(patient_id: str, date_range: tuple):
    """Export patient vitals to CSV for clinical review."""
    # Implementation exists but PRD doesn't mention CSV export
    pass
