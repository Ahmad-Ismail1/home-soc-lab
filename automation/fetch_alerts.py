
import csv
import sys
from collections import Counter
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    TransportError,
)

# ==========================================
# CONFIGURATION
# ==========================================

ES_URL = "https://localhost:9200"

CA_CERT = (
    Path.home()
    / "soc-automation"
    / "certs"
    / "http_ca.crt"
)

ALERT_INDEX = ".internal.alerts-security.alerts-*"

MAX_ALERTS = 1000

OUTPUT_DIR = Path.home() / "soc-automation" / "reports"

SEVERITY_PRIORITY = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
    "unknown": 5,
}

UNRESOLVED_STATUSES = {"open", "acknowledged"}


# ==========================================
# CONNECT TO ELASTICSEARCH
# ==========================================

def connect_elasticsearch():
    if not CA_CERT.is_file():
        raise FileNotFoundError(
            f"CA certificate not found: {CA_CERT}"
        )

    username = input("Elasticsearch username: ").strip()
    password = getpass("Elasticsearch password: ")

    es = Elasticsearch(
        ES_URL,
        basic_auth=(username, password),
        ca_certs=str(CA_CERT),
        request_timeout=30,
    )

    info = es.info()

    print("\n[+] Connected to Elasticsearch")
    print(f"[+] Cluster: {info['cluster_name']}")
    print(f"[+] Version: {info['version']['number']}")

    return es


# ==========================================
# RETRIEVE SECURITY ALERTS
# ==========================================

def fetch_alerts(es):
    response = es.search(
        index=ALERT_INDEX,
        expand_wildcards="all",
        size=0,
        track_total_hits=True,
        query={"match_all": {}},
    )

    total = response["hits"]["total"]["value"]

    print(f"\n[+] Total alerts in index: {total}")

    if total == 0:
        return []

    alerts = []

    # Retrieve alerts in batches using the Elasticsearch
    # scan helper, capped at MAX_ALERTS.
    from elasticsearch.helpers import scan

    for hit in scan(
        client=es,
        index=ALERT_INDEX,
        query={
            "query": {"match_all": {}},
            "sort": [{"@timestamp": {"order": "desc"}}],
        },
        scroll="2m",
        size=200,
        preserve_order=True,
        clear_scroll=True,
        request_timeout=30,
    ):
        alerts.append(hit)

        if len(alerts) >= MAX_ALERTS:
            break

    print(f"[+] Retrieved {len(alerts)} alerts")

    if total > MAX_ALERTS:
        print(
            f"[!] Limited to the {MAX_ALERTS} most recent alerts"
        )

    return alerts


# ==========================================
# NORMALIZE ALERT DATA
# ==========================================

def normalize_alert(hit):
    source = hit.get("_source", {})

    host_data = source.get("host") or {}

    if not isinstance(host_data, dict):
        host_data = {}

    return {
        "timestamp": source.get("@timestamp", "Unknown"),
        "rule": source.get(
            "kibana.alert.rule.name", "Unknown"
        ),
        "severity": str(
            source.get("kibana.alert.severity", "unknown")
        ).lower(),
        "status": str(
            source.get(
                "kibana.alert.workflow_status",
                "unknown",
            )
        ).lower(),
        "host": host_data.get("name", "Unknown"),
        "alert_id": hit.get("_id", "Unknown"),
    }


# ==========================================
# ANALYZE ALERTS
# ==========================================

def analyze_alerts(alerts):
    severity_counts = Counter(
        alert["severity"] for alert in alerts
    )

    status_counts = Counter(
        alert["status"] for alert in alerts
    )

    print("\n========== SOC ALERT SUMMARY ==========")
    print(f"Total analyzed: {len(alerts)}")

    print("\nSeverity Distribution:")

    for severity in [
        "critical",
        "high",
        "medium",
        "low",
        "unknown",
    ]:
        print(
            f"  {severity.capitalize()}: "
            f"{severity_counts.get(severity, 0)}"
        )

    print("\nWorkflow Status:")

    for status in [
        "open",
        "acknowledged",
        "closed",
        "unknown",
    ]:
        print(
            f"  {status.capitalize()}: "
            f"{status_counts.get(status, 0)}"
        )

    unresolved = [
        alert
        for alert in alerts
        if alert["status"] in UNRESOLVED_STATUSES
    ]

    unresolved.sort(
        key=lambda alert: (
            SEVERITY_PRIORITY.get(
                alert["severity"], 5
            ),
            alert["timestamp"],
        )
    )

    high_priority = [
        alert
        for alert in unresolved
        if alert["severity"] in {"critical", "high"}
    ]

    print("\n========== TRIAGE SUMMARY ==========")
    print(f"Unresolved alerts: {len(unresolved)}")
    print(f"Unresolved high-priority: {len(high_priority)}")

    print("\n========== HIGH-PRIORITY QUEUE ==========")

    if not high_priority:
        print("[+] No unresolved critical/high alerts found.")
    else:
        for alert in high_priority:
            print(
                f"[!] {alert['severity'].upper()} | "
                f"{alert['rule']} | "
                f"Host: {alert['host']} | "
                f"Status: {alert['status']}"
            )

    return unresolved, high_priority


# ==========================================
# EXPORT CSV REPORTS
# ==========================================

def export_csv(alerts, filename):
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    output_path = OUTPUT_DIR / filename

    fields = [
        "timestamp",
        "rule",
        "severity",
        "status",
        "host",
        "alert_id",
    ]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(alerts)

    output_path.chmod(0o600)

    print(
        f"[+] Exported {len(alerts)} alerts to {output_path}"
    )


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    print("=" * 50)
    print("        SOC ALERT TRIAGE AUTOMATION")
    print("=" * 50)

    try:
        es = connect_elasticsearch()

        raw_alerts = fetch_alerts(es)

        alerts = [
            normalize_alert(hit)
            for hit in raw_alerts
        ]

        unresolved, high_priority = analyze_alerts(alerts)

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d_%H%M%S")

        print("\n========== EXPORTING REPORTS ==========")

        export_csv(
            alerts,
            f"all_alerts_{timestamp}.csv",
        )

        export_csv(
            unresolved,
            f"unresolved_alerts_{timestamp}.csv",
        )

        export_csv(
            high_priority,
            f"high_priority_alerts_{timestamp}.csv",
        )

        print("\n[+] SOC automation completed successfully!")

    except AuthenticationException:
        print("\n[-] Authentication failed. Check credentials.")
        sys.exit(1)

    except AuthorizationException:
        print("\n[-] Insufficient Elasticsearch permissions.")
        sys.exit(1)

    except ConnectionError as error:
        print(f"\n[-] Elasticsearch connection error: {error}")
        sys.exit(1)

    except (TransportError, OSError, ValueError) as error:
        print(f"\n[-] Automation failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
