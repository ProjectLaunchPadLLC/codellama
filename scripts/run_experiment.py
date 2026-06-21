#!/usr/bin/env python3
import argparse
import json
import os
import time
from datetime import datetime
import numpy as np
import torch

def require_confirm():
    p = argparse.ArgumentParser()
    p.add_argument("--confirm", action="store_true")
    p.add_argument("--user", type=str, required=False)
    # other args...
    args, _ = p.parse_known_args()

    # allow local dev bypass with env var
    if os.getenv("CSDFS_SKIP_CONFIRM") == "1":
        print("CSDFS_SKIP_CONFIRM=1 detected — bypassing confirm guard (dev only).")
        return args

    if not args.confirm or not args.user:
        print("This script requires --confirm and --user <ID>. Exiting.")
        raise SystemExit(2)
    return args


def main():
    args = require_confirm()
    out = args.output.rstrip("/")
    os.makedirs(out, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    seeds = {"numpy": int(np.random.randint(0,2**31)), "torch": int(torch.randint(0,2**31,(1,)).item())}
    with open(f"{out}/seeds.json","w") as f:
        json.dump(seeds, f, indent=2)
    with open(f"{out}/runtime_metadata.json","w") as f:
        json.dump({"python": os.sys.version, "torch": torch.__version__}, f, indent=2)
    # tiny synthetic loop
    energies = []
    for i in range(min(args.steps, 1000)):
        energies.append(float(np.random.rand()))
        time.sleep(0.001)
    with open(f"{out}/energies.json","w") as f:
        json.dump({"energies": energies}, f)
    print("Smoke test complete. Outputs written to", out)

if __name__ == "__main__":
    main()
