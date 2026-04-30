---
type: rfc
status: draft
owner: "@tcheng"
related:
  - engineering/rfcs/rfc-security-architecture-v1.md
  - regulatory/submissions/510k-spo2-v1.md
---

# Expected findings:
# - SECURITY FINDING: Missing Multi-Patient Harm Assessment — FDA Cyber Guidance §V.A.4(a) requires assessment of multi-patient impact
# - SECURITY FINDING: Missing Updateability/Patchability Analysis — must demonstrate device can be updated to address vulnerabilities
# - GAP: Missing Security Use Case View — how do legitimate users interact with security controls?
# - GAP: Global System View incomplete — no trust boundaries identified between zones
# - Expected verdict: SECURITY CONCERN

# Security Architecture: PulseView SpO2 Monitor

## 1. Purpose

This document describes the security architecture of the PulseView SpO2 monitoring system for inclusion in the premarket cybersecurity submission per FDA guidance.

## 2. Architecture Views

### 2.1 Global System View

The PulseView system consists of the following components:

```
[Bedside Sensors] → [Hospital Network] → [AWS Cloud] → [Dashboard Browser]
```

**Components:**
- **Bedside Sensors:** Pulse oximetry sensors connected via HL7v2 over TCP/IP
- **Hospital Network:** Standard hospital Ethernet/WiFi infrastructure
- **AWS Cloud:** EC2 instances running Node.js backend, RDS PostgreSQL database, ElastiCache Redis
- **Dashboard Browser:** Chrome/Edge web browser displaying monitoring interface

**Network Protocols:**
- Sensor to Cloud: HL7v2 over MLLP/TCP (hospital network) → HTTPS (to AWS)
- Cloud to Dashboard: HTTPS (WebSocket upgrade for real-time updates)
- Cloud Internal: PostgreSQL wire protocol (encrypted), Redis protocol (encrypted)

### 2.2 Data Flow Diagram

```
SpO2 Sensor → HL7v2 Interface Engine → Message Parser → Algorithm Engine → Database → Dashboard API → Browser
```

All data flows use encrypted transport (TLS 1.2 minimum). Patient data is encrypted at rest using AES-256 in the PostgreSQL database and Redis cache.

## 3. Authentication and Authorization

### 3.1 User Authentication
- Username/password authentication with bcrypt hashing
- Session-based authentication with 8-hour timeout
- Password complexity requirements: 12+ characters, mixed case, numbers, symbols
- Account lockout after 5 failed attempts (30-minute lockout)

### 3.2 Role-Based Access Control

| Role | Dashboard View | Patient Data | System Config | User Mgmt |
|------|---------------|-------------|--------------|-----------|
| Nurse | Read | Read | None | None |
| Charge Nurse | Read | Read | Alarm Config | None |
| Physician | Read | Read/Export | None | None |
| BME | Read | None | System Config | None |
| Admin | Read | Read/Export | Full | Full |

## 4. Encryption

- **In Transit:** TLS 1.2 minimum for all external connections. Internal AWS traffic uses VPC encryption.
- **At Rest:** AES-256 encryption for PostgreSQL (RDS encryption), Redis (ElastiCache encryption), and S3 backups.
- **Key Management:** AWS KMS managed keys with annual rotation.

## 5. Logging and Monitoring

- Application logs shipped to CloudWatch Logs (90-day retention)
- AWS CloudTrail enabled for API activity logging
- Failed authentication attempts logged and alerted (>10/hour triggers notification)
- No security information and event management (SIEM) system is currently deployed

## 6. Conclusion

The PulseView security architecture provides defense-in-depth through encryption, authentication, authorization, and logging. The architecture supports the secure operation of the monitoring system in hospital network environments.
