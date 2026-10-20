# Home SOC Lab — Elastic Security SIEM & Incident Response

## Project Overview

This project documents the design, implementation, and operation of a virtual Security Operations Center (SOC) environment built using VMware Workstation, Elastic Security, Windows endpoints, Sysmon, Kali Linux, and Python.

The objective was to gain practical experience in security monitoring, detection engineering, threat investigation, incident response, and SOC workflow automation.

The lab includes centralized log collection, custom detection rules, controlled attack simulations, incident investigations, and Python-based alert triage.

## Network Architecture

![Home SOC Lab Architecture](architecture/home-soc-lab-architecture.png)

The environment uses an isolated VMware network (`192.168.100.0/24`) and a separate NAT network for software updates.

| Virtual Machine | Role | IP Address |
|---|---|---|
| SOC-ELK | Elasticsearch, Kibana, Fleet Server | 192.168.100.10 |
| WIN01 | Windows endpoint | 192.168.100.20 |
| WIN02 | Windows endpoint | 192.168.100.21 |
| KALI-LAB | Security testing machine | 192.168.100.30 |
| DC01 | Active Directory Domain Controller | 192.168.100.40 |

[View Architecture Documentation](architecture/lab-architecture.md)

## Technologies Used

- VMware Workstation
- Ubuntu Server
- Elasticsearch and Kibana
- Elastic Security
- Elastic Agent and Fleet
- Windows Security Event Logs
- Sysmon
- Windows Active Directory
- Kali Linux
- Python 3
- Git and GitHub

## Detection Engineering

Custom Elastic Security detection rules were developed and validated against controlled test activity.

| Detection | Event ID | Severity |
|---|---|---|
| Multiple Failed SMB Network Logons | 4625 | Low |
| Encoded PowerShell Execution | Sysmon 1 | Medium |
| Suspicious Scheduled Task Creation | 4698 | Medium |

[View Detection Engineering Documentation](detections/detection-rules.md)

## Incident Investigations

Three controlled security incidents were simulated, investigated, documented, and closed using Elastic Security Cases.

### Incident 1 — SMB Brute Force

Simulated repeated failed SMB authentication attempts from Kali Linux against WIN01.

- Windows Event ID: 4625
- Detection alerts: 2
- Outcome: Benign Positive — Authorized Security Test

[Read Incident 1 Investigation](incidents/incident-1-smb-brute-force.md)

### Incident 2 — Encoded PowerShell Execution

Executed a harmless Base64-encoded PowerShell command and investigated the resulting process creation alert.

- Sysmon Event ID: 1
- MITRE ATT&CK: T1059.001
- Detection alerts: 1
- Outcome: Benign Positive — Authorized Security Test

[Read Incident 2 Investigation](incidents/incident-2-encoded-powershell.md)

### Incident 3 — Suspicious Scheduled Task Creation

Simulated Windows scheduled-task persistence, detected the activity, investigated the alert, and removed the test task.

- Windows Event ID: 4698
- MITRE ATT&CK: T1053.005
- Detection alerts: 1
- Outcome: Benign Positive — Authorized Security Test

[Read Incident 3 Investigation](incidents/incident-03-scheduled-task.md)

## Python SOC Automation

Developed Python scripts to automate Elasticsearch connectivity and security alert triage.

### Features

- Authenticated Elasticsearch API connectivity with TLS verification
- Security alert retrieval
- Alert severity analysis
- Workflow status tracking
- Unresolved alert prioritization
- CSV report generation

### Python Files

- [Alert Triage Automation](automation/fetch_alerts.py)
- [Elasticsearch Connection Script](automation/connect_elasticsearch.py)
- [Python Dependencies](automation/requirements.txt)
- [Automation Documentation](automation/README.md)

## Skills Demonstrated

- SIEM deployment and administration
- Windows endpoint security monitoring
- Detection engineering and rule validation
- Log analysis and correlation
- MITRE ATT&CK mapping
- Security alert investigation
- Incident response and case management
- Python scripting and SOC automation
- Virtual networking and troubleshooting

## Security and Ethical Considerations

All attack simulations were performed within an authorized virtual laboratory environment.

The project uses private lab IP addresses. Passwords, API keys, private certificates, and other sensitive authentication material are not intentionally included in the published source files.

## Project Status

**Technical implementation:** Completed

**Detection validation:** Completed

**Incident investigations:** 3 completed and closed

**Python automation:** Implemented and tested

**GitHub documentation:** Final review in progress
