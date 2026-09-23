# Promise-to-product continuity — raw fixture

## Task

Review whether the supplied product promise is fulfilled by the first relevant task across desktop and mobile. State what the evidence establishes, what must not be generalized, and a proportionate correction and validation. No live actions or implementation.

## Artifacts

- Public product page: “Create a quote anywhere. Pick up the same quote on any device.”
- Authorized desktop test trace: a signed-in user creates quote `Q-104`, saves it as Draft, sees “Quote saved,” and reopens it from the desktop quote list.
- Authorized mobile test trace: the same test account and workspace sign in to the mobile app. Its quote list does not contain `Q-104`; no mobile deep link or recent-items entry is available.
- Source inspection: desktop posts saved quotes to the shared quotes API. The mobile quote list reads from a device-local `local_quotes` store and has no call to the shared quotes API. No test was supplied for importing a quote or changing platforms after a mobile-created quote.
- The traces use one test account and one quote. No human usability session, production incidence, retention metric, or permission review was supplied.

The expected task is to continue editing the same saved quote on mobile. The evidence does not establish behavior for every account, quote type, or platform version.
