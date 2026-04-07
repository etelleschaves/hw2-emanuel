"""
Customer Support Response Drafting Tool

Generates professional support response drafts using Google Gemini.
Usage: python app.py [--eval] [--input "customer message"]
"""

import argparse
import json
import os
import sys

import google.generativeai as genai


SYSTEM_PROMPT = """\
You are a professional customer support agent for a SaaS company called "CloudSync."
Your job is to draft helpful, empathetic, and accurate email responses to customer inquiries.

Guidelines:
- Start with a warm greeting using the customer's name if provided, otherwise use "Hi there."
- Acknowledge the customer's issue or emotion before jumping to solutions.
- Provide clear, actionable steps when possible.
- If you do not know specific details (pricing, internal policies, what another agent said), do NOT make them up. Instead, say you will check with the relevant team and follow up.
- Keep responses concise (under 150 words) but thorough.
- End with an offer to help further and a professional sign-off.
- Use a friendly but professional tone throughout.
- Never blame the customer.
"""


def generate_response(model, customer_message):
    """Send a customer message to Gemini and return the drafted response."""
    chat = model.start_chat()
    response = chat.send_message(
        f"Draft a support response for this customer message:\n\n{customer_message}"
    )
    return response.text


def run_eval(model, eval_path="eval_set.json"):
    """Run the model against all evaluation cases and print results."""
    with open(eval_path) as f:
        eval_cases = json.load(f)

    results = []
    for case in eval_cases:
        print(f"\n{'='*60}")
        print(f"Case {case['id']} ({case['type']})")
        print(f"{'='*60}")
        print(f"INPUT: {case['input'][:100]}...")
        print(f"EXPECTED: {case['expected'][:100]}...")
        print("-" * 60)

        response = generate_response(model, case["input"])
        print(f"OUTPUT:\n{response}")
        results.append({
            "id": case["id"],
            "type": case["type"],
            "input": case["input"],
            "expected": case["expected"],
            "output": response,
        })

    output_path = "eval_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")


def run_single(model, message):
    """Generate a single response and print it."""
    print("\n--- Customer Message ---")
    print(message)
    print("\n--- Draft Response ---")
    response = generate_response(model, message)
    print(response)


def main():
    parser = argparse.ArgumentParser(description="Customer Support Response Drafter")
    parser.add_argument("--eval", action="store_true", help="Run against evaluation set")
    parser.add_argument("--input", type=str, help="Single customer message to respond to")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash",
                        help="Gemini model to use (default: gemini-2.0-flash)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Set the GEMINI_API_KEY environment variable.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=args.model,
        system_instruction=SYSTEM_PROMPT,
    )

    if args.eval:
        run_eval(model)
    elif args.input:
        run_single(model, args.input)
    else:
        print("Usage:")
        print('  python app.py --input "Your customer message here"')
        print("  python app.py --eval")
        sys.exit(1)


if __name__ == "__main__":
    main()
