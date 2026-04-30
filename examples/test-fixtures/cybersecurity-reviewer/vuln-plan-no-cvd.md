---
type: rfc
status: draft
owner: "@agarcia"
related:
  - regulatory/submissions/510k-spo2-v1.md
  - engineering/rfcs/rfc-security-architecture-v1.md
---

# Expected findings:
# - SECURITY FINDING: No Coordinated Vulnerability Disclosure (CVD) procedures — statutory requirement under Section 524B(b)(1)
# - SECURITY FINDING: No remediation timelines defined — 30-day critical / 60-day high expected per FDA guidance
# - GAP: No ISAO participation — FDA Cyber Guidance §V.B recommends Information Sharing and Analysis Organization membership
# - GAP: Monitoring limited to NVD only — should include vendor advisories, CISA ICS-CERT, and threat intelligence feeds
# - Expected verdict: SECURITY CONCERN

# Vulnerability Management Plan: PulseView SpO2 Monitor

## 1. Purpose

This document describes the vulnerability management plan for the PulseView SpO2 monitoring system, addressing postmarket cybersecurity requirements.

## 2. Scope

This plan covers the identification, assessment, and remediation of cybersecurity vulnerabilities in the PulseView software and infrastructure components throughout the product lifecycle.

## 3. Vulnerability Monitoring

### 3.1 Monitoring Sources

The PulseView engineering team monitors the following source for new vulnerability disclosures:

- **National Vulnerability Database (NVD):** Weekly manual review of NVD entries matching PulseView SBOM components

### 3.2 Monitoring Process

Each Monday, a designated engineer searches the NVD website for CVEs published in the prior week that match components in the PulseView SBOM. Matching CVEs are logged in a shared spreadsheet with the following fields:
- CVE ID
- Affected Component
- CVSS Score
- Description
- Status (New / Under Review / Remediated / Accepted)

## 4. Vulnerability Assessment

When a new vulnerability is identified:

1. The engineering team reviews the CVE description and CVSS score
2. The team determines if the vulnerability is exploitable in the PulseView deployment configuration
3. If exploitable, the team estimates the effort to patch or mitigate
4. The vulnerability is prioritized based on CVSS score:
   - Critical (9.0-10.0): Address in next release
   - High (7.0-8.9): Address in next release
   - Medium (4.0-6.9): Address when convenient
   - Low (0.1-3.9): Accept risk, no action

## 5. Remediation

Vulnerabilities requiring remediation are addressed through the standard software release process:
- Component updated to patched version
- Regression testing performed
- Software release deployed per standard change control process

No expedited patch process exists for critical vulnerabilities. All patches follow the standard 6-8 week release cycle.

## 6. Vulnerability Reporting

### 6.1 Internal Reporting
A monthly vulnerability status report is provided to the Quality team summarizing:
- New vulnerabilities identified
- Vulnerabilities remediated
- Open vulnerabilities and estimated remediation timeline

### 6.2 External Reporting
No external vulnerability reporting or disclosure process is currently defined. If a security researcher reports a vulnerability, the report will be forwarded to the engineering team for review.

## 7. End-of-Life Planning

When PulseView reaches end-of-life, vulnerability monitoring will continue for 12 months following the last software update. Customers will be notified of end-of-support via email communication.
