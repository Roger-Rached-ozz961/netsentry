# NetSentry

**Automated Network Discovery & Service Auditing with a Local Web Dashboard**

NetSentry is a Bash-led network reconnaissance and defensive inventory tool. It discovers live IPv4 hosts, scans TCP ports, identifies services and versions with Nmap, and organizes the results into timestamped reports that can be explored through a local Python web dashboard.

> **Authorized use only:** Scan only networks and systems you own or have explicit permission to assess. Network scanning can affect fragile systems and may violate organizational policy or law when performed without authorization.

## Contents

- [Overview](#overview)
- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Scan profiles](#scan-profiles)
- [Reports](#reports)
- [Dashboard](#dashboard)
- [Tools and references](#tools-and-references)
- [Security notes and limitations](#security-notes-and-limitations)
- [Tests](#tests)
- [License](#license)

## Overview

NetSentry combines a command-line scanning workflow with a browser-based interface:

1. Provide an IPv4 address, CIDR subnet, or IPv4 range.
2. Discover responsive hosts with Nmap.
3. Enumerate TCP ports and service/version information on discovered hosts.
4. Save scan output in a timestamped report directory.
5. Review discovered assets, scan history, and heuristic exposure indicators in the local dashboard.

The dashboard is intended for local review. Scan data is not uploaded to a cloud service, and the project does not use cloud AI.

## Features

- **Flexible targets:** IPv4 hosts, CIDR subnets, and IPv4 address ranges.
- **Host discovery:** Nmap `-sn` discovery stage.
- **Service enumeration:** Nmap `-sV` TCP service and version detection.
- **Configurable scan depth:** Quick, Standard, and Comprehensive TCP profiles.
- **Structured reports:** Timestamped Nmap XML, normal, and grepable output.
- **Local dashboard:** Summary metrics, report history, searchable asset inventory, severity filters, findings, and references.
- **Explainable indicators:** Rule-based exposure indicators include supporting evidence and defensive recommendations.
- **Dependency assistance:** Dependency checker and installer for supported package managers.
- **Local-only web service:** Python standard-library server intended to bind to loopback.

## How it works

```text
Target input
    |
    v
IPv4 target validation
    |
    v
Nmap host discovery (-sn)
    |
    v
Live-host service/version scan (-sV)
    |
    v
Timestamped report files (XML / normal / grepable)
    |
    v
Local Python dashboard
    |
    v
Asset inventory, scan history and heuristic indicators
```

## Requirements

- Linux (Kali Linux, Debian, Ubuntu, Fedora, Arch, or openSUSE recommended)
- Bash 4 or later
- Nmap
- Python 3.10 or later

Optional utilities:

- `arp-scan` — Layer-2 discovery on a local Ethernet network
- `jq` — JSON inspection
- `curl` — HTTP/API checks
- `netcat` — network connectivity checks
- `dig` — DNS lookups

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Roger-Rached-ozz961/netsentry.git
cd netsentry
```

Make the scripts executable, run the dependency installer, and launch NetSentry:

```bash
chmod +x netsentry.sh install-tools.sh
./install-tools.sh
./netsentry.sh
```

The installer supports `apt`, `dnf`, `pacman`, `zypper`, and Homebrew when available. Review package-manager prompts before approving installation.

## Usage

Start the application:

```bash
./netsentry.sh
```

Use the interactive menu:

- **Option 1:** Configure and run a network scan.
- **Option 2:** Start the local web dashboard.

The dashboard is available at:

```text
http://127.0.0.1:8765
```

Choose a target range you are authorized to scan. Start with the Quick profile when you need an initial view, then use a deeper profile where appropriate.

## Scan profiles

| Profile | TCP ports | Intended use |
|---|---:|---|
| Quick | Top 100 | Initial overview |
| Standard | Top 1,000 | Routine asset inventory |
| Comprehensive | All 65,535 | Thorough TCP port review |

A comprehensive scan can take substantially longer and may generate more network traffic. Select the profile appropriate to the environment and your authorization.

## Reports

Each scan creates a timestamped directory under `reports/`, following this naming pattern:

```text
reports/YYYYMMDDTHHMMSSZ_target/
```

The directory contains discovery and service-scan output in Nmap XML, normal, and grepable formats (for example, `discovery.*` and `services.*`).

**Keep the `services.xml` file.** The dashboard uses this XML report to parse and display scan results.

Treat reports as potentially sensitive infrastructure information. Store and share them only with people authorized to access the scanned environment.

## Dashboard

The local dashboard provides:

- Scan summary metrics and report history
- Searchable discovered-asset inventory
- Severity filtering
- Findings with evidence and defensive recommendations
- Reference links for further investigation

### Local API

| Endpoint | Description |
|---|---|
| `GET /api/reports` | Returns parsed reports |
| `GET /api/report/<report-id>` | Returns a selected report |

The server is designed to refuse non-loopback binding. Keep the dashboard local and do not expose it to an untrusted network.

## Tools and references

| Tool | Requirement | Purpose | Documentation |
|---|---|---|---|
| Nmap | Required | Host discovery, TCP scanning, service/version detection | [Nmap Reference Guide](https://nmap.org/book/man.html) |
| Python 3 | Required | Local dashboard and XML parsing | [Python Documentation](https://docs.python.org/3/) |
| arp-scan | Optional | Local Layer-2 host discovery | [arp-scan](https://github.com/royhills/arp-scan) |
| jq | Optional | JSON inspection | [jq](https://jqlang.github.io/jq/) |
| curl | Optional | HTTP/API checks | [curl](https://curl.se/docs/) |

Additional security references surfaced by the dashboard include:

- [MITRE ATT&CK: Network Service Discovery (T1046)](https://attack.mitre.org/techniques/T1046/)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [National Vulnerability Database](https://nvd.nist.gov/)

## Security notes and limitations

NetSentry's findings are **heuristic exposure indicators, not confirmed vulnerabilities**. An open RDP or database port alone does not establish that a host is vulnerable. Validate the exact product, version, configuration, and exposure with the relevant asset owner and trusted vendor/security advisories.

The current version does not provide:

- Exploitation or authenticated vulnerability checks
- Automated CVE matching
- UDP or IPv6 scanning
- Scheduled scanning or automatic remediation
- Machine-learning or neural-network analysis

The analysis is deterministic and explainable. No neural network is used in v1.0.0; unvalidated model output should not be presented as security evidence.

## Tests

Run the test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

## License

NetSentry is distributed under the MIT License. See [LICENSE](LICENSE) for details.
