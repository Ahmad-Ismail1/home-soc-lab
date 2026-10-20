# Incident 01 — SMB Brute Force

## Incident Summary

A controlled SMB authentication attack was simulated from Kali Linux against a Windows endpoint to validate Elastic Security's ability to detect repeated failed network logons.

## Environment

- Source: KALI-LAB (192.168.100.30)
- Target: WIN01 (192.168.100.20)
- Test account: SOC-Test
- SIEM: Elastic Security
- Windows Event ID: 4625
- Logon Type: 3 (Network)

## Detection

- Rule: Multiple Failed Network Logons from Same Source IP
- Threshold: 5 or more failed network logons from one source IP within 10 minutes
- Severity: Low
- Risk Score: 21

## Investigation

1. Generated six unsuccessful SMB authentication attempts from Kali Linux.
2. Verified Windows Security Event ID 4625 in Kibana Discover.
3. Confirmed the source IP, destination host, account, and network logon type.
4. Observed two detection alerts from the primary and test rules.
5. Created a Kibana investigation timeline.
6. Attached both alerts to the incident case.
7. Documented the authorized simulation and closed the case.

## Findings

The alerts correctly identified repeated failed SMB authentication attempts from the Kali Linux testing machine.

## Resolution

- Classification: Benign Positive — authorized security test
- Case status: Closed
- Actual compromise: None observed

## Lessons Learned

- Windows Event ID 4625 is useful for investigating authentication failures.
- Logon Type 3 identifies network logon attempts.
- Threshold detections help identify repeated failures from a common source.
- Source context is essential for distinguishing authorized testing from malicious activity.
