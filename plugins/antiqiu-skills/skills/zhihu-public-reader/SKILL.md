---
name: zhihu-public-reader
description: Read the full body of one user-specified public Zhihu answer through zhihu-cli, with HTTP/completeness checks and auth stop rules; not search or crawling.
---

# Zhihu Public Reader

Read the complete body of one user-specified public answer through `zhihu-cli`. Discovery, hot lists, account data and search summaries belong to the official `zhihu` capability; summaries are not full answers. The API probe is a compatibility fallback, not an access-control bypass.

## Read

1. Check `zhihu-cli --version` and `auth status` once; reuse until install/path/auth changes. Report health without credentials.
2. Remove tracking/query parameters and accept only `https://www.zhihu.com/question/<question-id>/answer/<answer-id>`.
3. Run `scripts/read_public_answer.ps1` once. It uses `zhihu-cli answer <url> --api --json`, verifies an active profile, makes at most one answer-detail request, disables captcha retries and rejects redirects.
4. Analyze only HTTP 200 plus valid JSON, matching answer ID, nonempty content, no top-level error and exit 0. Stop on authentication errors, captcha, login wall, malformed JSON or missing content; no alternate hosts, endpoint enumeration, proxy/fingerprint rotation or browser credential extraction.
5. After normal user-completed login/verification, the same canonical request may be retried once.

```powershell
& '<skill-dir>\scripts\read_public_answer.ps1' -Url 'https://www.zhihu.com/question/<question-id>/answer/<answer-id>'
```

`-MetadataOnly` checks reachability without returning the body. No active profile means no request. `-AllowAnonymousProbe` is only for one explicitly authorized compatibility test, never retries or alternate endpoints.

## Restore CLI access only when requested

Browser readability does not prove CLI authentication. Use a user-visible interactive terminal that keeps stdin attached for `zhihu-cli login --qrcode --browser <edge|chrome> -p <profile>`. Let the user complete safety verification and QR confirmation personally; keep the same process and do not automate challenges or duplicate them.

After reported login success, check auth status and read the same answer once. If still blocked, stop. When QR login is unavailable, only a request deliberately copied and supplied by the user may enter `zhihu-cli auth paste`; never collect browser storage or credentials on their behalf or expose them in chat/logs.

## Deliver

Answer concisely in chat, separating author claims, visible facts and inference. Save a file only when requested or needed by the actual downstream task; retain necessary metadata, canonical URL, completeness evidence and short excerpts without expanding them into an extra report or copying the full answer into a Wiki.

Report `ok`, `blocked_auth`, `blocked_human_verification`, `unreadable` or `cli_error` according to the actual response. A restored CLI claim requires a fresh native read satisfying all HTTP/JSON/identity/content/error/exit checks above; browser access, profile presence, QR success and unit tests alone are insufficient.
