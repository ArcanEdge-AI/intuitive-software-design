# Intuitive Software Design Examples

These examples teach the standard; they are not universal component prescriptions. Always adapt them to the intended user, task, consequence, and evidence.

## 1. Orientation — configuration scope

### Before

```text
Settings

Notifications   Permissions   Defaults
[ Save ]
```

### After

```text
ACME HOSPITAL / ESTIMATE 1042
Pricing settings

Labor default      Commercial crew ▼
Markup             18%

Unsaved changes                         [ Save pricing settings ]
```

### Why the second is more intuitive

- object and configuration scope are visible;
- the action names the consequence;
- changed state is visible;
- the user need not reconstruct the navigation path.

### Standard mapping

UI Orientation; Recognition; Interpretation and Memory Friction; Context preservation.

## 2. Prediction — vague completion action

### Before

```text
Proposal editor

[ Cancel ]                         [ Done ]
```

The control closes the editor, saves the draft, and sometimes sends it when an `Auto-send` preference is enabled elsewhere.

### After

```text
Proposal editor

Saved 2:41 PM
[ Close ]              [ Save draft ]  [ Review and send ]
```

### Why the second is more intuitive

- each action has a predictable consequence;
- saved state is visible;
- sending remains a distinct high-consequence step;
- the hidden preference no longer creates a large Prediction Gap.

### Standard mapping

Feel Predictability; Predict; Interpretation Friction; Critical Failure candidate when sending is binding.

## 3. Direct interaction — team role

### Before

```text
Project
  ⋮
  Manage
    Project configuration
      Personnel
        John Smith
          Edit
            Role
```

### After

```text
PROJECT TEAM

John Smith       Foreman ▼
Maria Lopez      Carpenter ▼

+ Add team member
```

### Why the second is more intuitive

- relevant objects and current state are visible;
- actions are located next to affected objects;
- fewer unrelated transitions are required;
- consequences are easier to predict.

### Design boundary

If role changes alter payroll, access, or legal responsibility, keep the direct entry point but add a proportionate explanation/confirmation or focused permission flow.

## 4. Feedback — proposal sending

### Before

```text
[ Send proposal ]
```

After activation the button remains unchanged for eight seconds. The user is returned to the list with no durable status.

### After

```text
[ Sending… ]

Proposal sent to bids@acme.example at 2:43 PM  ✓
[ View proposal ]  [ Copy link ]
```

Failure:

```text
Proposal was not sent. Your draft is preserved.
Connection timed out. [ Try again ]  [ Save draft ]
```

### Why the second is more intuitive

- immediate acknowledgment prevents duplicate activation;
- pending, success, and failure are distinct;
- the result names what happened;
- recovery preserves work and makes continuation clear.

### Standard mapping

Feel Feedback; Confirm and Continue; Feedback and Recovery Friction; Critical Failure candidate for consequential sending.

## 5. Recognition over recall — estimate to scope

### Before

```text
Step 2: Scope

Type __________
Area __________
```

The user must remember the customer, estimate type, and building area selected on the previous screen.

### After

```text
ESTIMATE 1042 / ACME HOSPITAL
Commercial renovation · 42,000 sq ft
Step 2 of 4 — Define scope

Scope type       ▼
Included areas   ▼
```

### Why the second is more intuitive

- previous choices carry forward;
- current object and progress remain visible;
- options can be contextualized to the chosen estimate type;
- backtracking and memory work decrease.

## 6. Progressive disclosure and Decision Density

### Before

```text
NEW PROJECT

Name
Customer
Project type
Project subtype
Billing method
Workflow
Labor model
Markup
Tax configuration
Location profile
Crew type
Notification policy

[ Create ]
```

### After

```text
NEW PROJECT

Name        __________
Customer    __________
Type        ▼

Defaults: Standard workflow · Customer tax profile
[ Review settings ]

[ Create project ]
```

After creation, labor, crew, and workflow choices appear when scope and team information make them meaningful.

### Why the second is more intuitive

