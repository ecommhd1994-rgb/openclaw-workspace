#!/usr/bin/env python3
"""
promptinspector - Evaluate and compare AI prompts

Usage:
    promptinspector --api-url <url> --api-key <key> --prompts <file> [--model <model>]
"""

import argparse
import json
import sys
import os

try:
    import requests
except ImportError:
    print("Error: requests required. Install: pip install requests")
    sys.exit(1)


def load_prompts(path: str) -> dict:
    """Load prompts from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def evaluate_prompt(api_url: str, api_key: str, model: str, system: str, user: str) -> dict:
    """Send prompt to API and return response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": []
    }
    if system:
        payload["messages"].append({"role": "system", "content": system})
    payload["messages"].append({"role": "user", "content": user})
    
    resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "success": True,
            "content": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
            "usage": data.get("usage", {})
        }
    else:
        return {"success": False, "error": resp.text}


def run_evaluator(api_url: str, api_key: str, model: str, prompts: dict, judge: bool = False):
    """Evaluate all prompts and optionally judge outputs."""
    results = {}
    
    for name, prompt_data in prompts.items():
        system = prompt_data.get("system", "")
        user = prompt_data.get("prompt", prompt_data.get("user", ""))
        
        print(f"\n🔍 Evaluating: {name}")
        if system:
            print(f"   [System: {system[:50]}...]")
        
        result = evaluate_prompt(api_url, api_key, model, system, user)
        
        if result["success"]:
            content = result["content"]
            print(f"   ✅ Output ({len(content)} chars): {content[:100]}...")
            results[name] = {
                "output": content,
                "tokens": result["usage"]
            }
        else:
            print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
            results[name] = {"error": result.get("error")}
    
    # Optional: LLM-as-judge comparison
    if judge and len(results) > 1:
        print("\n⚖️ Running LLM-judged comparison...")
        compare_prompt = (
            "Compare the following prompt outputs and rate them 1-10 for helpfulness and accuracy.\n\n"
        )
        for name, data in results.items():
            if "output" in data:
                compare_prompt += f"--- {name} ---\n{data['output'][:500]}\n\n"
        compare_prompt += "\nProvide scores and brief reasoning."
        
        judge_result = evaluate_prompt(api_url, api_key, model, "", compare_prompt)
        if judge_result["success"]:
            print(f"\n📝 Judge Output:\n{judge_result['content']}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="promptinspector - Evaluate AI prompts")
    parser.add_argument("--api-url", required=True, help="API endpoint URL")
    parser.add_argument("--api-key", required=True, help="API key")
    parser.add_argument("--prompts", required=True, help="JSON file with prompts")
    parser.add_argument("--model", default="gpt-4", help="Model to use")
    parser.add_argument("--judge", action="store_true", help="Enable LLM-judged comparison")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.prompts):
        print(f"Error: File not found: {args.prompts}")
        sys.exit(1)
    
    prompts = load_prompts(args.prompts)
    
    print(f"🤖 promptinspector - Evaluating {len(prompts)} prompt(s)")
    print(f"   Model: {args.model}")
    
    results = run_evaluator(args.api_url, args.api_key, args.model, prompts, args.judge)
    
    # Save results
    output_file = "results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    main()
