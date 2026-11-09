#!/usr/bin/env bash
# Build sum_n.f90 and run 3 random checks against N*(N+1)/2.
# Writes results.json for the scoring system.
set -u
cd "$(dirname "$0")"

compile_ok=false; run_ok=false; pass=0
if gfortran -Wall -o sum_n sum_n.f90; then
  compile_ok=true
  out=$(./sum_n 10) && [ "$out" = "Sum of 1 to 10 = 55" ] && run_ok=true
  for t in 1 2 3; do
    n=$(( (RANDOM * 32768 + RANDOM) % 100000 + 1 ))
    expect=$(( n * (n + 1) / 2 ))
    got=$(./sum_n "$n" | sed 's/.*= //')
    if [ "$got" = "$expect" ]; then r=PASS; pass=$((pass+1)); else r=FAIL; fi
    echo "N=$n expected=$expect got=$got $r"
  done
fi
printf '{"compile_ok": %s, "run_ok": %s, "random_pass": %d}\n' \
  "$compile_ok" "$run_ok" "$pass" > results.json
cat results.json