- only necessary creation decisions are required now;
- consequential defaults are summarized, not hidden;
- additional settings remain discoverable;
- decisions appear with better information.

### Design boundary

Do not defer a choice if work becomes unsafe, invalid, unexpectedly billed, or costly before the user sees it.

## 7. Error recovery — preserved work

### Before

```text
Error: invalid request.

[ Back ]
```

All 18 entered fields are cleared.

### After

```text
We could not create the project yet. Your entries are preserved.

2 fields need attention:
- Start date must be on or after August 25. [ Go to Start date ]
- Customer billing profile is inactive. [ Choose another profile ]

[ Review fields ]
```

### Why the second is more intuitive

- cause and location are specific;
- valid work remains;
- recovery actions correspond to each cause;
- retry does not risk duplicate creation.

## 8. Navigation — contextual action

### Before

```text
Project detail -> Administration -> People -> Assignments
```

The user leaves the project and must search for it again in a global assignment screen.

### After

```text
Project detail / Team

+ Assign team member
```

The assignment picker is already scoped to the project and returns to the same Team view.

### Why the second is more intuitive

- the entry point appears at the moment of need;
- project context is preserved;
- system administration no longer dictates the job flow;
- return location is predictable.

## 9. Minimal but cognitively complex

### Before

```text
Project 1042

✦    ◇    ↗
```

The icons mean calculate, duplicate, and send. None has a visible label.

### After

```text
Project 1042

[ Recalculate ]  [ Duplicate ]  [ Send proposal ]
```

On narrow screens, the two lower-frequency actions may move into a clearly labeled `More actions` menu while `Send proposal` remains visible.

### Why the second is more intuitive

- visual simplicity no longer creates interpretation work;
- actions and consequences can be recognized;
- priority remains clear across viewport sizes;
- cognitive simplicity takes precedence over icon minimalism.

## 10. Dense expert interface

### Deliberately dense screen

```text
CREW SCHEDULE — WEEK 35

Filters: Region [North] Trade [All] Status [At risk]
Rows: 42 crews × 7 days, color + text status, utilization %, conflicts
Keyboard: J/K navigate · E edit · Shift+S assign · ? shortcuts
Saved view: Superintendent morning review
```

### Correct evaluation

Do not penalize the screen because it contains many rows, abbreviations, or expert shortcuts. Evaluate:

- whether dispatchers recognize the grid and domain terms;
- whether hierarchy separates conflicts from routine work;
- whether state is not color-only;
- whether shortcuts are discoverable and visible actions remain available;
- whether edits preserve week, filters, selection, and scroll position;
- whether assignment results and conflicts are confirmed.

### Possible legitimate finding

If selecting a crew silently resets the region filter and scroll position, that is Context/Memory Friction and a Feel inconsistency. “Reduce the number of rows” is not supported by that evidence.

## 11. Beginner-to-expert progression

### Before

```text
Save is available only as Ctrl/Cmd+S.
```

### After

```text
[ Save ]
Shortcut shown in tooltip/menu: Ctrl/Cmd+S
Saved view and bulk-save patterns available to frequent users.
```

### Why the second is more intuitive

- beginners can recognize the action;
- the shortcut becomes discoverable;
- expert efficiency grows without removing the visible path;
- the system supports mastery rather than choosing one audience.

## 12. Smallest complete improvement

### Diagnosis

The existing proposal screen is clear, but sending provides no pending, success, failure, or durable sent state.

### Incomplete “small” change

Show a green toast saying `Sent`.

### Smallest complete change

Keep the layout and button. On activation:

1. change the action to `Sending…` and prevent duplicate activation;
2. on success, show `Sent` with recipient and time in durable proposal state;
3. on failure, state that sending failed, preserve the draft, and expose safe retry;
4. ensure the result is semantically announced;
5. keep `View proposal` as continuation.

### Why this is the standard's preferred improvement

It fixes the complete feedback contract without redesigning the screen, introducing a new navigation layer, or changing behavior that already works.
