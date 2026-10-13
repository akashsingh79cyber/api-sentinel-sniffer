# API-Sentinel: Kernel Sniffer (Member 1)

Part of API-Sentinel, a runtime BOLA and Shadow API detection engine.
This module captures HTTP API traffic at the Linux kernel level using eBPF,
without changing any microservice code.

## Architecture
mock microservice -> eBPF tracepoint (sys_enter_sendto) -> JSON -> Python receiver -> structured events

## Files
- mock_server.py : mock microservice (orders and billing endpoints, port 8080)
- poc/http_sniffer.bt : bpftrace eBPF program, prints captured HTTP requests
- poc/http_json.bt : same program, emits JSON-friendly output
- poc/receiver.py : Python receiver, extracts method/path/host, filters port 8080
- poc/benchmark.py : latency benchmark (baseline vs with sniffer)
- api-sentinel-sniffer*/ : Rust + Aya skeleton (port in progress)

## How to run
1. python3 mock_server.py
2. sudo env BPFTRACE_MAX_STRINGLENGTH=256 bpftrace -f json poc/http_json.bt | python3 poc/receiver.py
3. curl http://127.0.0.1:8080/api/orders/101

Output: {"pid": 5012, "comm": "curl", "method": "GET", "path": "/api/orders/101", "host": "127.0.0.1:8080"}

## Daily progress
- Day 1: Environment setup (Rust, Aya), hello-world tracepoint
- Day 2: HTTP capture via sys_enter_sendto, mock server
- Day 3: JSON output, Python receiver, port 8080 filter
- Day 4: Latency benchmark and documentation

## Latency result
Run: python3 poc/benchmark.py baseline, then with sniffer running: python3 poc/benchmark.py sniffer, then python3 poc/benchmark.py compare
Result: (paste your compare output here)

## Known limitations
- Only plain HTTP (HTTPS needs SSL library uprobes)
- Port is read from the Host header because sendto has no destination port
- Rust/Aya build blocked by an LLVM version mismatch on Kali; PoC uses bpftrace (same eBPF mechanism)

## Next steps
- Finish the Rust/Aya port (Ubuntu or pinned toolchain)
- Active blocking mode (Week 3)
- Send events to the Python backend (Member 2) and React dashboard (Member 4)

## python3 poc/benchmark.py compare
sniffer {'mean': 1.26, 'median': 1.179, 'p95': 1.928, 'p99': 2.863}
                  baseline  with sniffer
mean               1.063ms       1.260ms
median             1.025ms       1.179ms
p95                1.481ms       1.928ms
p99                2.161ms       2.863ms

Average overhead: 0.197 ms
RESULT: PASS (< 5 ms)

