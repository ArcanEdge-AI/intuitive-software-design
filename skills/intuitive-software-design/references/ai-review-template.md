# AI-Agent Intuitive Software Review Template

Use this when a coding or review agent evaluates source, screenshots, runtime software, prototypes, or a written design. Be concise for ordinary reviews; keep the full shape for formal audits.

## Instructions to the reviewing agent

1. Infer the intended user and task from available evidence when reasonable. Ask only if a missing fact materially changes the evaluation.
2. State evidence type and limitations. Source code is evidence of an implemented path, not proof of rendered or observed behavior. A screenshot is not proof of interaction, recovery, or accessibility operation.
3. Classify the request as `DESIGN`, `REVIEW`, `AUDIT`, or `IMPROVE`.
4. Evaluate relative to the intended user, including relevant domain expertise.
5. Separate UI, Flow, and Feel.
6. Locate Loop breaks, Prediction Gaps, Decision Density, friction types, severity, and Critical Failures.
7. Use 0–4 scores only when evidence supports the full criterion; otherwise use `NE`.
8. Prefer the smallest complete change. Preserve effective behavior and avoid aesthetic modernization.

## Output

### Evaluation frame

```text
Mode:
Intended user:
Task:
Starting point:
Success condition:
Evidence:
Not evaluated:
```

### Diagnosis

```text
Primary weakness:
Major friction:
Earliest Loop break:
Critical Failures:
```

### Strengths to preserve

- [specific observed strength]

### Findings

Use one block per material finding:

```text
Finding:
[specific observable problem]

Area:
UI | Flow | Feel | Cross-Cutting

Principle:
[standard principle]

Friction Type:
Navigation | Interpretation | Decision | Interaction | Memory | Feedback | Recovery | Process

Loop Break:
Orient | Recognize | Predict | Act | Confirm | Continue

Evidence:
[file/symbol, screenshot region, runtime step, spec passage, or observation]

User Impact:
[reasoned effect on the intended user and task; label inference when not observed]

Severity:
Critical | High | Medium | Low

Score:
[criterion and 0–4, or NE]

Recommendation:
[smallest complete corrective change, including relevant pending/failure/recovery states]

Expected Outcome:
[observable behavior that should become easier or more predictable]

Validation:
[test or evidence that would prove the result]
```

### Scorecards

Include only requested/supported scorecards. For each criterion include score or `NE` plus an evidence sentence. State evaluated coverage and never average Critical Failures.

### Improvement sequence

```text
1. [critical containment or task blocker]
2. [foundational change resolving multiple findings]
3. [remaining high-frequency friction]
```

For each item state what remains unchanged.

### Evidence gaps

- [missing runtime state, user role, device, failure path, keyboard behavior, assistive-technology behavior, or representative workflow]

## Review quality gate

Reject or revise the output if it:

- says only “improve feedback,” “simplify,” “make modern,” or another generic instruction;
- treats density or domain terminology as a defect without intended-user evidence;
- assumes minimal UI is cognitively simple;
- invents a user result or score;
- hides a Critical Failure inside a high average;
- proposes a redesign when a smaller complete correction addresses the evidence;
- omits failure/recovery from a change whose operation can fail;
- cannot trace a recommendation back to specific evidence and a standard principle.
