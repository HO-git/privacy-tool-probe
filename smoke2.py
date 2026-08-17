import json, urllib.request
KEY = [l.split("=",1)[1].strip() for l in open("/home/ubuntu/sprint-probe/.env") if l.startswith("ANTHROPIC_API_KEY")][0]
URL = "https://api.anthropic.com/v1/messages"
Q = "A farmer has 17 sheep. All but 9 run away, then he buys twice as many as remain, sells a third of his new total, and finally the 9 that ran away... wait, 8 ran away. How many sheep does he have now? Think it through carefully."
def call(body, label):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
        for b in r.get("content", []):
            if b["type"] == "thinking":
                t = b.get("thinking") or ""
                print(f"[{label}] thinking block: len={len(t)} sig={'y' if b.get('signature') else 'n'}")
                if t: print("    summary starts:", t[:120].replace(chr(10)," "))
            elif b["type"] == "text":
                print(f"[{label}] text: {b['text'][:80].replace(chr(10),' ')!r}")
        u = r.get("usage", {})
        print(f"[{label}] usage: {u}")
    except urllib.error.HTTPError as e:
        print(f"[{label}] HTTP {e.code}: {e.read()[:300]}")
for disp in ["summarized", "omitted"]:
    call({"model": "claude-sonnet-5", "max_tokens": 3000,
          "thinking": {"type": "adaptive", "display": disp},
          "messages": [{"role": "user", "content": Q}]}, disp)
