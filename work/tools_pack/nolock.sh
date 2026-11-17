#!/bin/bash
# nolock.sh CMD... — runs CMD only when no measurement holds /home/claude/work/PERF_LOCK and no other measurement chromium runs; else exits 3
if [ -e /home/claude/work/PERF_LOCK ]; then echo "LOCKED: $(cat /home/claude/work/PERF_LOCK) — not running"; exit 3; fi
exec "$@"
