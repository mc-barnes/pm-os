# Common Value Sets

## LOINC Codes (Vitals)

| Code | Display | Unit (UCUM) |
|------|---------|-------------|
| 59408-5 | SpO2 (pulse oximetry) | % |
| 8867-4 | Heart rate | /min |
| 9279-1 | Respiratory rate | /min |
| 8310-5 | Body temperature | Cel |
| 8480-6 | Systolic blood pressure | mm[Hg] |
| 29463-7 | Body weight | kg |
| 76516-4 | Gestational age in weeks | wk |
| 3151-8 | Inhaled oxygen flow rate | L/min |

## SNOMED Codes

| Code | Display | Context |
|------|---------|---------|
| 706767009 | Pulse oximeter | Device type |
| 27113001 | Body weight | Observation category |
| 363787002 | Observable entity | General |
| 276885007 | Core body temperature | Observation |

## Observation Interpretation Codes

System: `http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation`

| Code | Display | Use |
|------|---------|-----|
| N | Normal | Within reference range |
| H | High | Above high normal |
| L | Low | Below low normal |
| HH | Critical high | Panic high |
| LL | Critical low | Panic low |
| A | Abnormal | Outside normal range |
| AA | Critical abnormal | Life-threatening |

## Diagnostic Report Codes

| Code | System | Display |
|------|--------|---------|
| urgent | local | Urgent triage |
| routine | local | Routine triage |
| emergency | local | Emergency triage |
