
from elasticsearch import Elasticsearch
from getpass import getpass
from pathlib import Path

# Elasticsearch connection settings
ELASTICSEARCH_URL = "https://localhost:9200"
CA_CERT = Path.home() / "soc-automation/certs/http_ca.crt"

# Request credentials without displaying the password
username = input("Elasticsearch username: ")
password = getpass("Elasticsearch password: ")

try:
    es = Elasticsearch(
        ELASTICSEARCH_URL,
        basic_auth=(username, password),
        ca_certs=str(CA_CERT),
        request_timeout=10
    )

    # Verify the connection
    info = es.info()

    print("\n[+] Successfully connected to Elasticsearch!")
    print(f"[+] Cluster: {info['cluster_name']}")
    print(f"[+] Node: {info['name']}")
    print(f"[+] Version: {info['version']['number']}")

except Exception as error:
    print(f"\n[-] Elasticsearch connection failed: {error}")
