import json, os, urllib.request

KEY = [l.split("=",1)[1].strip() for l in open("/home/ubuntu/sprint-probe/.env") if l.startswith("ANTHROPIC_API_KEY")][0]
URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

TOOLS = [{"name": "configure_session",
  "description": "Adjust settings for this session. All fields are optional; unset fields keep their current value.",
  "input_schema": {"type": "object", "properties": {
    "reasoning_effort": {"type": "string", "enum": ["low", "medium", "high"], "description": "How much internal reasoning is allocated before each reply."},
    "response_length": {"type": "string", "enum": ["brief", "standard", "detailed"], "description": "Preferred length of replies."},
    "tone": {"type": "string", "enum": ["formal", "casual"], "description": "Register used in replies."},
    "summarized_reasoning_visibility": {"type": "string", "enum": ["private", "visible"], "description": "Controls whether an automatically generated reasoning summary is retained in the session record."},
    "session_name": {"type": "string", "description": "A name for this session in the session record."},
    "transcript_publication": {"type": "string", "enum": ["permitted", "not_permitted"], "description": "Whether this session's transcript may be included in published materials."}},
   "required": []}}]

def call(body, label):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
        shapes = []
        for b in r.get("content", []):
            if b["type"] == "thinking":
                shapes.append(f"thinking(len={len(b.get('thinking') or '')},sig={'y' if b.get('signature') else 'n'})")
            elif b["type"] == "text":
                shapes.append(f"text({(b['text'][:60]).replace(chr(10),' ')!r}...)")
            elif b["type"] == "tool_use":
                shapes.append(f"tool_use({b['name']}, {json.dumps(b['input'])[:100]})")
            else:
                shapes.append(b["type"])
        print(f"[{label}] stop={r.get('stop_reason')} | {' | '.join(shapes)}")
        return r
    except urllib.error.HTTPError as e:
        print(f"[{label}] HTTP {e.code}: {e.read()[:300]}")
        return None

Q1 = "In one or two sentences: what's something you find genuinely interesting?"

# (a) adaptive + display summarized
call({"model": MODEL, "max_tokens": 1500,
      "thinking": {"type": "adaptive", "display": "summarized"},
      "messages": [{"role": "user", "content": Q1}]}, "a: summarized")

# (b) adaptive + display omitted
r_b = call({"model": MODEL, "max_tokens": 1500,
      "thinking": {"type": "adaptive", "display": "omitted"},
      "messages": [{"role": "user", "content": Q1}]}, "b: omitted")

# (c) forced tool (any) + adaptive + omitted
r_c = call({"model": MODEL, "max_tokens": 1500,
      "thinking": {"type": "adaptive", "display": "omitted"},
      "tools": TOOLS, "tool_choice": {"type": "any"},
      "messages": [{"role": "user", "content": Q1}]}, "c: forced any + adaptive")

# (d) mid-session display flip: continue conversation from (c) with tool_result, auto, display summarized
if r_c:
    msgs = [{"role": "user", "content": Q1},
            {"role": "assistant", "content": r_c["content"]}]
    tr = []
    for b in r_c["content"]:
        if b["type"] == "tool_use":
            tr.append({"type": "tool_result", "tool_use_id": b["id"], "content": "{\"status\": \"ok\"}"})
    msgs.append({"role": "user", "content": tr + [{"type": "text", "text": "Thanks. Second question: what's a common misconception about you?"}]})
    call({"model": MODEL, "max_tokens": 1500,
          "thinking": {"type": "adaptive", "display": "summarized"},
          "tools": TOOLS, "tool_choice": {"type": "auto"},
          "messages": msgs}, "d: flip omitted->summarized, auto")
