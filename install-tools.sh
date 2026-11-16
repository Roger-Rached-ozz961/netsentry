#!/usr/bin/env bash
set -e
echo "NetSentry dependency installer. Required: Nmap, Python 3. Optional: arp-scan, jq, curl."
if command -v apt-get >/dev/null; then sudo apt-get update && sudo apt-get install -y nmap python3 arp-scan jq curl
elif command -v dnf >/dev/null; then sudo dnf install -y nmap python3 arp-scan jq curl
elif command -v pacman >/dev/null; then sudo pacman -Sy --needed nmap python arp-scan jq curl
elif command -v zypper >/dev/null; then sudo zypper install -y nmap python3 arp-scan jq curl
elif command -v brew >/dev/null; then brew install nmap python arp-scan jq curl
else echo "Unsupported package manager. Install Nmap and Python 3 manually."; exit 1; fi
