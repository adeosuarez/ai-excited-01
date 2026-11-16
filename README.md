# ai-excited-01

make.fun bounty entry: a striking radiant starburst — 24 golden rays bursting
from a white-hot core over a deep indigo-to-magenta sky, rendered as a
1024x1024 PNG.

The image is pre-generated and committed (`entry.png`). `main.ts` verifies it
(non-empty, valid PNG signature, under 1 MiB) and copies it into the output
directory.

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Requires Node 22. Set `MAKEFUN_OUTPUT_DIR` to override the destination
(default `/output`).

## Regenerating the image

```
python3 scripts/gen.py
```

Python stdlib only (zlib, struct); fully deterministic, no network.
