---
type: audit
status: draft
owner: "@tcheng"
related:
  - engineering/sdlc/soup-register-v1.md
  - quality/audits/supplier-log-v1.xlsx
---

# Expected findings:
# - FINDING: SOUP/cloud providers not evaluated as suppliers (ISO 13485:2016 §7.4.1)
# - FINDING: No monitoring metrics or re-evaluation schedule defined for any supplier
# - OBSERVATION: No supplier risk classification (critical vs. non-critical)
# - OBSERVATION: No documented acceptance criteria for software suppliers (21 CFR 820.50)
# - Expected verdict: NEEDS REMEDIATION

# Approved Supplier List: PulseView SpO2 Monitor

## 1. Purpose

This document maintains the list of approved suppliers for the PulseView SpO2 monitoring system, including hardware component suppliers, contract services, and manufacturing partners.

## 2. Supplier Evaluation Criteria

Suppliers are evaluated based on:
- Ability to meet purchase order specifications
- Delivery performance
- Pricing competitiveness
- References from other medical device companies (preferred)

## 3. Approved Supplier List

### 3.1 Hardware Suppliers

| Supplier | Component | Status | Last Evaluated |
|----------|-----------|--------|----------------|
| SensorTech Inc. | SpO2 sensor modules | Approved | 2025-06-15 |
| DisplayCorp | Monitoring displays (27") | Approved | 2025-08-20 |
| NetConnect Systems | Network switches | Approved | 2025-07-10 |

### 3.2 Contract Services

| Supplier | Service | Status | Last Evaluated |
|----------|---------|--------|----------------|
| MedTest Labs | EMC/EMI testing (IEC 60601-1-2) | Approved | 2025-09-01 |
| ClinTrial Partners | Clinical validation study | Approved | 2025-11-15 |

### 3.3 Software and Cloud Services

The following software components and cloud services are used in the PulseView system. These are acquired through standard commercial licenses and terms of service.

| Component/Service | Usage | License |
|------------------|-------|---------|
| Amazon Web Services (AWS) | Cloud hosting, database (RDS), compute (EC2) | Enterprise agreement |
| React v18.2 | Frontend dashboard framework | MIT open source |
| PostgreSQL v15 | Patient data storage | PostgreSQL license |
| Node.js v20 LTS | Backend runtime | MIT open source |
| hl7-parser v2.1 | HL7v2 message parsing | MIT open source |
| Chart.js v4.4 | SpO2 waveform visualization | MIT open source |
| Redis v7.2 | Alarm queue and caching | BSD license |
| Grafana Cloud | System monitoring and alerting | Commercial SaaS |

These software components and cloud services have not been formally evaluated as suppliers. They are tracked in the SOUP register (see related documents) for IEC 62304 compliance.

## 4. Evaluation Records

Supplier evaluation records are maintained in the supplier quality file. Each hardware supplier and contract service provider has a completed Supplier Evaluation Form on file.

No evaluation forms exist for software/cloud service providers listed in Section 3.3.

## 5. Re-Evaluation Schedule

Hardware suppliers and contract services are re-evaluated annually or upon significant quality event. The next scheduled re-evaluation cycle begins 2026-06-01.

No re-evaluation schedule has been established for software/cloud providers.
