# Worked examples

These are illustrative fixtures, not research results. Each separates what the evaluator knows from what the intended user can know.

## Website: compare before enquiring

**Frame:** An owner arrives from search at an agency's services page to decide whether it suits a website project. No prior brand knowledge is assumed. Success is enough information to decide whether to enquire; a reasoned decision not to proceed can also meet the goal.

**Fixture evidence:** A page screenshot shows “Website development” and a “Start your transformation” button. No scope, delivery process, examples, or destination description appears in the supplied viewport. Source inspection says the button opens an enquiry form; other page sections are unavailable.

| Step and intent | Knowledge and visible clue | Prediction | Result and evidence | Gap |
| --- | --- | --- | --- | --- |
| Establish fit | Service heading identifies a broad category | The service might address the project; fit remains uncertain | Heading observed in screenshot | Scope and process are unknown outside the viewport |
| Decide whether to enquire | Vague action label provides no destination cue | Could start a form, booking, or purchase; this is an inference | Form destination is source-supported, not runtime-tested | The person has not received the agent's destination knowledge |

**Correction hypothesis:** If the full page confirms the gap, explain relevant scope/process near the decision and give the enquiry action a concrete consequence such as “Discuss your website project.” Preserve existing useful evidence elsewhere instead of duplicating it automatically.

**Validation:** Inspect the full page first. Ask likely users whether the agency suits their project and what they expect the action to do, without instructing them to click it. Functional verification separately checks the destination. Do not claim every visitor should convert.

## Application: save a draft without sending

**Frame:** A daily estimator uses this product for the first time, edits a proposal, and wants to keep a draft for tomorrow without notifying a client. Domain expertise is justified; knowledge of this product's hidden behavior is not.

**Fixture evidence:** The editor shows “Done.” Source inspection says its handler saves and closes. A runtime trace shows a click closing the editor and a “Saved” toast; reopening has not been tested.

**Prediction gap:** “Done” leaves save/close/send consequences ambiguous. That ambiguity is an inference about the intended user, not an observed mistake. Agent inspection of the handler does not resolve the visible ambiguity for the person.

**Observation:** The exercised action closed the editor and displayed a toast. The source supports a save path. Persisted content, later retrieval, failed-save handling, and whether any external notification occurred are not proven by that trace alone.

**Correction hypothesis:** Use an action label that matches the verified consequence, such as “Save draft and close,” and show pending and failure behavior that preserves edits. Do not promise “not sent” until downstream behavior supports it. Preserve familiar estimating terminology and efficient expert editing.

**Validation:** In an authorized test environment, save, reopen, and compare the edited fields; verify any notification effects separately. Exercise a supported save failure and correction path when feasible. A human task is “Keep this proposal so you can finish tomorrow without sending it.” Observe how the person chooses and recognizes completion; do not name the button in the prompt.

## Interruption: return to unfinished work

**Frame:** A manager compares three records, opens one, and later returns to the comparison. The important knowledge includes the selected records and prior filter, not every detail on the screen.

**Fixture evidence:** A screenshot of the returned list shows no selection. There is no before-state capture or runtime navigation trace.

**Boundary:** Selection loss is unknown. The screenshot cannot establish whether selection ever existed, whether this is the same task, or whether restoration is intended. Do not diagnose a confirmed reset.

**Next evidence:** Compare before/after state through the actual entry and return path with an authorized fixture. If loss is demonstrated and selection is needed to continue, classify Memory/Process friction and propose preserving or explicitly recovering that context. If durable resume is unnecessary, a smaller clear return path may suffice.
