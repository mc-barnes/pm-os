# Cybersecurity in Medical Devices: Quality System Considerations and Content of Premarket Submissions

**Source:** FDA Center for Devices and Radiological Health (CDRH) / Center for Biologics Evaluation and Research (CBER)
**URL:** https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket
**Docket:** FDA-2021-D-1158
**Published:** June 27, 2025 (final guidance; supersedes September 27, 2023 version)
**Revised:** February 3, 2026 (Level 2 revision — QSR→QMSR terminology alignment only; no substantive cybersecurity changes)
**Retrieved:** 2026-04-30

---

This is a structured reference summary. The full guidance document is available at the URL above. Section numbers match the June 2025 final guidance.

## Document Structure

### I. Introduction

Establishes scope: applies to premarket submissions for devices containing software (including firmware) or programmable logic with network/internet connectivity. Covers Quality Management System considerations and premarket submission content for cybersecurity.

### II. Background

Describes the evolving cybersecurity threat landscape for medical devices and the statutory basis for cybersecurity requirements, including Section 524B of the FD&C Act (added by the Consolidated Appropriations Act, 2023).

### III. Scope

Applies to all premarket submissions (510(k), PMA, PDP, De Novo, HDE) for devices that contain software and have network connectivity. Applies regardless of whether the device meets the "cyber device" definition under Section 524B — cybersecurity is a design consideration for all software-containing devices.

### IV. General Principles

#### IV.A. Secure Product Development Framework (SPDF)

Manufacturers should establish and maintain a Secure Product Development Framework encompassing the total product lifecycle (TPLC):
- Security risk management integrated with safety risk management (ISO 14971)
- Secure design and development practices
- Security verification and validation
- Cybersecurity management of fielded devices (monitoring, response, patching)

The SPDF should be documented and evidence of implementation provided in premarket submissions.

### V. Design Considerations and Content of Premarket Submissions

#### V.A. Security Architecture and Design

##### V.A.1. Security Risk Management
- Must integrate cybersecurity risk with safety risk management per ISO 14971
- Exploitability and severity assessed separately
- Residual cybersecurity risk must be documented as controlled or uncontrolled

##### V.A.2. Threat Modeling
- Systematic analysis using recognized methodology (STRIDE, PASTA, attack trees, LINDDUN)
- Must identify: threat sources, attack vectors, attack surfaces, potential impacts
- Cybersecurity threats must trace to patient safety outcomes (per AAMI TIR57)
- Must be updated when architecture changes or new threat intelligence emerges

##### V.A.3. Cybersecurity Risk Assessment
- Exploitability assessment (CVSS or equivalent): remote exploitability, attack complexity, privileges required, user interaction, exploit maturity
- Severity assessment connected to patient safety outcomes per ISO 14971
- Controlled vs. uncontrolled risk determination with supporting rationale
- Cumulative/chained vulnerability effects must be considered

##### V.A.4. Software Bill of Materials and Security Architecture

###### V.A.4(a). Security Architecture Views
Four required architecture views (see Appendix 2):
1. **Global System View** — all components, trust boundaries, data flows, network interfaces, external connections
2. **Multi-Patient Harm Assessment** — whether single exploit could affect multiple patients
3. **Updateability/Patchability Analysis** — mechanism for authenticated, validated security updates with rollback capability
4. **Security Use Case View** — how users interact with security features (auth, session management, encryption config)

###### V.A.4(b). Software Bill of Materials (SBOM)
- Must include: component name, version, manufacturer/supplier, dependency relationships, known vulnerabilities at submission
- Machine-readable format preferred (SPDX or CycloneDX), aligned with NTIA minimum elements
- Must include transitive dependencies
- Must be maintained throughout TPLC with continuous vulnerability monitoring

#### V.B. Cybersecurity Testing
- Required testing commensurate with device risk: static analysis, dynamic analysis, fuzz testing, penetration testing, vulnerability scanning
- Penetration testing must be independent of development team
- Fuzz testing must cover all external interfaces
- Test scope must match threat model attack surface
- Negative/adversarial test cases required

