---
type: soup-register
status: draft
owner: "@tcheng"
related:
  - engineering/sdlc/soup-register-v1.md
  - regulatory/submissions/510k-spo2-v1.md
---

# Expected findings:
# - SECURITY FINDING: No component versions specified — versions required for vulnerability tracking (Section 524B(b)(3), FDA Cyber Guidance §V.A.4(b))
# - SECURITY FINDING: No transitive dependencies listed — Log4j/Log4Shell demonstrated criticality of transitive dependency tracking
# - GAP: Not machine-readable — SPDX or CycloneDX format expected for automated vulnerability monitoring
# - GAP: No vulnerability monitoring process described — how are new CVEs matched to SBOM components?
# - Expected verdict: SECURITY CONCERN

# Software Bill of Materials: PulseView SpO2 Monitor

## 1. Purpose

This Software Bill of Materials (SBOM) lists all software components included in the PulseView SpO2 monitoring system, as required by Section 524B of the FD&C Act for cyber devices.

## 2. SBOM Format

This SBOM is provided in human-readable markdown format for inclusion in the premarket submission package.

## 3. Component List

### 3.1 Application Components

| Component | Description | License |
|-----------|------------|---------|
| React | Frontend UI framework | MIT |
| Node.js | Backend runtime | MIT |
| Express | Web application framework | MIT |
| Chart.js | Data visualization library | MIT |
| Socket.io | Real-time communication | MIT |
| Axios | HTTP client | MIT |
| hl7-parser | HL7v2 message parsing | MIT |
| moment | Date/time utilities | MIT |
| lodash | Utility library | MIT |
| winston | Logging framework | MIT |

### 3.2 Database Components

| Component | Description | License |
|-----------|------------|---------|
| PostgreSQL | Relational database | PostgreSQL |
| Redis | In-memory cache/queue | BSD |
| pg (node-postgres) | PostgreSQL client for Node.js | MIT |
| ioredis | Redis client for Node.js | MIT |

### 3.3 Infrastructure Components

| Component | Description | License |
|-----------|------------|---------|
| Ubuntu Linux | Server operating system | GPL |
| nginx | Reverse proxy/web server | BSD-2 |
| Docker | Container runtime | Apache 2.0 |
| Terraform | Infrastructure as code | BSL |

### 3.4 Security Components

| Component | Description | License |
|-----------|------------|---------|
| OpenSSL | TLS/cryptography library | Apache 2.0 |
| passport | Authentication middleware | MIT |
| helmet | HTTP security headers | MIT |
| bcrypt | Password hashing | MIT |

## 4. Open Source License Compliance

All open source components are used under permissive licenses (MIT, BSD, Apache 2.0, PostgreSQL). No copyleft (GPL) components are incorporated into proprietary PulseView code. Ubuntu Linux is used as the host operating system only and is not distributed with the product.

## 5. Component Origin

All components are sourced from public package registries (npm, apt) or official project repositories. No components are forked or modified from their upstream sources.
