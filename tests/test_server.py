import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from server import parse_xml,report_data
class Tests(unittest.TestCase):
 def test_parse_only_open_ports(self):
  xml='<?xml version="1.0"?><nmaprun><host><status state="up"/><address addr="192.0.2.10" addrtype="ipv4"/><ports><port protocol="tcp" portid="22"><state state="open"/><service name="ssh" product="OpenSSH" version="9.0"/></port><port protocol="tcp" portid="80"><state state="closed"/></port></ports></host></nmaprun>'
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"a.xml";p.write_text(xml);h=parse_xml(p)
  self.assertEqual(len(h),1);self.assertEqual(len(h[0]["ports"]),1);self.assertEqual(h[0]["ports"][0]["service"],"ssh")
 def test_telnet_finding(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"services.xml").write_text('<nmaprun><host><status state="up"/><address addr="192.0.2.2" addrtype="ipv4"/><ports><port protocol="tcp" portid="23"><state state="open"/><service name="telnet"/></port></ports></host></nmaprun>')
   self.assertEqual(report_data(p)["findings"][0]["severity"],"high")
 def test_empty_xml(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"x.xml";p.write_text("<nmaprun/>");self.assertEqual(parse_xml(p),[])
if __name__=="__main__": unittest.main()
