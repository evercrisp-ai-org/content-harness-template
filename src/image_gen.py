"""Generate the week's image assets from the AI image prompts in a batch folder.

Reads every week-*.md draft in the batch folder, pulls the 9-point AI image
prompt(s) using the same extraction logic as the Drive summary export, calls
the OpenAI Images API once per prompt, and writes PNGs to <batch>/images/.

Usage:
    python3 src/image_gen.py [batch_folder] [--model gpt-image-1-mini]
                             [--quality low|medium|high] [--dry-run]

The OpenAI key is read from the OPENAI_API_KEY environment variable, or from
a `.env` file at the repo root (KEY=value lines). The .env file is gitignored.

Size selection: explicit "WxH" dimensions in the prompt win; otherwise
orientation keywords (vertical/portrait vs horizontal/landscape vs square)
decide. OpenAI's image models support exactly 1024x1024, 1536x1024, and
1024x1536, so platform dimensions are mapped to the nearest orientation and
final resizing happens downstream if a platform needs exact pixels.
"""

import argparse
import base64
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    # macOS python.org builds are not linked to the system keychain; fall
    # back to the system PEM bundle so HTTPS verification still works.
    SSL_CONTEXT = ssl.create_default_context(
        cafile="/etc/ssl/cert.pem" if os.path.exists("/etc/ssl/cert.pem") else None
    )

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_content_batch import _extract_image_prompts, find_latest_batch_folder

OPENAI_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-1-mini"
DEFAULT_QUALITY = "medium"

DIM_RE = re.compile(r"(\d{3,4})\s*[x×]\s*(\d{3,4})")


def load_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(repo_root, ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith("OPENAI_API_KEY=") :
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    sys.exit("No OpenAI key found. Set OPENAI_API_KEY or add it to .env at the repo root.")


def pick_size(prompt: str) -> str:
    m = DIM_RE.search(prompt)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        if w > h:
            return "1536x1024"
        if h > w:
            return "1024x1536"
        return "1024x1024"
    low = prompt.lower()
    if any(k in low for k in ("vertical", "portrait", "9:16", "story format")):
        return "1024x1536"
    if any(k in low for k in ("horizontal", "landscape", "16:9", "1.91:1")):
        return "1536x1024"
    return "1024x1024"


def extract_prompt_list(text: str) -> list:
    """Return individual prompts. Multiple prompts per file are joined with
    blank lines by _extract_image_prompts; prompt bodies themselves never
    contain blank lines (continuations are space-joined)."""
    raw = _extract_image_prompts(text)
    if not raw:
        return []
    return [p.strip() for p in raw.split("\n\n") if p.strip()]


def generate(prompt: str, size: str, model: str, quality: str, api_key: str) -> bytes:
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        OPENAI_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=300, context=SSL_CONTEXT) as resp:
        payload = json.loads(resp.read())
    return base64.b64decode(payload["data"][0]["b64_json"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_folder", nargs="?", default=None)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--quality", default=DEFAULT_QUALITY, choices=["low", "medium", "high"])
    ap.add_argument("--dry-run", action="store_true", help="list planned images without calling the API")
    args = ap.parse_args()

    folder = args.batch_folder or find_latest_batch_folder("outputs/drafts")
    if not folder or not os.path.isdir(folder):
        sys.exit(f"Batch folder not found: {folder}")

    out_dir = os.path.join(folder, "images")
    os.makedirs(out_dir, exist_ok=True)

    drafts = sorted(
        f for f in os.listdir(folder)
        if f.startswith("week-") and f.endswith(".md")
    )

    plan = []
    for fname in drafts:
        text = open(os.path.join(folder, fname)).read()
        prompts = extract_prompt_list(text)
        stem = os.path.splitext(fname)[0]
        for i, prompt in enumerate(prompts, 1):
            suffix = f"-{i}" if len(prompts) > 1 else ""
            plan.append((f"{stem}{suffix}.png", prompt, pick_size(prompt)))

    if not plan:
        sys.exit("No AI image prompts found in this batch folder.")

    print(f"Batch: {folder}  |  model: {args.model}  quality: {args.quality}")
    print(f"{len(plan)} image(s) planned -> {out_dir}\n")

    api_key = None if args.dry_run else load_api_key()
    ok, failed, skipped = 0, 0, 0
    for name, prompt, size in plan:
        out_path = os.path.join(out_dir, name)
        if os.path.exists(out_path):
            print(f"SKIP  {name}  (already exists)")
            skipped += 1
            continue
        if args.dry_run:
            print(f"PLAN  {name:55} {size}  prompt: {len(prompt)} chars")
            continue
        try:
            png = generate(prompt, size, args.model, args.quality, api_key)
            with open(out_path, "wb") as fh:
                fh.write(png)
            print(f"OK    {name:55} {size}  {len(png)//1024} KB")
            ok += 1
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            print(f"FAIL  {name}: HTTP {e.code} {detail}")
            failed += 1
        except Exception as e:
            print(f"FAIL  {name}: {e}")
            failed += 1

    if not args.dry_run:
        print(f"\nDone: {ok} generated, {skipped} skipped, {failed} failed.")
        if failed:
            sys.exit(1)


if __name__ == "__main__":
    main()