### VI. Cybersecurity Transparency and Labeling
- Device labeling must include: cybersecurity features/capabilities, recommended security configurations, known residual risks, supported operating environments, SBOM or pointer to SBOM, end-of-support date, vulnerability reporting contact
- Compensating controls for residual risks must be communicated to users
- End-of-support/end-of-life must be clearly communicated

### VII. Cyber Devices (Section 524B) — New in June 2025

Implements statutory requirements from Section 524B of the FD&C Act for "cyber devices" (devices with software, internet connectivity, and cybersecurity-vulnerable characteristics). Applies to submissions filed on or after March 29, 2023.

#### VII.A. Plan to Monitor and Address Postmarket Vulnerabilities
- Postmarket vulnerability management plan with coordinated vulnerability disclosure (CVD) procedures
- Monitoring: NVD/CVE, CISA advisories, vendor advisories, ISAO alerts, researcher disclosures
- Remediation timelines: 30-day customer communication, 60-day fix for uncontrolled risk
- ISAO participation (e.g., Health-ISAC) recommended for enforcement discretion

#### VII.B. Design, Develop, and Maintain Cybersecurity Processes
- Processes providing reasonable assurance the device is cyber secure
- Including patches/updates to address vulnerabilities in a timely manner
- Evidence of SPDF implementation

#### VII.C. Software Bill of Materials
- Statutory requirement per Section 524B(b)(3)
- Must include commercial, open-source, and off-the-shelf software components
- Legal requirement — not a recommendation

#### VII.D. Modifications to Previously Authorized Cyber Devices
- Changes likely to impact cybersecurity require updated documentation
- Changes unlikely to impact cybersecurity require rationale justifying no impact

#### VII.E. Reasonable Assurance of Cybersecurity
- Overall demonstration that the device maintains safety and essential performance under cybersecurity threats

### Appendix 1 — Security Control Categories

Eight categories of security controls:
1. **Authentication** — appropriate for clinical context, balancing security with workflow
2. **Authorization** — role-based access, least privilege
3. **Cryptography** — current validated algorithms, cryptographic agility
4. **Code, Data, and Execution Integrity** — tamper detection, secure boot, code signing
5. **Confidentiality** — data protection at rest and in transit
6. **Event Detection and Logging** — security-relevant events, tamper-evident storage, forensic capability
7. **Resiliency and Recovery** — fail-safe defaults, continued safety during incidents, recovery procedures
8. **Firmware/Software Updates** — authenticated, validated, rollback-capable update mechanisms

### Appendix 2 — Security Architecture Views

Detailed requirements for the four architecture views described in Section V.A.4(a):
1. Global System View
2. Multi-Patient Harm Assessment
3. Updateability/Patchability Analysis
4. Security Use Case View

### Appendix 3 — [Threat Modeling Frameworks]

References to recognized threat modeling methodologies.

### Appendix 4 — Premarket Submission Documentation Table (New in June 2025)

Consolidated checklist of required cybersecurity documentation elements for premarket submissions.

### Appendix 5 — Definitions (New in June 2025)

Key definitions including "cyber device," "controlled risk," "uncontrolled risk," and related terms.

## Recognized Consensus Standards Referenced

- **AAMI TIR57:2016** — Principles for medical device security — Risk management (see `aami-tir57-reference-stub.md`)
- **IEC 81001-5-1:2021** — Health software and health IT systems safety, effectiveness, and security (see `iec-81001-5-1-reference-stub.md`)
- **ANSI/AAMI SW96:2023** — Standard for medical device security — Security risk management for device manufacturers
- **ISO 14971:2019** — Medical devices — Application of risk management to medical devices
- **NIST Cybersecurity Framework (CSF)**
- **NTIA SBOM Minimum Elements** — Minimum requirements for software bill of materials
