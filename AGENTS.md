# Local AGENTS Instructions

## Priority
- This file overrides global agent guidance for this project.
- Follow this fork workflow first:
  1. `main` is reserved for syncing upstream.
  2. Custom development must happen on `custom` or `feature/*`.
  3. Upstream contributions should come from a clean `feature/*` branch based on `main`.

## Repository Workflow
- `origin` = this fork repository.
- `upstream` = original repository: `ztx888/HaloWebUI`.
- Keep `main` as close as possible to upstream `main`.
- Do **not** make direct feature/custom edits on `main`.
- Long-term fork customization belongs on `custom`.
- Isolated work belongs on `feature/*`.
- If a change may be contributed upstream, keep it minimal and separate from fork-only customization.

## Task Log
- Do not read from or write to parent-folder log directories; parent folders are storage containers, not this project's log center.
- Follow project-local `TASK.md` for current handoff and `LOG.md` for concise history.
- Keep `TASK_LOG.md` as the legacy long-form history file; read it only when older detail is needed.
- Before larger edits, add or update a task entry.
- After finishing, record:
  - what changed
  - affected files
  - whether the change is fork-only or suitable for upstream PR
  - any sync/merge risk with upstream

## MCP Usage
- Prefer local MCP tools first.
- External MCP / external services may be used when helpful for verification or coverage.
- Keep external calls minimal in scope.
- Record the reason and outcome in responses.

## External Tool Log Format
- Format:
  - `服务: <name> | 触发: <reason> | 参数: <key args> | 结果: <summary> | 状态: <success|fail>`

## Issue Screening Scope
- Do not browse or triage broad upstream issues by default.
- Only inspect issues when the user explicitly asks, or when a failing local test/bug points to a matching upstream issue.
- When issue review is needed, keep it limited to this fork's six active lines:
  - provider/interface configuration
  - model inheritance
  - MCP inheritance
  - tool and skill state
  - new/old chat send state
  - native web search and Responses behavior
- Exclude unrelated product ideas, branding, migration docs, logo work, image-only issues, performance ideas, and broad upstream backlog unless the user names them.
- Prefer local reproduction and tests before treating any upstream issue as actionable.

## Change Strategy
- Prefer **minimal diff** changes.
- Prefer **additive / wrapper / extension** changes over rewriting upstream core files.
- Avoid broad refactors unless explicitly requested.
- When changing shared/core files, clearly note possible future merge conflicts.
- Preserve existing license, attribution, and upstream identity.

## Codex Working Rules
- Codex should work only in the current checked-out branch.
- Prefer working in:
  - `custom` for long-term fork features
  - `feature/*` for isolated tasks
- Avoid branch switching unless explicitly requested.
- Before editing, first analyze:
  - relevant entry files
  - impact area
  - conflict risk with future upstream sync
- After editing, summarize:
  - changed files
  - why each file changed
  - whether the change is safe for upstream PR
  - suggested commit message

## Upstream Sync Rules
- Sync flow:
  1. sync `upstream/main` -> `main`
  2. merge `main` -> `custom`
  3. resolve conflicts carefully
- Never put custom fork changes back into `main`.
- If conflicts appear after syncing, prefer preserving upstream compatibility first, then reapply fork customization with minimal diff.

## Validation Rules
- Prefer quick local verification first.
- If available, validate:
  - install/build success
  - lint/type check if configured
  - local page rendering for changed UI

## Safety
- Do not remove upstream license or attribution.
- Do not modify secrets, tokens, `.env`, deployment credentials, or runtime artifacts unless explicitly requested.
- Do not rewrite Git history or force-push protected/shared branches unless explicitly requested.
