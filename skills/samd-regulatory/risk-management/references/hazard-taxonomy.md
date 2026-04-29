# Hazard Taxonomy for Medical Device Software

## Categories (per ISO 14971 Annex C)

### Energy Hazards
- Electrical (leakage current, defibrillation interference)
- Thermal (overheating sensors)
- Mechanical (device movement, pinching)

### Biological Hazards
- Infection (contaminated sensors)
- Biocompatibility (adhesive reactions)
- Allergenicity (latex, nickel)

### Information Hazards (most common for SaMD)
- Incorrect measurement display
- Incorrect algorithm output (misclassification)
- Missing alarm/alert
- False alarm (alarm fatigue -> missed real events)
- Delayed information delivery
- Incorrect patient association
- Loss of data

### Operational Hazards
- Use error (incorrect sensor placement)
- Training deficiency
- Labeling/IFU inadequacy
- Maintenance failure

### Software-Specific Hazards (IEC 62304 Annex B)
- Incorrect algorithm logic
- Race conditions in concurrent processing
- Memory corruption/overflow
- Network timeout/disconnection
- Invalid input handling
- Configuration drift

## SpO2 AI System Hazards (Example)
| ID | Hazard | Category |
|----|--------|----------|
| HAZ-001 | Misclassify urgent desaturation as normal | Information |
| HAZ-002 | False positive artifact flag on real desat | Information |
| HAZ-003 | Sensor disconnect undetected | Operational |
| HAZ-004 | Wrong GA threshold applied | Software |
| HAZ-005 | Handoff report omits critical context | Information |

**Note on HAZ-003 severity**: Sensor disconnect severity depends on duration and clinical context.
In NICU with continuous monitoring and 1:2 nurse ratio, brief disconnect (<1 min) is S3 (staff likely notices).
In step-down unit with 1:4 ratio, prolonged disconnect could be S4 (unmonitored period with no backup).
Assign severity based on intended use environment; default to higher severity if environment varies.
