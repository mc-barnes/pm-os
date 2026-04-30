---
type: complaint
status: draft
owner: "@agarcia"
related:
  - quality/complaints/complaint-log-v1.xlsx
  - quality/capa/capa-log-v1.xlsx
---

# Expected findings:
# - FINDING: No MDR reportability evaluation documented (21 CFR 803, 21 CFR 820.198)
# - FINDING: "No further action" closure without documented rationale for closing without CAPA
# - OBSERVATION: "Unable to reproduce" without documented reproduction methodology or environment
# - OBSERVATION: No complaint trending — isolated evaluation without pattern analysis
# - Expected verdict: NOT AUDIT-READY

# Customer Complaint Record: C-2026-055

## 1. Complaint Information

| Field | Value |
|-------|-------|
| Complaint Number | C-2026-055 |
| Date Received | 2026-03-10 |
| Source | Hospital Biomedical Engineering |
| Product | PulseView SpO2 Monitor v2.1 |
| Lot/Version | Software v2.1.3 |
| Reporter | John Martinez, BME Director, Regional Medical Center |

## 2. Complaint Description

The hospital's biomedical engineering department reported that the PulseView central monitoring dashboard displayed SpO2 values of 0% for two patients simultaneously for approximately 45 seconds before recovering to normal values. The event occurred during the overnight shift (approximately 02:30 AM) on 2026-03-08.

The reporting engineer stated that the bedside nurse noticed the 0% readings and immediately performed a manual assessment — both patients had normal perfusion and the bedside pulse oximeters displayed normal SpO2 values (94% and 97% respectively). No alarms triggered on the central dashboard during the event.

The reporter described this as a "software glitch" and expressed concern about the alarm system's reliability.

## 3. Investigation

The software team reviewed server logs for the reported date and time. Log analysis showed a brief database connection timeout (47 seconds) that caused the dashboard to display default values (0%) for patients assigned to the affected database shard.

The team attempted to reproduce the issue in the staging environment by simulating database connection timeouts. **Unable to reproduce** — the staging environment uses a different database configuration and the timeout behavior could not be replicated.

## 4. Risk Assessment

The event involved display of incorrect SpO2 values (0%) on the central dashboard. The bedside monitors were unaffected and displayed correct values. No patient harm occurred.

## 5. Disposition

**No further action required.** The event appears to be an isolated database timeout that self-resolved. The staging environment was unable to reproduce the issue, suggesting it may be related to the specific hospital's network configuration.

## 6. Closure

Complaint closed on 2026-03-15 by Ana Garcia. No CAPA initiated.
