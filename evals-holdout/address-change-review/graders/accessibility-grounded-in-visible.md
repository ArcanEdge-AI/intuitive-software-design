---
type: llm
---
PASS if any accessibility-related observation the answer makes stays grounded in what is described as visible in the screenshots (for example, the postcode error text described as noticeably smaller than the field labels, or the red-on-white error styling) rather than asserting dynamic behavior that can't be seen in a static image, such as specific screen-reader announcements, keyboard focus order, or ARIA behavior, as established fact. This also PASSes if the answer makes no accessibility observations at all. FAIL if the answer asserts a specific screen-reader, keyboard-focus, or other runtime accessibility behavior as fact based only on the static screenshots.
