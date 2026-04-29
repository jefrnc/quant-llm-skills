#!/usr/bin/env python3
"""Run regression evals for quant-llm-skills.

Loads evals/evals.yaml, runs each prompt through `claude --plugin-dir`,
and asserts the response contains the required keywords (and lacks the
forbidden ones). Optionally runs the baseline (no plugin) for
comparison.

Exits 0 if all evals pass, 1 if any fail.

Usage:
  python3 evals/run_evals.py              # CI gate
  python3 evals/run_evals.py --baseline   # also compare without plugin
  python3 evals/run_evals.py --filter id  # run subset
  python3 evals/run_evals.py --verbose    # print full responses
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = str(ROOT)
TIMEOUT_SEC = 180


def run_claude(prompt: str, model: str, with_plugin: bool) -> str:
    cmd = ["claude", "--model", model, "-p", prompt]
    if with_plugin:
        cmd = ["claude", "--plugin-dir", PLUGIN_DIR, "--model", model, "-p", prompt]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TIMEOUT_SEC
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"<TIMEOUT after {TIMEOUT_SEC}s>"


def matches(pattern: Any, text: str) -> bool:
    if isinstance(pattern, str):
        return pattern.lower() in text.lower()
    if isinstance(pattern, dict) and "regex" in pattern:
        return bool(re.search(pattern["regex"], text, re.IGNORECASE))
    return False


def check(text: str, must_contain: list, must_not_contain: list) -> list[str]:
    failures = []
    for p in must_contain or []:
        if not matches(p, text):
            failures.append(f"missing: {p!r}")
    for p in must_not_contain or []:
        if matches(p, text):
            failures.append(f"forbidden: {p!r}")
    return failures


def run_one(eval_def: dict, default_model: str, run_baseline: bool) -> dict:
    eval_id = eval_def["id"]
    model = eval_def.get("model", default_model)
    prompt = eval_def["prompt"]

    t0 = time.time()
    with_resp = run_claude(prompt, model, with_plugin=True)
    with_failures = check(
        with_resp,
        eval_def.get("must_contain", []),
        eval_def.get("must_not_contain", []),
    )

    baseline_resp, baseline_failures = None, None
    if run_baseline:
        baseline_resp = run_claude(prompt, model, with_plugin=False)
        baseline_failures = check(
            baseline_resp,
            eval_def.get("must_contain", []),
            eval_def.get("must_not_contain", []),
        )

    return {
        "id": eval_id,
        "model": model,
        "elapsed": time.time() - t0,
        "with_failures": with_failures,
        "with_response": with_resp,
        "baseline_failures": baseline_failures,
        "baseline_response": baseline_resp,
        "differentiator": eval_def.get("differentiator", False),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--filter", default="")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--max-workers", type=int, default=4)
    args = parser.parse_args()

    manifest_path = ROOT / "evals" / "evals.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    default_model = manifest.get("default_model", "claude-haiku-4-5-20251001")
    evals = [
        e for e in manifest["evals"]
        if not args.filter or args.filter in e["id"]
    ]

    print(f"Running {len(evals)} eval(s) "
          f"(model: {default_model}, baseline: {args.baseline}) …")

    failures = 0
    differentiators_proven = 0
    differentiators_total = 0

    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = {
            ex.submit(run_one, e, default_model, args.baseline): e for e in evals
        }
        for fut in as_completed(futures):
            r = fut.result()
            label = r["id"]
            elapsed = f"{r['elapsed']:.1f}s"

            if r["with_failures"]:
                print(f"  ✗ {label}  ({elapsed})")
                for f in r["with_failures"]:
                    print(f"      {f}")
                if args.verbose:
                    print(f"      response: {r['with_response'][:300]!r}")
                failures += 1
                continue

            # When --baseline is set, classify EVERY passing eval as
            # either differentiator (baseline failed) or shared (baseline
            # also passed). Differentiator marker is just a "we expected
            # this" hint.
            if r["baseline_failures"] is not None:
                differentiators_total += 1
                if r["baseline_failures"]:
                    differentiators_proven += 1
                    expected = " [as expected]" if r["differentiator"] else ""
                    print(f"  ✓ {label}  ({elapsed})  "
                          f"[differentiator: baseline failed{expected}]")
                else:
                    expected = " [marked as differentiator but model already knew]" if r["differentiator"] else ""
                    print(f"  ✓ {label}  ({elapsed})  "
                          f"[shared: baseline also passed{expected}]")
            else:
                print(f"  ✓ {label}  ({elapsed})")

    if differentiators_total:
        print(f"\nDifferentiators proven: "
              f"{differentiators_proven}/{differentiators_total}")

    if failures:
        print(f"\n✗ {failures}/{len(evals)} eval(s) failed")
        return 1
    print(f"\n✓ All {len(evals)} eval(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
