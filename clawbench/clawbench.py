#!/usr/bin/env python3
"""
clawbench - AI Model Latency Benchmarking Tool

Usage:
    clawbench --api-url <url> --api-key <key> --model <model> [--prompt <text>] [--runs <n>]
"""

import argparse
import time
import statistics
import json
import sys

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


def run_benchmark(api_url: str, api_key: str, model: str, prompt: str, runs: int) -> list:
    """Execute benchmark requests and return latencies in seconds."""
    latencies = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    for i in range(runs):
        try:
            start = time.perf_counter()
            resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
            elapsed = time.perf_counter() - start
            
            if resp.status_code == 200:
                latencies.append(elapsed)
                print(f"  Run {i+1}/{runs}: {elapsed:.3f}s")
            else:
                print(f"  Run {i+1}/{runs}: ERROR {resp.status_code} - {resp.text[:100]}")
        except Exception as e:
            print(f"  Run {i+1}/{runs}: FAILED - {e}")
    
    return latencies


def main():
    parser = argparse.ArgumentParser(description="clawbench - AI Model Latency Benchmark")
    parser.add_argument("--api-url", required=True, help="API endpoint URL")
    parser.add_argument("--api-key", required=True, help="API authentication key")
    parser.add_argument("--model", required=True, help="Model name to benchmark")
    parser.add_argument("--prompt", default="Hello, world!", help="Prompt to send")
    parser.add_argument("--runs", type=int, default=5, help="Number of benchmark runs")
    
    args = parser.parse_args()
    
    print(f"\n🤖 clawbench - Benchmarking {args.model}")
    print(f"   Prompt: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    print(f"   Runs: {args.runs}\n")
    
    latencies = run_benchmark(args.api_url, args.api_key, args.model, args.prompt, args.runs)
    
    if latencies:
        print(f"\n📊 Results ({len(latencies)} successful runs):")
        print(f"   Mean:   {statistics.mean(latencies):.3f}s")
        print(f"   Median: {statistics.median(latencies):.3f}s")
        print(f"   Min:    {min(latencies):.3f}s")
        print(f"   Max:    {max(latencies):.3f}s")
        if len(latencies) > 1:
            print(f"   StdDev: {statistics.stdev(latencies):.3f}s")
    else:
        print("\n❌ No successful runs completed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
