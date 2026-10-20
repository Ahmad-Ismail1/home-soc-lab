# Detection Engineering — Elastic Security

## Overview

This document describes three detection scenarios implemented and validated in the Home SOC Lab.

## 1. Multiple Failed SMB Network Logons

- Detection rule: Multiple Failed Network Logons from Same Source IP
- Windows Event ID: 4625
- Logon type: 3 (Network)
- Threshold: At least 5 failed logons from the same source IP within 10 minutes
- Severity: Low
- Risk score: 21
- Test source: KALI-LAB (192.168.100.30)
- Target: WIN01 (192.168.100.20)
- Result: Detection successfully generated alerts during authorized SMB authentication testing.

## 2. Encoded PowerShell Command Execution

- Detection rule: Encoded PowerShell Command Execution
- Telemetry: Sysmon Event ID 1 (Process Creation)
- Suspicious behavior: PowerShell launched with an encoded-command argument
- Severity: Medium
- Risk score: 47
- MITRE ATT&CK: T1059.001 — PowerShell
- Result: One alert generated from a harmless encoded PowerShell test command.

## 3. Suspicious Scheduled Task Creation

- Detection rule: Suspicious Scheduled Task Creation
- Windows Event ID: 4698 (Scheduled Task Created)
- Detection behavior: Scheduled task creation with cmd.exe referenced in TaskContent
- Severity: Medium
- Risk score: 47
- MITRE ATT&CK: T1053.005 — Scheduled Task
- Result: One alert generated from an authorized scheduled task persistence simulation.

## Investigation Workflow

1. Generate controlled test activity.
2. Verify event ingestion in Kibana Discover.
3. Validate rule conditions and generated alerts.
4. Investigate supporting event fields and evidence.
5. Attach relevant alerts to Elastic Security cases.
6. Document conclusions and close the investigations.

## Notes

The documented detection scenarios were validated in an isolated laboratory. Rule effectiveness against real-world adversary activity has not been independently established.
