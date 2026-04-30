---
type: risk-record
status: draft
owner: "@tcheng"
related:
  - regulatory/risk-management/risk-spo2-v1.xlsx
  - engineering/rfcs/rfc-security-architecture-v1.md
---

# Expected findings:
# - SECURITY FINDING: No threat modeling methodology used — STRIDE, PASTA, or attack tree required (FDA Cyber Guidance §V.A.2)
# - SECURITY FINDING: No patient safety tracing — threats not mapped to patient harm scenarios (AAMI TIR57:2016)
# - GAP: No attack surface analysis — network interfaces, data flows, and entry points not enumerated
# - GAP: No threat source identification — who are the adversaries and what are their capabilities?
# - Expected verdict: SECURITY CONCERN

# Threat Assessment: PulseView SpO2 Monitor

## 1. Purpose

This document identifies cybersecurity threats to the PulseView SpO2 monitoring system to support the premarket cybersecurity submission.

## 2. System Overview

PulseView is a cloud-connected SpO2 monitoring system deployed in hospital NICUs. The system receives data from bedside pulse oximeters, processes it in a cloud environment, and displays results on a web-based dashboard.

## 3. Threat List

### T-001: Unauthorized Access
An unauthorized user could gain access to the monitoring dashboard and view patient SpO2 data.
**Mitigation:** Username/password authentication is implemented.

### T-002: Data Breach
Patient SpO2 data could be exposed through a data breach.
**Mitigation:** Data is encrypted at rest using AES-256.

### T-003: Malware
Malware could infect the system and disrupt monitoring functions.
**Mitigation:** Servers run antivirus software with daily signature updates.

### T-004: Denial of Service
A denial of service attack could make the monitoring dashboard unavailable.
**Mitigation:** AWS provides DDoS protection (AWS Shield Standard).

### T-005: Man-in-the-Middle
An attacker could intercept data between the sensor and the cloud.
**Mitigation:** All communications use TLS 1.2 encryption.

### T-006: Insider Threat
A disgruntled employee could access or modify patient data.
**Mitigation:** Role-based access control limits data access to authorized personnel.

### T-007: Physical Access
An unauthorized person could physically access the server hardware.
**Mitigation:** Servers are hosted in AWS data centers with physical security controls.

### T-008: Social Engineering
An attacker could use social engineering to obtain credentials.
**Mitigation:** Security awareness training is provided to all staff annually.

## 4. Risk Summary

All identified threats have been mitigated through standard security controls. The overall cybersecurity risk of the PulseView system is Low.

## 5. Conclusion

This threat assessment identifies 8 cybersecurity threats and corresponding mitigations for the PulseView SpO2 monitoring system. All threats have been addressed with industry-standard security controls.
