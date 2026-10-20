# Home SOC Lab Architecture

## Overview

This project implements a virtual Security Operations Center (SOC) environment using VMware Workstation, Elastic Security, Windows endpoints, and Kali Linux.

## Virtual Machines

| Virtual Machine | IP Address | Role |
|---|---|---|
| SOC-ELK | 192.168.100.10 | Elasticsearch, Kibana, Fleet Server |
| WIN01 | 192.168.100.20 | Windows endpoint and attack simulation target |
| WIN02 | 192.168.100.21 | Additional Windows endpoint |
| KALI-LAB | 192.168.100.30 | Security testing and attack simulation |
| DC01 | 192.168.100.40 | Windows domain controller |

## Network Configuration

- Hypervisor: VMware Workstation
- Lab network: VMnet2 (192.168.100.0/24)
- Network type: Host-only / isolated
- NAT network: 192.168.94.0/24, used for updates

## Security Monitoring

- Elastic Agent collects endpoint telemetry.
- Windows Security logs provide authentication and system activity events.
- Sysmon provides additional process execution telemetry.
- Elasticsearch stores and indexes collected events.
- Kibana and Elastic Security support alerting and investigations.

## Security Testing

Authorized simulations include SMB authentication failures, encoded PowerShell execution, and scheduled task creation.

All testing is performed within the controlled lab environment.
