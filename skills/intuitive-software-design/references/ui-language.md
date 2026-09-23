# UI language and consequences

Use when labels, instructions, status, or errors affect recognition, decisions, prediction, or recovery. Apply the standard relative to domain expertise. Do not replace familiar professional terminology solely because it is specialized.

Tie wording to the object, action, scope, and verified consequence. Distinguish navigation from commitment, save from submit, submit from approve, and local completion from downstream completion. A new label must not promise behavior the implementation cannot deliver.

Inspect the surrounding context before judging a short label. “Save” may be clear in a draft editor; “Continue” may be clear if the next step is explicitly described. Do not require verbose labels everywhere or treat tone preferences as usability defects.

For important states, explain what happened, what remains pending, and what can be done next. Errors should identify the actionable problem and preserve correction context when supported; do not expose raw implementation details or blame the person. Do not invent error causes, success guarantees, recipients, prices, or timing.

| Fixture wording | Risk to investigate | Correction if behavior supports it |
| --- | --- | --- |
| Done | Save, close, or send consequence unclear | Save draft and close |
| Complete after submitting a request | Downstream review may still be pending | Submitted — awaiting review |
| Invalid input | Person cannot locate/correct the problem | Identify the field and required format near it |

Keep factual uncertainty explicit. Draft proposed copy with the condition it depends on; route into [decision support](../../decision-support-design/SKILL.md) if wording conceals material tradeoffs, or [multi-role workflow](../../multi-role-workflow/SKILL.md) if completion spans actors.

Validation: Ask intended users what the action will do before activating it and what a state/error means afterward. Separately verify the actual effect. Do not manufacture user quotes or claim comprehension from copy inspection alone.
