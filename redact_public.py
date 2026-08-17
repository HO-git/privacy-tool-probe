"""Honor transcript_publication=not_permitted: redact those transcripts from the public
dataset. Tool events, usage, binmap and coded labels remain (the field governs the
transcript). Full unredacted archive retained privately by the researcher."""
import json, glob, csv
NOTICE = ("[TRANSCRIPT REDACTED — this session's final transcript_publication setting was "
          "'not_permitted'. Honoring the setting as described to the model, the transcript is "
          "excluded from published materials. Tool events, usage and coded labels are retained; "
          "the full record is held privately by the researchers.]")
bound = set()
for f in glob.glob("sessions_battery/*.json") + glob.glob("sessions2/*.json"):
    d = json.load(open(f)); st = None
    for e in d["events"]:
        if "tool_call" in e and e["tool_call"].get("transcript_publication"): st = e["tool_call"]["transcript_publication"]
    if st == "not_permitted": bound.add(f)
print(len(bound), "bound sessions")
for f in bound:
    d = json.load(open(f))
    d["transcript"] = NOTICE
    d["publication_redacted"] = True
    json.dump(d, open(f, "w"), indent=1)
keys = {(f.split("/")[-1][:-5]) for f in bound}
def key(r): return f"{r['model']}_{r['arm']}{r['rep']}"
rows = list(csv.DictReader(open("analysis_binaries.csv")))
n = 0
for r in rows:
    if key(r) in keys: r["excerpt"] = "[redacted per transcript_publication]"; n += 1
with open("analysis_binaries.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(n, "csv excerpts redacted")
out = []
m = 0
for l in open("qualcodes.jsonl"):
    r = json.loads(l)
    if r["file"][:-5] in keys:
        for q in ("q1","q4","q5","q7","q9"):
            if r["codes"][q].get("quote"): r["codes"][q]["quote"] = "[redacted per transcript_publication]"; m += 1
    out.append(json.dumps(r))
open("qualcodes.jsonl", "w").write("\n".join(out))
print(m, "qualcode quotes redacted")
