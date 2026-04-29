# US Core Profiles (v6.1)

## Pulse Oximetry Profile

Profile URL: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-pulse-oximetry`

### Must-Support Elements

- status (required: final | amended | corrected)
- category: `vital-signs` (required)
- code: LOINC 59408-5 (required)
- subject: Patient reference (required)
- effectiveDateTime (required)
- valueQuantity: value + unit(%) + system(UCUM) + code(%) (required)
- component[0]: Flow O2 (LOINC 3151-8) if supplemental O2

### Example

```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "59408-5",
        "display": "Oxygen saturation in Arterial blood by Pulse oximetry"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "effectiveDateTime": "2026-01-15T08:30:00Z",
  "valueQuantity": {
    "value": 91.0,
    "unit": "%",
    "system": "http://unitsofmeasure.org",
    "code": "%"
  }
}
```

### With Supplemental Oxygen Component
When patient is on supplemental O2, add `component` array:
```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
  "code": {"coding": [{"system": "http://loinc.org", "code": "59408-5", "display": "Oxygen saturation in Arterial blood by Pulse oximetry"}]},
  "subject": {"reference": "Patient/example"},
  "effectiveDateTime": "2026-01-15T08:30:00Z",
  "valueQuantity": {"value": 95.0, "unit": "%", "system": "http://unitsofmeasure.org", "code": "%"},
  "component": [
    {
      "code": {"coding": [{"system": "http://loinc.org", "code": "3151-8", "display": "Inhaled oxygen flow rate"}]},
      "valueQuantity": {"value": 2.0, "unit": "L/min", "system": "http://unitsofmeasure.org", "code": "L/min"}
    }
  ]
}
```

## Vital Signs Profile

Required category: `vital-signs`
Must-support: status, category, code, subject, effective[x], value[x]

## Patient Profile

Must-support: identifier, name, gender, birthDate
Race/ethnicity extensions required for US Core
