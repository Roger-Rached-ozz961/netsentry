#!/usr/bin/env bash
set -Eeuo pipefail
APP="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUT="$APP/reports"; mkdir -p "$OUT"
C=$'\033[96m'; G=$'\033[92m'; Y=$'\033[93m'; R=$'\033[91m'; X=$'\033[0m'
banner(){ printf "%s\n" "${C}╔══════════════════════════════════════════════════════════════╗" "║ NETSENTRY | Automated Network Discovery & Service Audit   ║" "╚══════════════════════════════════════════════════════════════╝${X}"; }
has(){ command -v "$1" >/dev/null 2>&1; }
tools(){ for t in nmap python3 arp-scan jq curl; do if has "$t"; then printf "%-12s %s\n" "$t" "${G}available${X}"; else printf "%-12s %s\n" "$t" "${Y}missing / optional${X}"; fi; done; }
install(){ if has apt-get; then sudo apt-get update && sudo apt-get install -y nmap python3 arp-scan jq curl; elif has dnf; then sudo dnf install -y nmap python3 arp-scan jq curl; elif has pacman; then sudo pacman -Sy --needed nmap python arp-scan jq curl; elif has zypper; then sudo zypper install -y nmap python3 arp-scan jq curl; elif has brew; then brew install nmap python arp-scan jq curl; else echo "Install Nmap and Python 3 manually."; fi; }
scan(){
 has nmap || { echo "Nmap missing. Choose install tools."; return 1; }
 read -rp "Authorized IPv4 target (host/CIDR/range): " target
 [[ "$target" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}(/[0-9]{1,2}|-[0-9]{1,3}(\.[0-9]{1,3}){3})?$ ]] || { echo "Invalid target format."; return 1; }
 echo "1 Quick (top 100)  2 Standard (top 1000)  3 Comprehensive (all TCP ports)"
 read -rp "Profile [2]: " profile; profile=${profile:-2}
 case "$profile" in 1) ports="--top-ports 100";; 2) ports="--top-ports 1000";; 3) ports="-p-";; *) echo "Invalid profile"; return 1;; esac
 stamp=$(date -u +%Y%m%dT%H%M%SZ); safe=$(printf %s "$target" | tr '/:' '__' | tr -cd 'A-Za-z0-9_.-')
 dir="$OUT/${stamp}_${safe}"; mkdir -m 700 -p "$dir"
 echo "[1/2] Host discovery"; nmap -sn -oA "$dir/discovery" "$target"
 echo "[2/2] TCP service/version scan"; nmap -sV -T3 --open $ports -oA "$dir/services" "$target"
 echo "${G}Saved: $dir${X}"
}
dashboard(){ python3 "$APP/server.py" --reports "$OUT" --host 127.0.0.1 --port 8765; }
while true; do
 banner; echo " 1) Scan network  2) Launch dashboard  3) Check tools  4) Install tools  5) Exit"
 read -rp "Select: " c
 case "$c" in 1) scan;; 2) dashboard;; 3) tools; read -rp "Enter to continue" _;; 4) install;; 5) exit 0;; *) echo "Invalid option";; esac
done
