# Incident 2 — Encoded PowerShell Execution

## Incident Summary

This incident documents a controlled PowerShell execution simulation performed on WIN01 within my isolated Home SOC Lab.

The objective was to execute a harmless Base64-encoded PowerShell command, collect the resulting process execution telemetry, detect the activity using Elastic Security, and investigate the generated alert.

**Incident status:** Closed  
**Classification:** Benign Positive — Authorized Security Testing  
**Alert severity:** Medium  
**Risk score:** 47  
**Alerts attached to case:** 1  
**MITRE ATT&CK:** T1059.001 — PowerShell

## Affected Systems

| System | Role | Lab IP |
|---|---|---|
| WIN01 | Windows endpoint | 192.168.100.20 |
| SOC-ELK | Elasticsearch and Kibana | 192.168.100.10 |

## Attack Simulation

A harmless PowerShell command was encoded using Base64 and executed through PowerShell's encoded-command functionality.

The command's intended behavior was to print the following test string:

`SOC-PHASE24-INCIDENT2`

No malicious payload or persistence mechanism was involved.

## Detection and Telemetry

The simulation generated process execution telemetry recorded through Sysmon Event ID **1 (Process Creation)**.

An Elastic Security detection rule named **Encoded PowerShell Command Execution** identified the suspicious command-line
