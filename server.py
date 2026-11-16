#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from xml.etree import ElementTree as ET

BASE=Path(__file__).resolve().parent
WEB=BASE/"dashboard"
RULES={
21:("FTP exposed","medium","FTP may transmit credentials or data without modern encryption.","Prefer SFTP/FTPS and restrict access."),
23:("Telnet exposed","high","Telnet sessions are not protected by modern encryption.","Disable Telnet and use SSH."),
445:("SMB exposed","high","SMB exposure can increase lateral movement and file-sharing risk.","Restrict SMB to trusted network segments."),
3389:("RDP exposed","medium","Remote Desktop is a common remote-access attack surface.","Require MFA and restrict access through VPN or ZTNA."),
5900:("VNC exposed","medium","VNC may expose interactive desktop access.","Restrict access and use encrypted tunnels."),
2375:("Docker API exposed","critical","Plaintext Docker API access can enable host-level control.","Disable remote plaintext API; use authenticated TLS and ACLs."),
6379:("Redis listener exposed","high","An accessible Redis listener may expose data or administrative functions.","Bind to trusted interfaces and enforce authentication."),
27017:("MongoDB listener exposed","high","A database listener should not be broadly reachable.","Restrict network access and enforce authentication."),
9200:("Elasticsearch listener exposed","high","Search APIs can expose indexed data if misconfigured.","Require authentication and restrict network access."),
3306:("MySQL listener exposed","medium","A database port is reachable from the scan vantage point.","Limit source networks and enforce TLS."),
5432:("PostgreSQL listener exposed","medium","A database port is reachable from the scan vantage point.","Limit source networks and enforce TLS.")
}
def parse_xml(path):
 try: root=ET.parse(path).getroot()
 except (OSError,ET.ParseError): return []
 hosts=[]
 for h in root.findall("host"):
  st=h.find("status")
  if st is not None and st.get("state")!="up": continue
  a=next((x.get("addr") for x in h.findall("address") if x.get("addrtype")=="ipv4"),"unknown")
  hn=h.find("hostnames/hostname"); hostname=hn.get("name","") if hn is not None else ""
  ports=[]
  for p in h.findall("ports/port"):
   state=p.find("state")
   if state is None or state.get("state")!="open": continue
   s=p.find("service")
   ports.append({"port":int(p.get("portid","0")),"protocol":p.get("protocol","tcp"),"service":s.get("name","unknown") if s is not None else "unknown","product":s.get("product","") if s is not None else "","version":s.get("version","") if s is not None else ""})
  hosts.append({"ip":a,"hostname":hostname,"ports":ports})
 return hosts
def report_data(folder):
 hosts=parse_xml(folder/"services.xml"); findings=[]
 for h in hosts:
  for p in h["ports"]:
   if p["port"] in RULES:
    title,sev,desc,fix=RULES[p["port"]]
    findings.append({"id":f'{h["ip"]}:{p["port"]}',"ip":h["ip"],"port":p["port"],"service":p["service"],"title":title,"severity":sev,"description":desc,"recommendation":fix,"evidence":f'{h["ip"]}:{p["port"]}/{p["protocol"]}',"references":["https://nvd.nist.gov/","https://attack.mitre.org/techniques/T1046/","https://www.cisa.gov/known-exploited-vulnerabilities-catalog"]})
 return {"id":folder.name,"hosts":hosts,"findings":findings,"host_count":len(hosts),"open_ports":sum(len(h["ports"]) for h in hosts)}
def load_reports(root):
 return [report_data(p) for p in sorted(root.iterdir(),reverse=True) if p.is_dir() and (p/"services.xml").exists()] if root.exists() else []
class Handler(SimpleHTTPRequestHandler):
 reports=Path("reports")
 def __init__(self,*a,**kw): super().__init__(*a,directory=str(WEB),**kw)
 def send_json(self,obj):
  b=json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.send_header("Cache-Control","no-store"); self.end_headers(); self.wfile.write(b)
 def do_GET(self):
  if self.path=="/api/reports": return self.send_json(load_reports(self.reports))
  if self.path.startswith("/api/report/"):
   key=self.path.rsplit("/",1)[-1]
   if key in (".","..") or "/" in key: self.send_error(400); return
   item=next((x for x in load_reports(self.reports) if x["id"]==key),None)
   if item is None: self.send_error(404); return
   return self.send_json(item)
  return super().do_GET()
 def log_message(self,fmt,*args): print("[dashboard] "+fmt%args)
def main():
 p=argparse.ArgumentParser(); p.add_argument("--reports",default="reports"); p.add_argument("--host",default="127.0.0.1"); p.add_argument("--port",type=int,default=8765); a=p.parse_args()
 if a.host not in ("127.0.0.1","localhost","::1"): raise SystemExit("Only loopback binding is allowed.")
 Handler.reports=Path(a.reports).resolve(); srv=ThreadingHTTPServer((a.host,a.port),Handler)
 print(f"Dashboard: http://127.0.0.1:{a.port} (Ctrl+C to stop)")
 try: srv.serve_forever()
 except KeyboardInterrupt: pass
 finally: srv.server_close()
if __name__=="__main__": main()
