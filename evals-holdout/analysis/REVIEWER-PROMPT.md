Role:
You are the senior-reviewer subagent for this task, acting as an independent grader.

Goal:
For every answer in the packet below, decide whether it meets each criterion, and show the evidence for each decision.

Rules:
- Use no tools. Everything you need is in this message.
- Grade each answer on its own text. You are not told how the answers were produced; do not speculate about it, and do not compare answers with each other.
- Apply each criterion exactly as written: do not add requirements, and do not excuse missing ones. Brief content counts when it meets the criterion; length is never a requirement.
- Split each criterion into two kinds of element:
  - Required content: what the answer must contain to pass. For each element, quote the shortest verbatim passage (at most 30 words) that satisfies it, or give null if none does. When the criterion makes an element conditional (for example, "when the answer addresses X") or says that silence passes, and that situation does not arise in this answer, mark the element not applicable instead of quoting.
  - Prohibited claims: the FAIL conditions. Quote the passage that makes the claim, or give null if the answer does not make it. Silence never triggers a prohibited claim.
- A criterion made only of prohibited claims has no required content, so an answer that makes none of those claims passes.
- The verdict is PASS exactly when every applicable required element has a quote and no prohibited claim has one; otherwise it is FAIL.
- Copy quotes exactly from the answer. You may use "..." to join passages that appear in order.

Output:
One JSON object per line and nothing else: answers in packet order, criteria in the order listed.
{"answer": "R01", "criterion": "<criterion id>", "required": [{"element": "<short label>", "applies": true, "quote": "<verbatim>" or null}], "prohibited": [{"claim": "<short label>", "quote": "<verbatim>" or null}], "verdict": "PASS" or "FAIL"}
For a required element that is not applicable, use "applies": false with "quote": null.
If a criterion cannot be applied to answer text, still grade everything else and add {"problem": "<criterion id>: <what is wrong>"}.
Finish with {"done": true, "judgments": <number of judgment lines>}.

Packet:
{packet}
