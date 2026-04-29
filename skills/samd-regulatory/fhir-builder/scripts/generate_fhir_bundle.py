#!/usr/bin/env python3
"""Generate valid FHIR R4 JSON bundles for medical device interoperability.

Standalone script using only Python stdlib. No external dependencies required.

Usage:
    python scripts/generate_fhir_bundle.py --example spo2
    python scripts/generate_fhir_bundle.py --example spo2 --output-dir ./my-output
"""

import argparse
import json
import os
import uuid
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOINC_SYSTEM = "http://loinc.org"
SNOMED_SYSTEM = "http://snomed.info/sct"
UCUM_SYSTEM = "http://unitsofmeasure.org"
OBSERVATION_CATEGORY_SYSTEM = (
    "http://terminology.hl7.org/CodeSystem/observation-category"
)
INTERPRETATION_SYSTEM = (
    "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
)
ISO11073_SYSTEM = "urn:iso:std:iso:11073:10101"


# ---------------------------------------------------------------------------
# Resource builders
# ---------------------------------------------------------------------------


def _uuid() -> str:
    """Return a new random UUID string."""
    return str(uuid.uuid4())


def _now_iso() -> str:
    """Return current UTC time in ISO 8601."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_patient(
    patient_id: str,
    identifier_value: str,
    family: str,
    given: list[str],
    gender: str,
    birth_date: str,
    birth_time: str | None = None,
) -> dict:
    """Build a FHIR R4 Patient resource with optional birth-time extension."""
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [
            {
                "system": "urn:oid:1.2.36.146.595.217.0.1",
                "value": identifier_value,
            }
        ],
        "name": [{"family": family, "given": given}],
        "gender": gender,
        "birthDate": birth_date,
    }
    if birth_time:
        patient["extension"] = [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                "valueDateTime": birth_time,
            }
        ]
    return patient


def build_observation_ga(
    obs_id: str,
    patient_ref: str,
    ga_weeks: float,
    effective_dt: str,
) -> dict:
    """Build a Gestational Age Observation (LOINC 76516-4)."""
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": OBSERVATION_CATEGORY_SYSTEM,
                        "code": "vital-signs",
                        "display": "Vital Signs",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": LOINC_SYSTEM,
                    "code": "76516-4",
                    "display": "Gestational age in weeks",
                }
            ]
        },
        "subject": {"reference": patient_ref},
        "effectiveDateTime": effective_dt,
        "valueQuantity": {
            "value": ga_weeks,
            "unit": "wk",
            "system": UCUM_SYSTEM,
            "code": "wk",
        },
    }


def build_observation_spo2(
    obs_id: str,
    patient_ref: str,
    device_ref: str,
    spo2_value: float,
    effective_dt: str,
    interpretation_code: str,
    interpretation_display: str,
    ref_range_low: float,
    ref_range_high: float,
    ref_range_text: str,
) -> dict:
    """Build a US Core-compliant SpO2 Observation (LOINC 59408-5)."""
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "meta": {
            "profile": [
                "http://hl7.org/fhir/us/core/StructureDefinition/us-core-pulse-oximetry"
            ]
        },
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": OBSERVATION_CATEGORY_SYSTEM,
                        "code": "vital-signs",
                        "display": "Vital Signs",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": LOINC_SYSTEM,
                    "code": "59408-5",
                    "display": "Oxygen saturation in Arterial blood by Pulse oximetry",
                }
            ]
        },
        "subject": {"reference": patient_ref},
        "effectiveDateTime": effective_dt,
        "valueQuantity": {
            "value": spo2_value,
            "unit": "%",
            "system": UCUM_SYSTEM,
            "code": "%",
        },
        "interpretation": [
            {
                "coding": [
                    {
                        "system": INTERPRETATION_SYSTEM,
                        "code": interpretation_code,
                        "display": interpretation_display,
                    }
                ]
            }
        ],
        "referenceRange": [
            {
                "low": {"value": ref_range_low, "unit": "%"},
                "high": {"value": ref_range_high, "unit": "%"},
                "text": ref_range_text,
            }
        ],
        "device": {"reference": device_ref},
    }


def build_device(
    device_id: str,
    identifier_value: str,
    manufacturer: str,
    model_number: str,
    serial_number: str,
) -> dict:
    """Build a FHIR R4 Device resource for a pulse oximeter."""
    return {
        "resourceType": "Device",
        "id": device_id,
        "identifier": [
            {
                "system": "urn:oid:1.2.840.10004.1.1.1.0.0.1.0.0.1.2680",
                "value": identifier_value,
            }
        ],
        "type": {
            "coding": [
                {
                    "system": SNOMED_SYSTEM,
                    "code": "706767009",
                    "display": "Pulse oximeter",
                }
            ]
        },
        "manufacturer": manufacturer,
        "modelNumber": model_number,
        "serialNumber": serial_number,
    }


def build_device_metric(
    metric_id: str,
    device_ref: str,
    calibration_time: str,
) -> dict:
    """Build a FHIR R4 DeviceMetric with calibration info."""
    return {
        "resourceType": "DeviceMetric",
        "id": metric_id,
        "type": {
            "coding": [
                {
                    "system": ISO11073_SYSTEM,
                    "code": "150456",
                    "display": "SpO2",
                }
            ]
        },
        "source": {"reference": device_ref},
        "category": "measurement",
        "calibration": [
            {
                "type": "two-point",
                "state": "calibrated",
                "time": calibration_time,
            }
        ],
    }


def build_diagnostic_report(
    report_id: str,
    patient_ref: str,
    observation_refs: list[str],
    effective_dt: str,
    conclusion: str,
    conclusion_code: str,
    conclusion_display: str,
) -> dict:
    """Build a FHIR R4 DiagnosticReport linking Observations."""
    return {
        "resourceType": "DiagnosticReport",
        "id": report_id,
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": LOINC_SYSTEM,
                    "code": "59408-5",
                    "display": "Oxygen saturation in Arterial blood by Pulse oximetry",
                }
            ]
        },
        "subject": {"reference": patient_ref},
        "effectiveDateTime": effective_dt,
        "result": [{"reference": ref} for ref in observation_refs],
        "conclusion": conclusion,
        "conclusionCode": [
            {
                "coding": [
                    {
                        "system": "urn:local:triage",
                        "code": conclusion_code,
                        "display": conclusion_display,
                    }
                ]
            }
        ],
    }


def build_collection_bundle(resources: list[dict]) -> dict:
    """Wrap resources in a FHIR R4 collection Bundle with UUID fullUrls."""
    timestamp = _now_iso()
    entries = []
    for resource in resources:
        entries.append(
            {
                "fullUrl": f"urn:uuid:{_uuid()}",
                "resource": resource,
            }
        )
    return {
        "resourceType": "Bundle",
        "id": _uuid(),
        "type": "collection",
        "timestamp": timestamp,
        "entry": entries,
    }


def build_capability_statement() -> dict:
    """Build a FHIR R4 CapabilityStatement for a medical device FHIR server."""
    return {
        "resourceType": "CapabilityStatement",
        "id": _uuid(),
        "status": "active",
        "date": _now_iso(),
        "kind": "instance",
        "software": {
            "name": "SpO2 AI Eval Pipeline FHIR Server",
            "version": "1.0.0",
        },
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                        ],
                        "searchParam": [
                            {
                                "name": "identifier",
                                "type": "token",
                                "documentation": "MRN or other patient identifier",
                            }
                        ],
                    },
                    {
                        "type": "Observation",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                            {"code": "create"},
                        ],
                        "searchParam": [
                            {
                                "name": "code",
                                "type": "token",
                                "documentation": "LOINC code for observation type",
                            },
                            {
                                "name": "date",
                                "type": "date",
                                "documentation": "Observation effective date",
                            },
                            {
                                "name": "patient",
                                "type": "reference",
                                "documentation": "Patient reference",
                            },
                        ],
                    },
                    {
                        "type": "Device",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                        ],
                        "searchParam": [
                            {
                                "name": "identifier",
                                "type": "token",
                                "documentation": "Device serial number or ID",
                            }
                        ],
                    },
                    {
                        "type": "DeviceMetric",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                        ],
                    },
                    {
                        "type": "DiagnosticReport",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"},
                            {"code": "create"},
                        ],
                        "searchParam": [
                            {
                                "name": "patient",
                                "type": "reference",
                                "documentation": "Patient reference",
                            },
                            {
                                "name": "code",
                                "type": "token",
                                "documentation": "Report code",
                            },
                        ],
                    },
                ],
            }
        ],
    }


# ---------------------------------------------------------------------------
# Example generators
# ---------------------------------------------------------------------------


def generate_spo2_example() -> tuple[dict, dict]:
    """Generate the SpO2 AI Eval Pipeline example bundle + capability statement.

    Returns:
        Tuple of (collection_bundle, capability_statement).
    """
    effective_dt = "2026-01-15T08:30:00Z"
    calibration_dt = "2026-01-15T06:00:00Z"

    # IDs for internal references
    patient_id = "pat-neo-001"
    device_id = "dev-pulseox-001"
    obs_ga_id = "obs-ga-001"
    obs_spo2_id = "obs-spo2-001"
    metric_id = "metric-spo2-001"
    report_id = "report-spo2-001"

    patient_ref = f"Patient/{patient_id}"
    device_ref = f"Device/{device_id}"

    # Build resources
    patient = build_patient(
        patient_id=patient_id,
        identifier_value="PAT-SPO2-001",
        family="Doe",
        given=["Baby"],
        gender="female",
        birth_date="2026-01-10",
        birth_time="2026-01-10T14:30:00Z",
    )

    obs_ga = build_observation_ga(
        obs_id=obs_ga_id,
        patient_ref=patient_ref,
        ga_weeks=28.0,
        effective_dt=effective_dt,
    )

    obs_spo2 = build_observation_spo2(
        obs_id=obs_spo2_id,
        patient_ref=patient_ref,
        device_ref=device_ref,
        spo2_value=91.0,
        effective_dt=effective_dt,
        interpretation_code="LL",
        interpretation_display="Critical low",
        ref_range_low=85.0,
        ref_range_high=95.0,
        ref_range_text="GA-adjusted range for extremely preterm (24-28 wk)",
    )

    device = build_device(
        device_id=device_id,
        identifier_value="DEV-MASIMO-001",
        manufacturer="Masimo",
        model_number="Rad-97",
        serial_number="SN-RAD97-20260115",
    )

    metric = build_device_metric(
        metric_id=metric_id,
        device_ref=device_ref,
        calibration_time=calibration_dt,
    )

    report = build_diagnostic_report(
        report_id=report_id,
        patient_ref=patient_ref,
        observation_refs=[
            f"Observation/{obs_ga_id}",
            f"Observation/{obs_spo2_id}",
        ],
        effective_dt=effective_dt,
        conclusion=(
            "SpO2 91.0% -- classified as URGENT for 28-week GA infant. "
            "Below GA-adjusted threshold of 85%. Recommend clinical review."
        ),
        conclusion_code="urgent",
        conclusion_display="Urgent triage",
    )

    bundle = build_collection_bundle(
        [patient, obs_ga, obs_spo2, device, metric, report]
    )
    capability = build_capability_statement()

    return bundle, capability


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {
    "Patient": ["resourceType", "id", "identifier", "name"],
    "Observation": ["resourceType", "status", "category", "code", "subject"],
    "Device": ["resourceType", "id", "identifier", "type"],
    "DeviceMetric": ["resourceType", "id", "type", "source", "category"],
    "DiagnosticReport": ["resourceType", "status", "code", "subject"],
    "Bundle": ["resourceType", "type", "entry"],
    "CapabilityStatement": ["resourceType", "status", "fhirVersion", "rest"],
}


def validate_resource(resource: dict) -> list[str]:
    """Check that required fields are present on a resource.

    Returns a list of error strings (empty = valid).
    """
    errors: list[str] = []
    rtype = resource.get("resourceType", "UNKNOWN")
    required = REQUIRED_FIELDS.get(rtype, [])
    for field in required:
        if field not in resource:
            errors.append(f"{rtype}: missing required field '{field}'")
    return errors


def validate_bundle(bundle: dict) -> list[str]:
    """Validate a FHIR Bundle and all contained resources."""
    errors = validate_resource(bundle)
    for i, entry in enumerate(bundle.get("entry", [])):
        res = entry.get("resource")
        if res is None:
            errors.append(f"entry[{i}]: missing 'resource'")
            continue
        if "fullUrl" not in entry:
            errors.append(f"entry[{i}]: missing 'fullUrl'")
        errors.extend(validate_resource(res))
    return errors


def print_summary(bundle: dict) -> None:
    """Print a summary of the generated bundle."""
    entries = bundle.get("entry", [])
    resource_types: dict[str, int] = {}
    for entry in entries:
        rtype = entry.get("resource", {}).get("resourceType", "Unknown")
        resource_types[rtype] = resource_types.get(rtype, 0) + 1

    print(f"\n{'='*60}")
    print(f"FHIR Bundle Summary")
    print(f"{'='*60}")
    print(f"  Bundle type:    {bundle.get('type')}")
    print(f"  Total entries:  {len(entries)}")
    print(f"  Timestamp:      {bundle.get('timestamp', 'N/A')}")
    print(f"\n  Resources:")
    for rtype, count in resource_types.items():
        print(f"    {rtype}: {count}")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point for CLI execution."""
    parser = argparse.ArgumentParser(
        description="Generate FHIR R4 JSON bundles for medical device interoperability."
    )
    parser.add_argument(
        "--example",
        choices=["spo2"],
        required=True,
        help="Example bundle to generate (currently: spo2).",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write output files (default: output/).",
    )
    args = parser.parse_args()

    # Generate
    if args.example == "spo2":
        bundle, capability = generate_spo2_example()
        bundle_filename = "fhir-bundle-spo2-ai-eval-pipeline.json"
    else:
        parser.error(f"Unknown example: {args.example}")

    # Validate bundle
    errors = validate_bundle(bundle)
    if errors:
        print("VALIDATION ERRORS:")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)

    # Validate capability statement
    cap_errors = validate_resource(capability)
    if cap_errors:
        print("CAPABILITY STATEMENT VALIDATION ERRORS:")
        for err in cap_errors:
            print(f"  - {err}")
        raise SystemExit(1)

    # Write output
    os.makedirs(args.output_dir, exist_ok=True)

    bundle_path = os.path.join(args.output_dir, bundle_filename)
    with open(bundle_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Wrote bundle:     {bundle_path}")

    cap_path = os.path.join(args.output_dir, "capability-statement.json")
    with open(cap_path, "w") as f:
        json.dump(capability, f, indent=2)
    print(f"Wrote capability: {cap_path}")

    # Summary
    print_summary(bundle)
    print("Validation passed: all required fields present.")


if __name__ == "__main__":
    main()
