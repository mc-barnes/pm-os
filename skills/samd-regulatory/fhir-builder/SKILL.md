---
name: fhir-builder
description: >
  Generate valid FHIR R4 JSON resources, bundles, and capability statements.
  Use when building FHIR resources (Patient, Observation, Device, DiagnosticReport),
  creating FHIR bundles (collection/transaction), mapping HL7v2 to FHIR,
  building capability statements, or working with US Core profiles.
  Triggers: "FHIR resource", "FHIR profile", "capability statement",
  "FHIR bundle", "HL7v2 to FHIR mapping", "FHIR observation", "FHIR patient".
---

# FHIR R4 Resource Builder

## When to Use

- Building FHIR R4 JSON resources (Patient, Observation, Device, DiagnosticReport, etc.)
- Creating FHIR Bundles (collection for read-only grouping, transaction for atomic writes)
- Mapping HL7v2 segments to FHIR resources
- Building CapabilityStatements for conformance testing
- Working with US Core profiles (Pulse Oximetry, Vital Signs, Patient)

## When NOT to Use

- **HL7v2 pipe-delimited messages** -- use the `hl7v2-integration` skill instead
- **CDA XML documents** -- FHIR Builder generates JSON only
- **FHIR STU3 or earlier** -- this skill targets R4 (4.0.1) exclusively
- **SMART on FHIR auth flows** -- out of scope; handle auth separately

## Quick Start

```bash
python scripts/generate_fhir_bundle.py --example spo2
# Output: output/fhir-bundle-spo2-ai-eval-pipeline.json
#         output/capability-statement.json
```

## Resource Templates

### Patient (Neonatal with GA Extension)

```json
{
  "resourceType": "Patient",
  "id": "pat-neo-001",
  "identifier": [{"system": "urn:oid:1.2.36.146.595.217.0.1", "value": "PAT-SPO2-001"}],
  "name": [{"family": "Doe", "given": ["Baby"]}],
  "gender": "female",
  "birthDate": "2026-01-10",
  "extension": [
    {
      "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
      "valueDateTime": "2026-01-10T14:30:00Z"
    }
  ]
}
```

Gestational age is captured as a separate Observation (LOINC 76516-4), not a Patient extension.

**US Core requires** race and ethnicity extensions on Patient:
```json
"extension": [
  {
    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
    "extension": [
      {"url": "ombCategory", "valueCoding": {"system": "urn:oid:2.16.840.1.113883.6.238", "code": "2106-3", "display": "White"}},
      {"url": "text", "valueString": "White"}
    ]
  },
  {
    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
    "extension": [
      {"url": "ombCategory", "valueCoding": {"system": "urn:oid:2.16.840.1.113883.6.238", "code": "2186-5", "display": "Not Hispanic or Latino"}},
      {"url": "text", "valueString": "Not Hispanic or Latino"}
    ]
  }
]
```

### Observation -- SpO2 (LOINC 59408-5)

```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [
    {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs", "display": "Vital Signs"}]}
  ],
  "code": {
    "coding": [{"system": "http://loinc.org", "code": "59408-5", "display": "Oxygen saturation in Arterial blood by Pulse oximetry"}]
  },
  "subject": {"reference": "Patient/pat-neo-001"},
  "effectiveDateTime": "2026-01-15T08:30:00Z",
  "valueQuantity": {"value": 91.0, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%"},
  "interpretation": [
    {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": "LL", "display": "Critical low"}]}
  ],
  "referenceRange": [{"low": {"value": 85, "unit": "%"}, "high": {"value": 95, "unit": "%"}, "text": "GA-adjusted range for extremely preterm (24-28 wk)"}],
  "device": {"reference": "Device/dev-pulseox-001"}
}
```

### Device (Pulse Oximeter)

```json
{
  "resourceType": "Device",
  "id": "dev-pulseox-001",
  "identifier": [{"system": "urn:oid:1.2.840.10004.1.1.1.0.0.1.0.0.1.2680", "value": "DEV-MASIMO-001"}],
  "type": {"coding": [{"system": "http://snomed.info/sct", "code": "706767009", "display": "Pulse oximeter"}]},
  "manufacturer": "Masimo",
  "modelNumber": "Rad-97",
  "serialNumber": "SN-RAD97-20260115"
}
```

### DeviceMetric

```json
{
  "resourceType": "DeviceMetric",
  "id": "metric-spo2-001",
  "type": {"coding": [{"system": "urn:iso:std:iso:11073:10101", "code": "150456", "display": "SpO2"}]},
  "source": {"reference": "Device/dev-pulseox-001"},
  "category": "measurement",
  "calibration": [{"type": "two-point", "state": "calibrated", "time": "2026-01-15T06:00:00Z"}]
}
```

### DiagnosticReport

```json
{
  "resourceType": "DiagnosticReport",
  "status": "final",
  "code": {"coding": [{"system": "http://loinc.org", "code": "59408-5", "display": "Oxygen saturation in Arterial blood by Pulse oximetry"}]},
  "subject": {"reference": "Patient/pat-neo-001"},
  "effectiveDateTime": "2026-01-15T08:30:00Z",
  "result": [{"reference": "Observation/obs-spo2-001"}],
  "conclusion": "SpO2 91.0% -- classified as URGENT for 28-week GA infant.",
  "conclusionCode": [{"coding": [{"system": "urn:local:triage", "code": "urgent", "display": "Urgent triage"}]}]
}
```

### Bundle -- Collection

