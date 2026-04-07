# Report: Customer Support Response Drafting with GenAI

## Business Use Case

Customer support agents at SaaS companies handle dozens of tickets daily, many of which follow predictable patterns: billing questions, how-to inquiries, feature requests, and bug reports. Writing professional, empathetic responses from scratch for each ticket is time-consuming and repetitive. This prototype automates the first-draft stage: given a customer message, it generates a polished response draft that an agent can review, personalize, and send. The goal is to reduce response time and improve consistency, not to replace human judgment.

## Model Choice

I used **Google Gemini 2.0 Flash** via the `google-generativeai` Python SDK. I chose Gemini for three reasons:

1. **Free API access** through Google AI Studio, making it accessible for prototyping.
2. **Fast inference** - Flash models return responses in under 2 seconds, which matters for a tool agents would use in real time.
3. **Strong instruction following** - Gemini reliably adhered to system prompt constraints like word limits and the "don't fabricate" rule after prompt tuning.

I did not test other providers for this assignment, but the architecture is model-agnostic: swapping in OpenAI or Anthropic would require only changing the API client and model name.

## Baseline vs. Final Design

### Baseline (V0)
The initial prompt was minimal: "You are a customer support agent. Write a professional response. Be helpful and polite." Results were:
- **Too long**: Responses averaged 200+ words with filler phrases.
- **Hallucination-prone**: The model invented specific pricing ($29/month for Pro, $99/month for Enterprise) when asked about plans.
- **Confirmed unverifiable claims**: When told "agent Sarah promised a 30% discount," the model played along.
- **Structure inconsistent**: Some responses opened with solutions, others with apologies.

### Final (V2)
After two prompt revisions, the system prompt includes company context, structured guidelines, a 150-word limit, and explicit instructions not to fabricate unknown details. Results:
- **Concise**: Responses consistently stayed under 150 words.
- **No fabrication**: Pricing and compliance questions were redirected to the sales/pricing team.
- **Consistent structure**: Every response follows greeting > acknowledgment > action > sign-off.
- **Edge cases handled well**: Gibberish input gets a polite clarification request; angry messages are de-escalated without defensiveness.

The biggest improvement came from the anti-hallucination instruction in V1. The word limit in V2 was the second most impactful change.

## Where the Prototype Still Fails

The system still requires human review in several areas:

- **Technical troubleshooting**: When customers describe specific bugs, the model suggests generic steps (clear cache, restart) rather than diagnosing the actual issue. A real agent would check internal dashboards or escalate to engineering.
- **Account-specific actions**: The model cannot look up a customer's actual account, subscription status, or payment history. It can only write generically about "checking your account."
- **Tone calibration for escalated customers**: While V2 handles angry messages reasonably, truly hostile or threatening messages may need a different escalation path that the model cannot determine on its own.
- **Legal and compliance claims**: The model correctly avoids fabricating compliance certifications, but a human must still verify any claims before sending.

## Deployment Recommendation

I would recommend deploying this as a **draft-assistance tool** with mandatory human review, not as an autonomous responder. Specifically:

- **Yes, deploy** as a first-draft generator inside the support agent's workflow (e.g., a sidebar tool in Zendesk or Intercom). Agents would see the draft, edit as needed, and send.
- **Do not deploy** as an auto-responder or chatbot without a human in the loop. The risk of fabricating details or misjudging tone in edge cases is too high for unreviewed customer communication.
- **Conditions**: The system should log all generated drafts alongside final sent messages so the team can audit quality over time. Prompt updates should be versioned and tested against the evaluation set before deployment.

This prototype demonstrates that LLMs can meaningfully accelerate support workflows, but the value comes from augmenting human agents, not replacing them.
