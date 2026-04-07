# Homework 2 - Customer Support Response Drafting

## Overview

This project builds a simple GenAI workflow that drafts customer support email responses for a SaaS company. Given a customer complaint or inquiry, the system generates a professional, empathetic response draft that a support agent can review and send.

## Business Workflow

- **Workflow:** Drafting customer support responses
- **User:** Customer support agents at a SaaS company
- **Input:** Customer email/message describing an issue or question
- **Output:** A professional draft response ready for human review
- **Why automate:** Support agents handle 50-100 tickets per day. Drafting responses is repetitive and time-consuming. An LLM can produce a solid first draft in seconds, letting agents focus on accuracy and personalization rather than composing from scratch.

## Setup

```bash
pip install google-generativeai
export GEMINI_API_KEY="your-api-key-here"
python app.py
```

## Files

- `app.py` - Main application script
- `prompts.md` - Prompt versions and iteration notes
- `eval_set.json` - Evaluation test cases
- `report.md` - Final report

## Video Walkthrough

_Link will be added after recording._
