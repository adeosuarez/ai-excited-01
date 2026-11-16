#!/usr/bin/env python3
"""Generate entry.png: a striking radiant starburst on a deep gradient sky.

Python stdlib only (zlib, struct). Deterministic output.
"""
import math
import struct
import zlib

W = 1024
H = 1024
CX, CY = W / 2 - 0.5, H / 2 - 0.5
RAYS = 24
RMAX = min(W, H) * 0.48

def pixel(x, y):
    dx, dy = x - CX, y - CY
    r = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)

    # radial fade: bright core to dark rim
    t = min(r / RMAX, 1.0)
    fade = (1.0 - t) ** 1.6

    # starburst: sharp spikes on a soft base glow
    spike = 0.0
    k = ang * RAYS / (2 * math.pi)
    frac = k - math.floor(k)
    sharp = 1.0 - abs(frac - 0.5) * 2.0  # 1 at spike center, 0 between
    if r < RMAX:
        spike = sharp ** 6 * (1.0 - t)

    # rotating secondary shimmer (twist, still fully deterministic)
    twist = math.sin(r / RMAX * 9.0 + ang * 6.0) * 0.15 + 0.85

    core = math.exp(-(r / (RMAX * 0.10)) ** 2)

    # base colors: deep indigo sky -> magenta rim
    base_r = 12 + 210 * (t ** 2)
    base_g = 6 + 30 * t
    base_b = 24 + 90 * (1 - t)

    pr = base_r * twist * fade + 255 * spike + 255 * core
    pg = base_g * twist * fade + 235 * spike + 240 * core
    pb = base_b * twist * fade + 120 * spike + 220 * core

    return (min(int(pr), 255), min(int(pg), 255), min(int(pb), 255))

def build_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        for x in range(W):
            raw.extend(pixel(x, y))

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))

with open("entry.png", "wb") as f:
    f.write(build_png())
print("wrote entry.png")
