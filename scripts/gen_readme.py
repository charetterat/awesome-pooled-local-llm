#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render README.md from data/entries.json.

Same contract as qwen38-flashnext-guide: the JSON is the single source of
truth, the script contains no facts of its own, and --check exits non-zero on
drift so a stale README cannot merge.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "README.md")


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def table(headers, rows, align=None):
    align = align or ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(align) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def first_sentence(s, maxlen=120):
    """First sentence, but never mid-decimal and never mid-name."""
    cut = s.find(". ")
    if cut == -1 or cut > maxlen:
        cut = maxlen
    else:
        cut += 1  # keep the period
    out = s[:cut].rstrip()
    if out.endswith(("llama.", "DeepSeek-V4.", "V4.")):
        # sentence split landed inside a product name — take more text
        nxt = s.find(". ", cut + 1)
        out = s[: nxt + 1] if nxt != -1 and nxt <= maxlen * 2 else s[:maxlen] + "…"
    return out


def main():
    d = load("entries.json")
    entries = d["entries"]

    def find(name):
        for e in entries:
            if e["name"] == name:
                return e
        raise KeyError(name)

    backburner = find("Backburner")
    pooled = find("Pooled")
    exo = find("exo")

    cross = [e for e in entries if e["kind"].startswith(("cross-device", "two-PC",
             "heterogeneous", "LAN", "embedded", "cluster", "mesh", "memory tier"))]
    bounded = [e for e in entries if e["kind"].startswith(("single-device", "image-gen"))]

    L = []
    L.append(f"""<div align="center">

# awesome-pooled-local-llm

**A curated index of ways to run one LLM across the devices you already own —
instead of buying a bigger GPU.**

Pool your Mac + iPhone, two PCs, a LAN of machines, or even browser tabs.
What each project actually does, what hardware it needs, and the gotchas that
only show up in issue threads — every entry linked to its source.

> ⛔ **Not affiliated with any project listed here.** Star counts are a snapshot
> ({d['updated']}), not a ranking. We have not benchmarked these projects
> ourselves; numbers quoted are each project's own published results.

</div>

---

## The one-page map

{table(
    ["project", "devices it pools", "what you actually get", "★"],
    [[f"[{e['name']}]({e['url']})",
      e["hardware"],
      e.get("summary", first_sentence(e["what"])),
      e["stars"]] for e in entries],
    ["---", "---", "---", "---:"])}

---

## The flagships

### [{backburner['name']}]({backburner['url']}) — Mac + iPhone over one cable

{backburner['what']}

{table(
    ["requirement", "detail"],
    [["Mac", "Apple Silicon; tested on M4 Pro 24 GB"],
     ["Phone", "iPhone 15 Pro or newer (or M-series iPad, untested)"],
     ["Cable", "10 Gb/s USB-C — ⛔ the cable in the iPhone box is USB 2 and too slow"],
     ["Install", "AltStore with a free Apple ID, no developer account"],
     ["After every reboot", "re-run `sudo sysctl iogpu.wired_limit_mb=...` — macOS resets it"]],
    ["---", "---"])}

**Known limits, from the issue threads:**

{table(
    ["situation", "what happens", "source"],
    [["8 GB Mac + iPhone", "stock 27B does not fit; split decode is the path, ~4 tok/s on a MacBook Neo + iPhone Air",
      "[#1](https://github.com/StayLameBro/backburner/issues/1)"],
     ["iPhone Air (USB-2 port)", "cable link caps at 480 Mb/s — per-device bottleneck, not a software bug",
      "[#1](https://github.com/StayLameBro/backburner/issues/1)"],
     ["M4 Pro + iPhone 18 Pro Max", "L32/L36/L40/L44 splits benchmarked; phone app budget ~6,000 MiB confirms the entitlement works",
      "[#14](https://github.com/StayLameBro/backburner/issues/14)"]],
    ["---", "---", "---"])}

### [{pooled['name']}]({pooled['url']}) — every device with a browser

{pooled['what']}

No cable, no install, no side-loading: devices discover each other over WebRTC
and run the model in a tab. Choose it over Backburner when your second device
is a phone you would rather not side-load apps onto.

### [exo]({exo['url']}) — the incumbent

{exo['what']}

It is older and much larger than everything else here. If your devices are all
Apple silicon and you want the least experimental path, start here, not with
the new projects.

---

## By what you own

**Two PCs on a LAN** → [lmstudio-two-pc-split]({find('lmstudio-two-pc-split')['url']})
(two DLLs + one env var) · [llamacpp-distributed-inference]({find('llamacpp-distributed-inference')['url']})
(same RPC mechanism, with a GUI)

**Mac + Windows PC** → [DRIFT]({find('DRIFT')['url']}) — heterogeneous pipeline,
bit-for-bit identical output claim

**A drawer of boards** → [esp32s3-distributed-ai]({find('esp32s3-distributed-ai')['url']})
— three ESP32-S3 boards, 56M params, fully offline. The extreme small end.

**Heterogeneous LAN, early stage** → [tensorgrid]({find('tensorgrid')['url']}) ·
[OpenFabric]({find('OpenFabric')['url']}) · [network-container]({find('network-container')['url']})
— all promising, all zero-to-few stars, all missing license files. Watch, don't build on them yet.

**The memory tier underneath** → [memcloud]({find('memcloud')['url']}) — pooled RAM
as a KV store for LLM serving; dormant since 2025-12.

**No second device?** The honest alternatives are single-machine:
[moe-l2]({find('moe-l2')['url']}) (expert offload, 100B+ MoE on 8 GB cards) ·
[dsv41-flash-offload]({find('dsv41-flash-offload')['url']}) (RAM+SSD tiering on one 3090) ·
[ComfyUI-MultiGPU]({find('ComfyUI-MultiGPU')['url']}) (image-gen; the mature proof block-swap
works at scale). These are the boundary of this list — if you can pool, compare against them.

---

## What this list is not

- **Not a benchmark.** Numbers quoted are each project's own; we have not run any of them.
- **Not exhaustive for model-parallel research** — training-time parallelism frameworks are out of scope.
- **Not affiliated** with any project here.

### Corrections to things that look obvious but are wrong

{table(
    ["sounds true", "what the sources say", "source"],
    [["“the cable in the box will do”", "The iPhone box cable is USB 2; Backburner names a 10 Gb/s cable as a requirement.",
      f"[{backburner['name']} README]({backburner['url']})"],
     ["“any iPhone will do”", "Backburner requires iPhone 15 Pro or newer; the A17-class GPUs are the floor.",
      f"[{backburner['name']} README]({backburner['url']})"],
     ["“more devices is always better”", "The 8 GB MacBook Neo result shows a pool can be *slower* than the right single machine at ~4 tok/s; pooling is a fit question, not a count question.",
      "[#1](https://github.com/StayLameBro/backburner/issues/1)"]],
    ["---", "---", "---"])}

---

## Verify this list

Every entry's URL and a keyword that made it worth listing are re-checked by:

```bash
python3 scripts/verify_sources.py
```

It distinguishes `STALE` (page live but no longer says what we cited) from
`UNREACHABLE` (fetch failed) — a claim that went bad is not the same as a flaky network.

---

<div align="center">

**Data** — [`data/entries.json`](data/entries.json) · **Scripts** — [`scripts/verify_sources.py`](scripts/verify_sources.py)

<sub>README.md is generated. Edit the JSON, not this file.</sub>

</div>
""")

    text = "\n".join(L)

    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != text:
            sys.exit("README.md is stale — run: python3 scripts/gen_readme.py")
        print("README.md in sync")
        return

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {OUT} ({len(text):,} chars)")


if __name__ == "__main__":
    main()