# promptinspector

A CLI tool for evaluating and comparing AI prompts.

## What It Does

- Load multiple prompts from a JSON file
- Send each to an AI API and capture responses
- Compare outputs using an LLM-as-judge (optional)
- Save results to JSON

## Installation

```bash
git clone https://github.com/yourorg/promptinspector.git
cd promptinspector
pip install requests
chmod +f promptinspector.py
```

## Usage

Prepare a prompts JSON file:

```json
{
  "prompt-name": {
    "system": "Optional system prompt",
    "prompt": "User prompt text"
  }
}
```

Run evaluation:

```bash
python promptinspector.py \
  --api-url "https://api.example.com/v1/chat/completions" \
  --api-key "your-key" \
  --prompts example_prompts.json \
  --model "gpt-4" \
  --judge
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--api-url` | API endpoint | (required) |
| `--api-key` | API key | (required) |
| `--prompts` | JSON file with prompts | (required) |
| `--model` | Model to use | gpt-4 |
| `--judge` | Enable LLM-judged comparison | false |

## Output

Results saved to `results.json` with structure:

```json
{
  "prompt-name": {
    "output": "model response...",
    "usage": {"prompt_tokens": 10, "completion_tokens": 50}
  }
}
```

## License

MIT
