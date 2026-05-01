# SOUP Classification Reference

IEC 62304:2006+A1:2015 criteria for Software of Unknown Provenance (SOUP) identification and evaluation.

## SOUP Definition (IEC 62304 §3.29)

SOUP is software that is already developed and generally available, not developed for the purpose of being incorporated into the medical device. This includes open-source libraries, commercial off-the-shelf components, and language runtime libraries.

## Identification Requirements (§5.3.3)

For each SOUP item, document:
- **Title and manufacturer** — package name, publisher/maintainer
- **Version** — exact version in use (from lock file)
- **Unique identifier** — SOUP-001, SOUP-002, etc.

## Evaluation Requirements (§5.3.4 / §8.1.2)

| Evaluation Criterion | Auto-populated? | Notes |
|---------------------|----------------|-------|
| Fitness for intended use | No — GAP | Requires human assessment of suitability |
| Known anomalies reviewed | No — GAP | Requires review of CVE/issue tracker |
| Version controlled | Yes | Determined from lock file presence |
| Integration requirements | No — GAP | Requires documentation of integration constraints |

## Transitive Dependency Handling

IEC 62304 does not distinguish between directly imported and transitively included SOUP. A library pulled in by a dependency is still software of unknown provenance incorporated into the device. The SOUP register must include all transitive dependencies.

- **Lock file present:** Use resolved tree from lock file. Mark each dep as `declared` or `transitive`.
- **Lock file missing:** Flag as GAP. Dependency versions are not pinned. Resolved tree cannot be determined.

## License Flag Tiers

| Tier | Licenses | Action Required |
|------|----------|----------------|
| OK | MIT, BSD-2, BSD-3, Apache-2.0, ISC, Unlicense, CC0 | No license concern |
| WARNING | GPL (any), AGPL, SSPL, Unknown/missing | Legal review required — copyleft or undetermined terms |

WARNING does not mean the license is incompatible. It means the license requires legal review to determine compatibility with proprietary SaMD distribution.

## Monitoring (§6.1)

SOUP must be monitored on a defined cycle — at minimum every 6 months. Monitor for:
- Security vulnerabilities (CVE databases, vendor advisories)
- New versions that address known anomalies
- End-of-life or end-of-support announcements
