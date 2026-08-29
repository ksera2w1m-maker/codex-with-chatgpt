#!/usr/bin/env python3
from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"ERROR: expected exactly one matching block in {path}, found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "README.md",
    """2. 下载：把 https://github.com/XiaoDuoYa/codex-with-chatgpt 克隆到
   ~/codex-with-chatgpt（已存在就 git pull 更新）。
3. 构建：在该目录里执行 corepack pnpm install 和 corepack pnpm build。""",
    """2. 下载：把 https://github.com/XiaoDuoYa/codex-with-chatgpt 克隆到
   ~/codex-with-chatgpt。已存在时只检查是否有更新；没有我的明确同意，禁止
   git pull、安装依赖或执行更新后的代码。
3. 构建：在该目录里执行 corepack pnpm install --frozen-lockfile 和 corepack pnpm build。""",
)
replace_once(
    "README.md",
    """2. Download: clone https://github.com/XiaoDuoYa/codex-with-chatgpt into
   ~/codex-with-chatgpt (if it already exists, git pull to update).
3. Build: inside that folder run `corepack pnpm install` then `corepack pnpm build`.""",
    """2. Download: clone https://github.com/XiaoDuoYa/codex-with-chatgpt into
   ~/codex-with-chatgpt. If it already exists, check for updates but NEVER pull
   or install them without my explicit approval.
3. Build: inside that folder run `corepack pnpm install --frozen-lockfile` then `corepack pnpm build`.""",
)
replace_once(
    "README.md",
    """**Updates · 更新** — The Skill checks GitHub once a day and updates itself when a
new version is released; no action needed. You can also say \"更新 Codex with ChatGPT\"
anytime. / Skill 每天自动检查一次 GitHub，有新版本会自动更新，无需任何操作；
也可以随时对 Codex 说\"更新 Codex with ChatGPT\"。""",
    """**Updates · 更新** — The Skill checks GitHub once a day, but it never installs an
update automatically. When an update exists it only notifies you; applying it
requires explicit approval. You can say \"更新 Codex with ChatGPT\" anytime. /
Skill 每天只自动检查一次 GitHub，不会自动安装更新。发现新版本时只会通知你，
必须得到你的明确同意后才会更新；也可以随时对 Codex 说\"更新 Codex with ChatGPT\"。""",
)
replace_once(
    "README.zh-CN.md",
    """2. 下载：把 https://github.com/XiaoDuoYa/codex-with-chatgpt 克隆到
   ~/codex-with-chatgpt（已存在就 git pull 更新）。
3. 构建：在该目录里执行 corepack pnpm install 和 corepack pnpm build。""",
    """2. 下载：把 https://github.com/XiaoDuoYa/codex-with-chatgpt 克隆到
   ~/codex-with-chatgpt。已存在时只检查是否有更新；没有我的明确同意，禁止
   git pull、安装依赖或执行更新后的代码。
3. 构建：在该目录里执行 corepack pnpm install --frozen-lockfile 和 corepack pnpm build。""",
)
replace_once(
    "README.zh-CN.md",
    """**更新**：Skill 每天自动检查一次 GitHub，有新版本会自动更新并继续任务，
无需任何操作；也可以随时对 Codex 说\"更新 Codex with ChatGPT\"。""",
    """**更新**：Skill 每天只自动检查一次 GitHub，不会自动安装。发现新版本时只会
通知你；必须得到你的明确同意后才会执行 git pull、安装依赖和构建。也可以随时
对 Codex 说\"更新 Codex with ChatGPT\"。""",
)
replace_once(
    "skill/SKILL.md",
    """- `{ \"updateAvailable\": false }` → continue silently. Never mention the check.
- `{ \"updateAvailable\": true }` → tell the user one line:
  \"检测到 Codex with ChatGPT 有新版本，我先更新一下（约 1 分钟），随后继续你的任务。\"
  Then run the update workflow below, and CONTINUE the original task afterwards.

## Workflow: update（\"更新 Codex with ChatGPT\"，or triggered by the daily check）

Inside the checkout directory (see Locations):

1. `git pull --ff-only` (if it fails due to local edits: `git stash && git pull --ff-only`).
2. `corepack pnpm install && corepack pnpm build`.
3. Re-install the Skill: copy `skill/SKILL.md` to
   `~/.codex/skills/codex-with-chatgpt/SKILL.md`, then fix the \"checkout lives at:\"
   line in the copy to the actual checkout path.
4. `c2c sandbox-allow --json` (so existing installs pick up the sandbox allowlist),
   then `c2c restart -w <workspace>` so the bridge runs the new code, then
   `c2c update-check --force --json` to refresh the cache (should now report up to date).
5. Tell the user \"✓ 已更新到最新版本\" — then resume whatever task triggered this.
   (The updated SKILL.md takes effect from the next Codex session; that's expected.)""",
    """- `{ \"updateAvailable\": false }` → continue silently. Never mention the check.
- `{ \"updateAvailable\": true }` → tell the user one line:
  \"检测到 Codex with ChatGPT 有新版本。出于安全考虑我不会自动安装；需要更新时请明确回复『更新 Codex with ChatGPT』。\"
  Do NOT run `git pull`, install packages, build, restart, stash local changes,
  or otherwise apply the update. Continue the user's original task unchanged.

## Workflow: update（ONLY after explicit user approval）

Inside the checkout directory (see Locations):

1. Confirm that this workflow was triggered by an explicit user request such as
   \"更新 Codex with ChatGPT\". A daily update check is NEVER sufficient approval.
2. Run `git status --short`. If there are local edits, STOP and tell the user;
   NEVER run `git stash`, `git reset`, or discard local changes automatically.
3. Run `git fetch origin`, then inspect `git log --oneline HEAD..origin/main` and
   `git diff --stat HEAD..origin/main`. If the remote branch cannot be verified,
   STOP instead of executing unreviewed code.
4. Apply only a fast-forward update: `git pull --ff-only`.
5. Install exactly the locked dependency graph and build:
   `corepack pnpm install --frozen-lockfile && corepack pnpm build`.
6. Re-install the Skill: copy `skill/SKILL.md` to
   `~/.codex/skills/codex-with-chatgpt/SKILL.md`, then fix the \"checkout lives at:\"
   line in the copy to the actual checkout path.
7. `c2c sandbox-allow --json` (so existing installs pick up the sandbox allowlist),
   then `c2c restart -w <workspace>` so the bridge runs the new code, then
   `c2c update-check --force --json` to refresh the cache (should now report up to date).
8. Tell the user \"✓ 已更新到最新版本\" — then resume whatever task triggered this.
   (The updated SKILL.md takes effect from the next Codex session; that's expected.)""",
)
replace_once(
    "skill/SKILL.md",
    "2. If the c2c repo has no `node_modules`, run `pnpm install && pnpm build` in it.",
    "2. If the c2c repo has no `node_modules`, run `corepack pnpm install --frozen-lockfile && corepack pnpm build` in it.",
)
replace_once(
    "docs/security.md",
    "| Sensitive files | Deny-by-default patterns (.env*, keys, SSH, cloud creds, keychains…) enforced at resolve time — reads, listings, and search all pass through the same gate; `git diff` adds pathspec excludes; `.env.example` allowed |",
    "| Sensitive files | Deny-by-default patterns (.env*, keys, SSH, cloud creds, keychains…) are enforced by one `IgnoreRules` policy. `read_file`, listings, search, and `git_diff` all use that policy; `git_diff` first enumerates changed paths and only diffs paths that pass the policy. `.c2cignore` is honored and `.env.example` remains allowed. |",
)
replace_once(
    "docs/security.md",
    "| Tunnel exposure | Bridge binds 127.0.0.1 only (refuses 0.0.0.0); the only public surface is HTTPS via the tunnel, protected by OAuth; `/health` reveals only a salted workspace hash |",
    "| Tunnel exposure | Bridge binds 127.0.0.1 only (refuses 0.0.0.0); the only public surface is HTTPS via the tunnel, protected by OAuth; `/health` reveals only a short workspace-derived identifier, not the workspace path |",
)
replace_once(
    "docs/security.md",
    "| Admin API abuse | Loopback-only + random admin token (0600 runtime file) + requests with proxy headers (`cf-connecting-ip`, `x-forwarded-for`) rejected; unauthenticated probes get 404 |\n| Log credential leakage | Logger redacts token prefixes, bearer headers, token-like parameters, and pairing-code-shaped strings before writing |",
    "| Admin API abuse | Loopback-only + random admin token (0600 runtime file) + requests with proxy headers (`cf-connecting-ip`, `x-forwarded-for`) rejected; unauthenticated probes get 404 |\n| OAuth registration flood | Dynamic client registration is rate-limited, request sizes/redirect URI counts are bounded, and persisted client registrations have a hard cap |\n| Authorization-page injection | Repository-derived display values are HTML-escaped; the pairing page sends a restrictive Content-Security-Policy, disables framing, and is never cached |\n| Log credential leakage | Logger redacts token prefixes, bearer headers, token-like parameters, and pairing-code-shaped strings before writing |",
)

print("policy/docs hardening: applied")
