# SOC Incident Investigations

This directory contains three security incident investigations conducted in the Home SOC Lab using Elastic Security.

## Incident 1 — SMB Brute Force
- Source: Kali Linux
- Target: WIN01
- Windows Event ID: 4625
- Result: Detected and investigated; case closed

## Incident 2 — Encoded PowerShell
- Target: WIN01
- Sysmon Event ID: 1
- MITRE ATT&CK: T1059.001
- Result: Detected and investigated; case closed

## Incident 3 — Scheduled Task Persistence
- Target: WIN01
- Windows Event ID: 4698
- MITRE ATT&CK: T1053.005
- Result: Detected and investigated; case closed

## Investigation Workflow

1. Generate authorized test activity.
2. Collect and analyze security events.
3. Validate Elastic Security detection alerts.
4. Create a Kibana security case.
5. Document evidence and findings.
6. Close the case and classify the alerts.

All incidents were simulated in an isolated laboratory environment.
