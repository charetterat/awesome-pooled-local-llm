<div align="center">

# awesome-pooled-local-llm

**A curated index of ways to run one LLM across the devices you already own —
instead of buying a bigger GPU.**

Pool your Mac + iPhone, two PCs, a LAN of machines, or even browser tabs.
What each project actually does, what hardware it needs, and the gotchas that
only show up in issue threads — every entry linked to its source.

> ⛔ **Not affiliated with any project listed here.** Star counts are a snapshot
> (2026-10-24), not a ranking. We have not benchmarked these projects
> ourselves; numbers quoted are each project's own published results.

</div>

---

## The one-page map

| project | devices it pools | what you actually get | ★ |
|---|---|---|---:|
| [Backburner](https://github.com/StayLameBro/backburner) | M-series Mac + iPhone 15 Pro or newer over USB-C | iPhone helps a Mac run a bigger model over one cable | 771 |
| [Pooled](https://github.com/Nehanth/pooled) | any browser (WebGPU), phone or desktop | P2P inference in the browser — every device with a tab joins the pool | 575 |
| [exo](https://github.com/exo-explore/exo) | Macs, GPUs, phones on one network | The incumbent: frontier models across your existing devices | 47769 |
| [lmstudio-two-pc-split](https://github.com/momcilovicrobert-momc/lmstudio-two-pc-split) | two PCs on one LAN (AMD Radeon + anything, Vulkan) | Two PCs, one model, LM Studio: two DLLs + one env var | 2 |
| [DRIFT](https://github.com/TaewoooPark/DRIFT) | Mac (Apple MPS) + Windows PC (NVIDIA CUDA) | One model split across a Mac (MPS) + Windows PC (CUDA) | 26 |
| [llamacpp-distributed-inference](https://github.com/ADT109119/llamacpp-distributed-inference) | multiple PCs on a LAN | GUI wrapper for llama.cpp RPC across a LAN | 96 |
| [esp32s3-distributed-ai](https://github.com/wladimiravila/esp32s3-distributed-ai) | 3x ESP32-S3 boards over ESP-NOW | One LLM across 3 ESP32 boards, fully offline | 110 |
| [network-container](https://github.com/aphillipsmusik/network-container) | networked machines, Docker | RAM/VRAM pool across machines, no central orchestrator | 0 |
| [tensorgrid](https://github.com/konstantinos193/tensorgrid) | machines on a LAN, CPU+RAM+GPU | Rust runtime pooling CPU/RAM/GPU across a LAN | 0 |
| [memcloud](https://github.com/vibhanshu2001/memcloud) | macOS/Windows/Linux on one LAN | Pooled RAM as a KV-store memory tier (dormant) | 14 |
| [OpenFabric](https://github.com/tdev09/OpenFabric) | macOS/Linux/Windows/Raspberry Pi | Zero-config mesh incl. Raspberry Pi (very early) | 4 |
| [moe-l2](https://github.com/yalun753/moe-l2) | one 8 GB+ GPU | Single-device alternative: 100B+ MoE on an 8 GB card | 146 |
| [dsv41-flash-offload](https://github.com/0xSero/dsv41-flash-offload) | one 24 GB RTX 3090 + DDR4 + NVMe | Single-device alternative: RAM+SSD tiering on one 3090 | 101 |
| [ComfyUI-MultiGPU](https://github.com/pollockjj/ComfyUI-MultiGPU) | one or more GPUs | Image-gen sibling: mature block-swap proof (not LLM) | 992 |

---

## The flagships

### [Backburner](https://github.com/StayLameBro/backburner) — Mac + iPhone over one cable

Your iPhone runs the tail layers (prefill) or old-KV attention (decode) while the Mac runs the rest, pipelined over a 10 Gb/s cable. Measured +29-44% prefill at 16k-48k ctx, 196k-229k context at 8-bit on an iPhone 17 Pro Max. Greedy output token-identical with and without the phone.

| requirement | detail |
|---|---|
| Mac | Apple Silicon; tested on M4 Pro 24 GB |
| Phone | iPhone 15 Pro or newer (or M-series iPad, untested) |
| Cable | 10 Gb/s USB-C — ⛔ the cable in the iPhone box is USB 2 and too slow |
| Install | AltStore with a free Apple ID, no developer account |
| After every reboot | re-run `sudo sysctl iogpu.wired_limit_mb=...` — macOS resets it |

**Known limits, from the issue threads:**

| situation | what happens | source |
|---|---|---|
| 8 GB Mac + iPhone | stock 27B does not fit; split decode is the path, ~4 tok/s on a MacBook Neo + iPhone Air | [#1](https://github.com/StayLameBro/backburner/issues/1) |
| iPhone Air (USB-2 port) | cable link caps at 480 Mb/s — per-device bottleneck, not a software bug | [#1](https://github.com/StayLameBro/backburner/issues/1) |
| M4 Pro + iPhone 18 Pro Max | L32/L36/L40/L44 splits benchmarked; phone app budget ~6,000 MiB confirms the entitlement works | [#14](https://github.com/StayLameBro/backburner/issues/14) |

### [Pooled](https://github.com/Nehanth/pooled) — every device with a browser

Peer-to-peer LLM inference in the browser: pool your devices over WebRTC to run big open models, for chat and coding agents. No install — it runs in a tab.

No cable, no install, no side-loading: devices discover each other over WebRTC
and run the model in a tab. Choose it over Backburner when your second device
is a phone you would rather not side-load apps onto.

### [exo](https://github.com/exo-explore/exo) — the incumbent

Run frontier models distributed across your existing devices. The incumbent in this space — if you have several Apple-silicon machines this is the lowest-friction path.

It is older and much larger than everything else here. If your devices are all
Apple silicon and you want the least experimental path, start here, not with
the new projects.

---

## By what you own

**Two PCs on a LAN** → [lmstudio-two-pc-split](https://github.com/momcilovicrobert-momc/lmstudio-two-pc-split)
(two DLLs + one env var) · [llamacpp-distributed-inference](https://github.com/ADT109119/llamacpp-distributed-inference)
(same RPC mechanism, with a GUI)

**Mac + Windows PC** → [DRIFT](https://github.com/TaewoooPark/DRIFT) — heterogeneous pipeline,
bit-for-bit identical output claim

**A drawer of boards** → [esp32s3-distributed-ai](https://github.com/wladimiravila/esp32s3-distributed-ai)
— three ESP32-S3 boards, 56M params, fully offline. The extreme small end.

**Heterogeneous LAN, early stage** → [tensorgrid](https://github.com/konstantinos193/tensorgrid) ·
[OpenFabric](https://github.com/tdev09/OpenFabric) · [network-container](https://github.com/aphillipsmusik/network-container)
— all promising, all zero-to-few stars, all missing license files. Watch, don't build on them yet.

**The memory tier underneath** → [memcloud](https://github.com/vibhanshu2001/memcloud) — pooled RAM
as a KV store for LLM serving; dormant since 2025-12.

**No second device?** The honest alternatives are single-machine:
[moe-l2](https://github.com/yalun753/moe-l2) (expert offload, 100B+ MoE on 8 GB cards) ·
[dsv41-flash-offload](https://github.com/0xSero/dsv41-flash-offload) (RAM+SSD tiering on one 3090) ·
[ComfyUI-MultiGPU](https://github.com/pollockjj/ComfyUI-MultiGPU) (image-gen; the mature proof block-swap
works at scale). These are the boundary of this list — if you can pool, compare against them.

---

## What this list is not

- **Not a benchmark.** Numbers quoted are each project's own; we have not run any of them.
- **Not exhaustive for model-parallel research** — training-time parallelism frameworks are out of scope.
- **Not affiliated** with any project here.

### Corrections to things that look obvious but are wrong

| sounds true | what the sources say | source |
|---|---|---|
| “the cable in the box will do” | The iPhone box cable is USB 2; Backburner names a 10 Gb/s cable as a requirement. | [Backburner README](https://github.com/StayLameBro/backburner) |
| “any iPhone will do” | Backburner requires iPhone 15 Pro or newer; the A17-class GPUs are the floor. | [Backburner README](https://github.com/StayLameBro/backburner) |
| “more devices is always better” | The 8 GB MacBook Neo result shows a pool can be *slower* than the right single machine at ~4 tok/s; pooling is a fit question, not a count question. | [#1](https://github.com/StayLameBro/backburner/issues/1) |

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
