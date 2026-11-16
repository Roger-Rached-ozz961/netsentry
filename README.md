# NetSentry
**Automated Network Discovery & Service Audit with Local Web Dashboard**

A Bash-led defensive network inventory tool using Nmap for host discovery and TCP service/version detection, with timestamped XML reports and a local Python-powered dashboard.

> Only scan networks and systems you own or are explicitly authorized to assess. Scanning may disrupt fragile systems and may violate policy or law when unauthorized.

## Features
- IPv4 host, CIDR subnet and IPv4 range input.
- Two-stage discovery (`nmap -sn`) and service/version scan (`nmap -sV`).
- Quick (top 100), Standard (top 1,000) and Comprehensive (all TCP ports) profiles.
- Timestamped report folders with Nmap XML, normal and grepable output.
- Local dashboard: metrics, report history, searchable asset inventory, severity filters, findings and references.
- Rule-based exposure indicators with evidence and defensive recommendations.
- Dependency checker and installer for common package managers.
- Python standard-library server, loopback-only; no scan data uploaded and no cloud AI.

## Requirements
Linux (Kali/Debian/Ubuntu/Fedora/Arch/openSUSE recommended), Bash 4+, Nmap and Python 3.10+.
Optional tools: arp-scan (local Layer-2 discovery), jq, curl, netcat and dig.

## Install and run
```bash
chmod +x netsentry.sh install-tools.sh
./install-tools.sh
./netsentry.sh
```
Menu option 1 starts a scan; option 2 starts the dashboard at **http://127.0.0.1:8765**.

## Profiles
| Profile | Ports | Purpose |
|---|---:|---|
| Quick | Top 100 TCP | Initial overview |
| Standard | Top 1,000 TCP | Routine inventory |
| Comprehensive | All 65,535 TCP | Thorough TCP review |

## Reports
Each run creates `reports/YYYYMMDDTHHMMSSZ_target/` containing `discovery.*` and `services.*` Nmap outputs. Keep `services.xml`; the dashboard parses it.

## Tool guide
| Tool | Priority | Purpose | Reference |
|---|---|---|---|
| Nmap | Required | Discovery, TCP ports and service/version detection | https://nmap.org/book/man.html |
| Python 3 | Required | Local dashboard and XML parsing | https://docs.python.org/3/ |
| arp-scan | Optional | ARP discovery on local Ethernet networks | https://github.com/royhills/arp-scan |
| jq | Optional | JSON inspection | https://jqlang.github.io/jq/ |
| curl | Optional | HTTP/API checks | https://curl.se/docs/ |

Installer supports apt, dnf, pacman, zypper and Homebrew when present. Review package manager prompts before proceeding.

## Dashboard API
- `GET /api/reports` — all parsed reports.
- `GET /api/report/<report-id>` — one report.
Server refuses non-loopback binding. Public reference links open NVD, MITRE ATT&CK T1046, CISA KEV and Nmap documentation.

## Analysis and limitations
Findings are **heuristic exposure indicators**, not confirmed vulnerabilities. An open RDP/database port is not proof of a vulnerability. Validate exact product/build and configuration with asset owners and vendor advisories. No exploitation, authenticated checks, CVE matching, UDP, IPv6, scheduled scanning or automatic remediation are included. The current analysis is deterministic and explainable; no neural network is used in v1.0.0 because unvalidated model output should not be presented as security evidence.

## Tests
```bash
python3 -m unittest discover -s tests -v
```
MIT License; see [LICENSE](LICENSE).
