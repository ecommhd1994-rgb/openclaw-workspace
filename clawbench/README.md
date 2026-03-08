# clawbench

A minimal CLI tool for benchmarking AI model response latency.

## What It Does

Sends a prompt to an AI API multiple times, measures response time for each request, and reports average/median/min/max latency statistics.

## Installation

```bash
git clone https://github.com/yourorg/clawbench.git
cd clawbench
pip install requests
chmod +x clawbench.py
```

## Usage

```bash
python clawbench.py \
  --api-url "https://api.example.com/v1/chat/completions" \
  --api-key "your-api-key" \
  --model "gpt-4" \
  --prompt "Write a short story" \
  --runs 10
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--api-url` | API endpoint URL | (required) |
| `--api-key` | API authentication key | (required) |
| `--model` | Model name to test | (required) |
| `--prompt` | Prompt to send | "Hello, world!" |
| `--runs` | Number of benchmark runs | 5 |

## Example Output

```
🤖 clawbench - Benchmarking gpt-4
   Prompt: Write a short story
   Runs: 5

  Run 1/5: 1.234s
  Run 2/5: 1.198s
  Run 3/5: 1.312s
  Run 4/5: 1.089s
  Run 5/5: 1.256s

📊 Results (5 successful runs):
   Mean:   1.218s
   Median: 1.234s
   Min:    1.089s
   Max:    1.312s
   StdDev: 0.082s
```

## License

MIT