```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {"fullUrl": "urn:uuid:<uuid>", "resource": { "resourceType": "Patient", "..." : "..." }},
    {"fullUrl": "urn:uuid:<uuid>", "resource": { "resourceType": "Observation", "..." : "..." }}
  ]
}
```

### Bundle -- Transaction

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:<uuid>",
      "resource": { "resourceType": "Patient", "..." : "..." },
      "request": {"method": "POST", "url": "Patient"}
    }
  ]
}
```

### CapabilityStatement

```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "kind": "instance",
  "fhirVersion": "4.0.1",
  "format": ["json"],
  "rest": [{
    "mode": "server",
    "resource": [
      {"type": "Patient", "interaction": [{"code": "read"}, {"code": "search-type"}]},
      {"type": "Observation", "interaction": [{"code": "read"}, {"code": "search-type"}, {"code": "create"}]}
    ]
  }]
}
```

## US Core Profile Requirements

### Pulse Oximetry (us-core-pulse-oximetry)

Profile: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-pulse-oximetry`

**Must-support elements:**
| Element | Cardinality | Notes |
|---------|------------|-------|
| status | 1..1 | `final`, `amended`, or `corrected` |
| category | 1..* | Must include `vital-signs` |
| code | 1..1 | LOINC 59408-5 (required) |
| subject | 1..1 | Patient reference |
| effectiveDateTime | 1..1 | When measured |
| valueQuantity | 0..1 | value + unit(%) + system(UCUM) + code(%) |
| component (Flow O2) | 0..1 | LOINC 3151-8 if supplemental O2 administered |

### Vital Signs Profile

Required category: `vital-signs`. Must-support: status, category, code, subject, effective[x], value[x].

### Patient Profile

Must-support: identifier, name, gender, birthDate. Race/ethnicity extensions required for US Core.

## LOINC / SNOMED Codes

### Vitals (LOINC)
| Code | Display | UCUM Unit |
|------|---------|-----------|
| 59408-5 | SpO2 (pulse oximetry) | % |
| 8867-4 | Heart rate | /min |
| 9279-1 | Respiratory rate | /min |
| 8310-5 | Body temperature | Cel |
| 8480-6 | Systolic blood pressure | mm[Hg] |
| 29463-7 | Body weight | kg |
| 76516-4 | Gestational age in weeks | wk |
| 3151-8 | Inhaled oxygen flow rate | L/min |

### Devices (SNOMED)
| Code | Display |
|------|---------|
| 706767009 | Pulse oximeter |
| 27113001 | Body weight |

### Interpretation Codes
System: `http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation`

| Code | Display | Meaning |
|------|---------|---------|
| N | Normal | Within reference range |
| H | High | Above high normal |
| L | Low | Below low normal |
| HH | Critical high | Panic high |
| LL | Critical low | Panic low |
| A | Abnormal | Outside normal range |
| AA | Critical abnormal | Life-threatening |

## Bundle Patterns

### Collection Bundle
- Read-only grouping of resources. No server-side writes.
- Each entry has `fullUrl` (URN UUID) and `resource`.
- Use for: export, reporting, data exchange.

### Transaction Bundle
- Atomic write: all-or-nothing on a FHIR server.
- Each entry adds `request` with `method` (POST/PUT/DELETE) and `url`.
- Use for: batch create, conditional updates, FHIR server ingestion.

## HL7v2 to FHIR Mapping

| HL7v2 Segment | FHIR Resource | Key Fields |
|---------------|---------------|------------|
| PID | Patient | PID-3 -> identifier, PID-5 -> name, PID-8 -> gender |
| PV1 | Encounter | PV1-2 -> class, PV1-3 -> location, PV1-44 -> period.start |
| OBR | DiagnosticReport | OBR-4 -> code, OBR-7 -> effectiveDateTime |
| OBX | Observation | OBX-3 -> code, OBX-5 -> value, OBX-6 -> unit |
| DG1 | Condition | DG1-3 -> code, DG1-5 -> onsetDateTime |
| AL1 | AllergyIntolerance | AL1-3 -> code, AL1-4 -> type |
| MSH | MessageHeader | MSH-9 -> event, MSH-10 -> source |

### Mapping Rules
1. Map HL7v2 identifiers (e.g., PID-3) to FHIR `identifier[]` with appropriate `system`.
2. Convert HL7v2 timestamps (YYYYMMDDHHMMSS) to FHIR instant (ISO 8601).
3. Map HL7v2 coded elements (CE/CWE) to FHIR CodeableConcept with system + code + display.
4. Preserve original HL7v2 message ID in Provenance or MessageHeader for traceability.

## Verification Checklist

Before using generated FHIR resources:

- [ ] Every resource has `resourceType` set correctly
- [ ] All `id` fields are unique within the bundle
- [ ] `fullUrl` uses `urn:uuid:` format in bundles
- [ ] LOINC codes use system `http://loinc.org`
- [ ] SNOMED codes use system `http://snomed.info/sct`
- [ ] UCUM units use system `http://unitsofmeasure.org`
- [ ] Observations have `status`, `code`, and `subject` (required)
- [ ] Vital signs Observations include category `vital-signs`
- [ ] US Core pulse oximetry has `effectiveDateTime` and `valueQuantity`
- [ ] Transaction bundles have `request.method` and `request.url` on every entry
- [ ] Patient identifiers include `system` and `value`
- [ ] Device references in Observations match actual Device resource IDs
- [ ] DiagnosticReport `result[]` references point to valid Observations
- [ ] CapabilityStatement declares correct `fhirVersion: "4.0.1"`
