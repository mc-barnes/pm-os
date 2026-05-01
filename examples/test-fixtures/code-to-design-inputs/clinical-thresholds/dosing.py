"""Weight-based dosing calculations for neonatal medications."""


CAFFEINE_DOSE_MG_PER_KG = 20  # loading dose
CAFFEINE_MAINTENANCE_MG_PER_KG = 5
SURFACTANT_DOSE_ML_PER_KG = 5.0
LIMIT_MAX_DOSE_MG = 100


def calculate_caffeine_loading_dose(weight_kg: float) -> float:
    """Calculate caffeine citrate loading dose based on weight.

    Per NeoFax guidelines: 20 mg/kg loading dose.
    """
    dose = weight_kg * CAFFEINE_DOSE_MG_PER_KG
    if dose > LIMIT_MAX_DOSE_MG:
        flash("WARNING: Calculated dose exceeds maximum limit", "error")
        dose = LIMIT_MAX_DOSE_MG
    return dose


def calculate_surfactant_dose(weight_kg: float) -> float:
    """Calculate surfactant dose for RDS treatment."""
    return weight_kg * SURFACTANT_DOSE_ML_PER_KG


def flash(message: str, category: str):
    """Stub for flash message display."""
    print(f"[{category}] {message}")
