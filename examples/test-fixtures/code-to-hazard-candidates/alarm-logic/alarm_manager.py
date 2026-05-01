"""SpO2 alarm state machine for neonatal monitoring."""

# Alarm thresholds
ALARM_SPO2_LOW_CRITICAL = 80
ALARM_SPO2_LOW_WARNING = 88
ALARM_SPO2_HIGH_WARNING = 97


class AlarmState:
    INACTIVE = "INACTIVE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    SILENCED = "SILENCED"


class SpO2AlarmManager:
    """State machine managing SpO2 alarm transitions."""

    def __init__(self):
        self.alarm_state = AlarmState.INACTIVE
        self.silence_remaining_sec = 0
        self.consecutive_violations = 0

    def evaluate_spo2(self, spo2: float) -> str:
        """Evaluate SpO2 value and transition alarm state.

        Returns the new alarm state.
        """
        if self.alarm_state == AlarmState.SILENCED:
            if self.silence_remaining_sec > 0:
                self.silence_remaining_sec -= 1
                return self.alarm_state
            # Silence expired — re-evaluate
            self.alarm_state = AlarmState.INACTIVE

        if spo2 < ALARM_SPO2_LOW_CRITICAL:
            self.alarm_state = AlarmState.CRITICAL
            self.consecutive_violations += 1
            trigger_alarm("CRITICAL", spo2)
        elif spo2 < ALARM_SPO2_LOW_WARNING:
            if self.consecutive_violations >= 3:
                # Escalate to critical after 3 consecutive warnings
                self.alarm_state = AlarmState.CRITICAL
                trigger_alarm("CRITICAL", spo2)
            else:
                self.alarm_state = AlarmState.WARNING
                self.consecutive_violations += 1
                trigger_alarm("WARNING", spo2)
        elif spo2 > ALARM_SPO2_HIGH_WARNING:
            self.alarm_state = AlarmState.WARNING
            trigger_alarm("WARNING", spo2)
        else:
            self.consecutive_violations = 0
            self.alarm_state = AlarmState.INACTIVE

        return self.alarm_state

    def silence_alarm(self, duration_sec: int = 120):
        """Silence the current alarm for a specified duration."""
        self.alarm_state = AlarmState.SILENCED
        self.silence_remaining_sec = duration_sec

    def acknowledge_alarm(self):
        """Acknowledge alarm — resets escalation counter but keeps state."""
        self.consecutive_violations = 0


def trigger_alarm(severity: str, value: float):
    """Send alarm notification to nursing station."""
    print(f"ALARM [{severity}]: SpO2 = {value}%")
