"""Generates assets/geo.js: timezone->country, country names, region lists for the alerts selector."""
import json
from babel import Locale
names = {k: v for k, v in Locale('en').territories.items() if len(k) == 2 and k.isalpha()}
names["GB"] = "United Kingdom"; names["US"] = "United States"
tz = {}
for fn in ["/usr/share/zoneinfo/zone1970.tab", "/usr/share/zoneinfo/zone.tab"]:
    for line in open(fn):
        if line.startswith("#") or not line.strip(): continue
        p = line.rstrip("\n").split("\t"); tz.setdefault(p[2], p[0].split(",")[0])
US = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA","California"),("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("DC","District of Columbia"),("FL","Florida"),("GA","Georgia"),("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),("WI","Wisconsin"),("WY","Wyoming"),("PR","Puerto Rico"),("VI","US Virgin Islands"),("GU","Guam")]
GB = [("se","London & South East England"),("ee","East of England"),("sw","South West England"),("wm","West Midlands"),("em","East Midlands"),("yh","Yorkshire & Humber"),("nw","North West England"),("ne","North East England"),("wl","Wales"),("ni","Northern Ireland"),("st","Strathclyde"),("dg","Dumfries, Galloway, Lothian & Borders"),("ta","Central, Tayside & Fife"),("gr","Grampian"),("he","Highlands & Eilean Siar"),("os","Orkney & Shetland")]
# UK timezone-independent default region guess is not possible; US state from timezone is a rough hint only.
US_TZ_HINT = {"America/New_York":"NY","America/Chicago":"IL","America/Denver":"CO","America/Phoenix":"AZ","America/Los_Angeles":"CA","America/Anchorage":"AK","Pacific/Honolulu":"HI","America/Detroit":"MI","America/Indiana/Indianapolis":"IN","America/Kentucky/Louisville":"KY","America/Boise":"ID"}
# Countries whose alerts come from a national service we read (used for the "covered" note)
COVERED = ["GB","US","AT","BE","BA","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IS","IE","IL","IT","LV","LT","LU","MT","MD","ME","NL","MK","NO","PL","PT","RO","RS","SK","SI","ES","SE","CH","UA"]
js = "window.BSOS_GEO=" + json.dumps({"tz": tz, "names": names, "regions": {"US": US, "GB": GB}, "usTz": US_TZ_HINT, "covered": COVERED}, separators=(",", ":"), ensure_ascii=False) + ";\n"
open("assets/geo.js", "w").write(js)
print("geo.js", len(js), "bytes;", len(tz), "zones;", len(names), "countries")
