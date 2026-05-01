"""ECG rhythm classification for cardiac monitoring — non-neonatal domain."""
import numpy as np


# Cardiac-specific thresholds (not neonatal defaults)
QRS_DURATION_MS_MAX = 120
PR_INTERVAL_MS_MAX = 200
QT_INTERVAL_MS_MAX = 440
HEART_RATE_BRADY_THRESHOLD = 60
HEART_RATE_TACHY_THRESHOLD = 100


def classify_rhythm(ecg_signal: list[float], sample_rate: int = 500) -> str:
    """Classify ECG rhythm from raw signal data.

    Returns rhythm classification: NSR, AFib, AFlutter, VTach, VFib, Asystole.
    """
    heart_rate = calculate_heart_rate(ecg_signal, sample_rate)
    qrs_width = measure_qrs_duration(ecg_signal, sample_rate)

    if heart_rate == 0:
        return "Asystole"
    if qrs_width > QRS_DURATION_MS_MAX and heart_rate > 150:
        risk_score = compute_vtach_probability(ecg_signal)
        if risk_score > 0.8:
            return "VTach"
    if is_irregular(ecg_signal):
        return "AFib"
    if heart_rate < HEART_RATE_BRADY_THRESHOLD:
        return "Bradycardia"
    if heart_rate > HEART_RATE_TACHY_THRESHOLD:
        return "Tachycardia"
    return "NSR"


def calculate_heart_rate(ecg_signal: list[float], sample_rate: int) -> int:
    """Calculate heart rate from R-R intervals."""
    # Simplified peak detection
    peaks = detect_r_peaks(ecg_signal, sample_rate)
    if len(peaks) < 2:
        return 0
    rr_intervals = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
    avg_rr = sum(rr_intervals) / len(rr_intervals)
    heart_rate = int(60 * sample_rate / avg_rr) if avg_rr > 0 else 0
    return heart_rate


def compute_vtach_probability(ecg_signal: list[float]) -> float:
    """Compute probability of ventricular tachycardia using ML model."""
    # model.predict would go here
    return 0.5  # placeholder


def measure_qrs_duration(ecg_signal: list[float], sample_rate: int) -> float:
    """Measure QRS complex duration in milliseconds."""
    return 80.0  # placeholder


def detect_r_peaks(ecg_signal: list[float], sample_rate: int) -> list[int]:
    """Detect R-peaks in ECG signal."""
    return []  # placeholder


def is_irregular(ecg_signal: list[float]) -> bool:
    """Detect irregular R-R intervals (atrial fibrillation indicator)."""
    return False  # placeholder
