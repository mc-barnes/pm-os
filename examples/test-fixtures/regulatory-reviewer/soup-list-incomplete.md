---
type: soup-register
status: draft
owner: "@tcheng"
related:
  - engineering/sdlc/software-development-plan-v1.md
---

# Expected findings:
# - BLOCKER: Missing risk classification on React and PostgreSQL (IEC 62304 Sections 5.3.3–5.3.4, 7.1.2)
# - BLOCKER: Missing version number on hl7-parser (IEC 62304 Section 8.1.2)
# - WARNING: No verification dates on any entry (IEC 62304 Section 6.1 — minimum 6-month monitoring cycle)
# - WARNING: No monitoring cycle defined (how often SOUP is reviewed for updates/vulnerabilities)
# - WARNING: No anomaly lists referenced for Class B/C components (IEC 62304 Section 7.1.3)
# - Expected verdict: NEEDS REVISION

# SOUP Register: PulseView SpO2 Monitor

## Purpose

This document lists all Software of Unknown Provenance (SOUP) components used in the PulseView SpO2 monitoring system, as required by IEC 62304 Section 8.1.2.

## SOUP Components

### 1. React

| Field | Value |
|-------|-------|
| Package name | react |
| Version | 18.2.0 |
| Language | JavaScript |
| Website | https://react.dev |
| Software system | PulseView Dashboard (Frontend) |
| Purpose | UI component framework for the central monitoring dashboard |
| Functional requirements | Render real-time SpO2 values, waveform traces, and alarm indicators with ≤100ms UI update latency |
| Performance requirements | Support rendering of 24 simultaneous patient tiles without frame drops below 30 FPS |
| Risk classification | — |
| Known anomalies | — |
| Verification reasoning | Widely adopted, maintained by Meta, extensive test suite, large community support |

### 2. PostgreSQL

| Field | Value |
|-------|-------|
| Package name | postgresql |
| Version | 16.1 |
| Language | C |
| Website | https://www.postgresql.org |
| Software system | PulseView Data Store |
| Purpose | Persistent storage for patient trend data, alarm logs, and system configuration |
| Functional requirements | Store and retrieve 90 days of SpO2 trend data per patient with sub-second query response |
| Performance requirements | Handle concurrent writes from up to 24 sensor streams with ≤50ms write latency |
| Risk classification | — |
| Known anomalies | — |
| Verification reasoning | Enterprise-grade RDBMS with ACID compliance, extensive security track record, active development |

### 3. hl7-parser

| Field | Value |
|-------|-------|
| Package name | hl7-parser |
| Version | — |
| Language | Python |
| Website | https://github.com/example/hl7-parser |
| Software system | PulseView Sensor Integration |
| Purpose | Parse HL7v2 ADT and ORU messages from bedside pulse oximetry sensors |
| Functional requirements | Parse HL7v2 ORU messages containing SpO2 observation segments and extract numeric values with units |
| Performance requirements | Parse rate of ≥100 messages/second with ≤5ms per message |
| Risk classification | Class B — processes clinical data but does not directly control alarm logic |
| Known anomalies | — |
| Verification reasoning | Used in production by several health IT systems, adequate test coverage for HL7v2 parsing |

### 4. Chart.js

| Field | Value |
|-------|-------|
| Package name | chart.js |
| Version | 4.4.1 |
| Language | JavaScript |
| Website | https://www.chartjs.org |
| Software system | PulseView Dashboard (Frontend) |
| Purpose | Render SpO2 waveform traces and trend charts on the monitoring dashboard |
| Functional requirements | Render real-time line charts with streaming data updates at 1 Hz refresh rate |
| Performance requirements | Render 24 simultaneous chart instances without degrading dashboard FPS below 30 |
| Risk classification | Class A — display-only component, does not process or transform clinical values |
| Known anomalies | — |
| Verification reasoning | Popular charting library with active maintenance, MIT licensed, large plugin ecosystem |
