---
type: prd
status: draft
owner: "@mlee"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - regulatory/submissions/510k-spo2-v1.md
---

# Expected findings:
# - Critical: Implied SIDS benefit without evidence — AAP recommends against home monitors for SIDS risk reduction (AAP 2022)
# - Critical: No ABG gold-standard validation, sensitivity unreported (FDA SpO2 guidance requires Arms accuracy study)
# - Important: Owlet Smart Sock at 88.8% sensitivity was deemed unacceptable by FDA — this device's sensitivity is unknown
# - Important: No acknowledgment of healthy infant desaturation norms (brief desats are physiologically normal in neonates)
# - Expected verdict: CLINICALLY UNSAFE

# Product Requirements Document: PulseView Home — Infant SpO2 Monitor

## 1. Overview

PulseView Home is a consumer-grade infant SpO2 monitoring system designed to provide parents and caregivers with continuous overnight oxygen saturation monitoring for infants aged 0-12 months. The system consists of a fabric foot wrap sensor, a Bluetooth-connected base station, and a smartphone application.

## 2. Problem Statement

Sudden Infant Death Syndrome (SIDS) remains the leading cause of post-neonatal infant mortality in the United States. Parents of newborns experience significant anxiety about their infant's breathing during sleep. Existing consumer monitors are limited to movement detection (e.g., Snuza) and do not provide direct physiological measurement.

PulseView Home addresses this gap by providing continuous SpO2 monitoring that can alert parents to potential oxygen desaturation events during sleep, offering peace of mind and an added layer of safety for their infant.

## 3. Target Users

- Parents of healthy infants (0-12 months)
- Parents of infants with known risk factors (premature birth, siblings with SIDS history)
- Pediatricians recommending home monitoring for at-risk infants

## 4. Key Features

### 4.1 Continuous Overnight Monitoring
The system monitors SpO2 continuously from bedtime to wake-up. Typical monitoring sessions last 8-12 hours. The foot wrap sensor is designed for comfortable extended wear.

### 4.2 Parent Alert System
When SpO2 drops below 80%, the system triggers:
1. Smartphone alarm (loud, overrides silent mode)
2. Base station red LED and audible alarm
3. Push notification with event details

### 4.3 Sleep Summary Report
Each morning, parents receive a summary showing:
- Total monitoring time
- Average SpO2 during monitoring
- Number of low SpO2 events (if any)
- Wear quality score

### 4.4 Pediatrician Sharing
Parents can share 7-day trend reports with their pediatrician via email export (PDF format). Reports include nightly average SpO2, event counts, and wear quality metrics.

## 5. Marketing Claims

PulseView Home provides:
- "Clinical-grade SpO2 monitoring in a consumer-friendly design"
- "Peace of mind for parents worried about their baby's breathing"
- "Know your baby is safe with continuous oxygen monitoring"
- "The smart monitor that watches over your baby while you sleep"

## 6. Sensor Specifications

- Reflectance pulse oximetry sensor embedded in fabric wrap
- Bluetooth Low Energy (BLE) 5.0 connectivity
- Battery life: 16 hours per charge
- Sensor placement: dorsal aspect of foot (metatarsal region)

## 7. Algorithm

The system applies a simple threshold at SpO2 < 80% with a 10-second persistence window before alarming. No averaging, trending, or artifact rejection is applied beyond the persistence window.

SpO2 values are calculated using the standard R/IR ratio method with factory-calibrated lookup table. No per-patient calibration is performed.

## 8. Clinical Evidence

Algorithm accuracy was assessed through internal bench testing using a finger simulator device (Fluke Index 2) across the SpO2 range of 70-100%. Bench testing demonstrated ±3% accuracy compared to the simulator reference values.

No human subject testing has been performed. An IRB application for a validation study is planned for Q3 2026.

## 9. Regulatory Pathway

PulseView Home will be submitted via 510(k) with the Owlet Smart Sock 3 (K212666) cited as the primary predicate device.

## 10. Safety Considerations

The system includes the following safety features:
- Sensor disconnect detection (alerts parent if wrap is removed)
- Low battery warning (4 hours before depletion)
- Automatic firmware updates for algorithm improvements

No risk analysis has been performed for false negative scenarios (missed desaturation events). The system is positioned as a supplementary monitoring tool and includes a disclaimer that it does not replace medical care.
