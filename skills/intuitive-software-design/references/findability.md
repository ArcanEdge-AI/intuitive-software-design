# Navigation and findability

Use when a person must locate an object, action, or answer. Apply the standard's orientation, recognition, mental-model, and navigation-friction principles. The question is whether the available cues suggest a useful destination before activation.

Start at the actual entry point with the intended person's vocabulary and knowledge. Inspect labels, surrounding context, grouping, hierarchy, search/filter affordances, and current-location cues. Trace a plausible path using [User-Task Walkthrough](../../user-task-walkthrough/SKILL.md). Do not prove findability by directly opening a route learned from code.

Look for ambiguous siblings, inconsistent names, categories that mix objects and actions, misleading link promises, and information that exists but has no visible route. Judge search against the terms users can reasonably know; do not assume they know identifiers or internal entity names. A path with more steps can be clearer than a shorter path that requires guessing.

Fixture: An invoice is reachable under both Billing and Documents. That is not inherently a defect. Check whether either label/context gives a reliable path for the relevant user and whether the destinations agree. If Documents contains only uploaded files, using that label for generated invoices may create a mismatch; verify the actual contents first.

Recommend the smallest supported correction: clearer destination wording, contextual access, improved grouping, or relevant search cues. Do not automatically add a global navigation item or flatten the hierarchy. Preserve alternate paths that serve distinct legitimate tasks.

Validation: Ask intended users to find the needed object or answer without naming the menu. Record first choices, wrong turns, recovery, and whether they recognize the destination. A tree test can isolate label/grouping questions; it does not validate rendered controls or full runtime behavior. Agent navigation success is functional evidence, not a human findability result.
