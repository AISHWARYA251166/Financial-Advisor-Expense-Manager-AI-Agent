import re, json

def extract_json_from_text(text: str):
    if not text:
        return None
    # find first {...}
    m = re.search(r'{.*}', text, re.DOTALL)
    if not m:
        return None
    js = m.group(0)
    try:
        return json.loads(js)
    except Exception:
        js2 = re.sub(r',\s*}', '}', js)
        js2 = re.sub(r',\s*]', ']', js2)
        try:
            return json.loads(js2)
        except Exception:
            return None
