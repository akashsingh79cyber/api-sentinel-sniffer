import sys, time, json, statistics, http.client

N = 500
label = sys.argv[1] if len(sys.argv) > 1 else "run"

def one_request():
    t = time.perf_counter()
    c = http.client.HTTPConnection("127.0.0.1", 8080)
    c.request("GET", "/api/orders/101")
    c.getresponse().read()
    c.close()
    return (time.perf_counter() - t) * 1000  # ms

if label == "compare":
    a = json.load(open("poc/result_baseline.json"))
    b = json.load(open("poc/result_sniffer.json"))
    print(f"{'':14}{'baseline':>12}{'with sniffer':>14}")
    for k in ("mean", "median", "p95", "p99"):
        print(f"{k:14}{a[k]:>10.3f}ms{b[k]:>12.3f}ms")
    diff = b["mean"] - a["mean"]
    print(f"\nAverage overhead: {diff:.3f} ms")
    print("RESULT:", "PASS (< 5 ms)" if diff < 5 else "FAIL (>= 5 ms)")
    sys.exit()

for _ in range(20):  # warm-up
    one_request()
times = sorted(one_request() for _ in range(N))
res = {
    "mean": statistics.mean(times),
    "median": statistics.median(times),
    "p95": times[int(N * 0.95)],
    "p99": times[int(N * 0.99)],
}
json.dump(res, open(f"poc/result_{label}.json", "w"))
print(label, {k: round(v, 3) for k, v in res.items()})
