# FHIR R4 Key Resources

## Resource Types for Medical Devices

### Patient
- Required: identifier, name
- Neonatal extension: `http://hl7.org/fhir/StructureDefinition/patient-birthTime`
- GA extension: use Observation with LOINC 76516-4 (Gestational age in weeks)

### Observation
- Required: status, code, subject
- SpO2: code = LOINC 59408-5, unit = %, category = vital-signs
- referenceRange: low/high for GA-adjusted thresholds
- interpretation: use `http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation`

### Device
- Required: identifier, type
- Pulse oximeter: type = SNOMED 706767009
- manufacturer, modelNumber, serialNumber

### DeviceMetric
- Links to Device via `source` reference
- calibration: type (offset/gain/two-point), state (calibrated/not-calibrated), time

### DiagnosticReport
- Required: status, code, subject
- Links Observations via `result` references
- conclusion: free-text summary
- conclusionCode: coded triage result

### Bundle
- Types: collection (read-only grouping), transaction (atomic write)
- Entry structure: resource + request (for transaction) or fullUrl (for collection)
- Transaction: each entry has request.method (POST/PUT) and request.url

### CapabilityStatement
- Declares what a FHIR server supports
- rest[].resource[]: type, interaction[], searchParam[]
- Required for conformance testing

## Common Search Parameters

| Resource | Parameter | Type | Description |
|----------|-----------|------|-------------|
| Patient | identifier | token | MRN lookup |
| Observation | code | token | LOINC code |
| Observation | date | date | Observation date |
| Observation | patient | reference | Patient reference |
| Device | identifier | token | Device serial/ID |
