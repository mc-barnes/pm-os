# FDA 21 CFR 820.30 Design Controls

## Section Mapping

| 820.30 | Requirement | Common 483 Observations |
|--------|-------------|------------------------|
| (a) | Design controls apply to Class II/III | Claiming exemption without basis |
| (b) | Design and development planning | No documented plan, plan not updated |
| (c) | Design input | Incomplete, ambiguous, or conflicting requirements |
| (d) | Design output | Output doesn't reference acceptance criteria |
| (e) | Design review | No independent reviewer, missing attendee list |
| (f) | Design verification | No objective evidence, informal testing |
| (g) | Design validation | Not on production-equivalent units, no user testing |
| (h) | Design transfer | Manufacturing can't reproduce design intent; no documented transfer procedures; process parameters not validated on production equipment; traceability gaps between design specs and manufacturing specs; personnel training not documented |
| (i) | Design changes | Changes not evaluated for effect on other components |
| (j) | Design history file | Incomplete, missing records, not maintained |

### 820.30(h) Design Transfer — Expanded Requirements
FDA expects design transfer to include:
- Manufacturing procedures that reproduce design intent
- Process parameters validated on production equipment (not just development environment)
- Traceability from design specifications to manufacturing specifications
- Personnel training documented (operators, QA, service)
- For SaMD/software: deployment procedures, environment specifications, configuration management during transfer

## Top FDA 483 Observations (Design Controls)
1. Failure to establish and maintain procedures for design changes (820.30(i))
2. Failure to establish design input requirements (820.30(c))
3. Failure to establish and maintain adequate design review procedures (820.30(e))
4. Failure to adequately validate device design (820.30(g))
5. Failure to maintain a design history file (820.30(j))

## Software-Specific Expectations
- IEC 62304 compliance expected for software lifecycle
- Cybersecurity documentation (per FDA premarket guidance)
- AI/ML: predetermined change control plan for adaptive algorithms
- Real-world performance monitoring plan

### Software-Specific Documentation Requirements
- **Software Requirements Specification (SRS)**: Functional, performance, interface, safety requirements
- **Software Design Specification (SDS)**: Architecture, detailed design, data structures, algorithms
- **Test hierarchy**: Unit tests -> Integration tests -> System tests -> Acceptance tests (each with distinct protocols)
- **SOUP/OTS assessment**: Software of Unknown Provenance — identify, evaluate risk, document version and intended use per IEC 62304
- **SBOM**: Software Bill of Materials for supply chain transparency
- **Configuration management**: Version control, baseline identification, change control per IEC 62304 Clause 8
- **AI/ML specific**: Predetermined change control plan (PCCP), performance monitoring, retraining criteria, update validation strategy per FDA guidance
