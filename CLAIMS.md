# Claim provenance

Every factual assertion on the marketing site, and where it comes from. Update
this file in the same commit as any copy change. Anything that can't be sourced
here doesn't ship.

Verified against the live platform and the backend source on 2026-09-28.

## Claims that ship

| Claim | Source | Notes |
|---|---|---|
| Nigerian market, Lagos number pool | `proxy_numbers` region `lagos`; `GET /v1/numbers/pool` | Single region. Multi-country is a Phase 4 item — do not imply it. |
| Private beta | No self-service onboarding; tenant provisioning is manual | Phase 3 item. |
| Calls run over PSTN, reach any handset | `CLAUDE.md` § Network Resilience; `<Dial>` via Africa's Talking | Genuinely differentiating — feature phones work. |
| `<500ms` call-routing budget, p99 | `CLAUDE.md` § Performance Targets | **Target, not a measurement.** Page labels it as such. |
| 15 min default grace period | `SESSION_DEFAULT_GRACE_PERIOD_MINUTES`, `tenants.default_grace_period` | Per-tenant override live since `a5aab54`. |
| 120 min default session cap | `SESSION_DEFAULT_MAX_DURATION_MINUTES`, `tenants.default_session_ttl_min` | Verified in live session responses. |
| AES-256-GCM at rest, per-tenant keys | `src/utils/crypto.ts`; `sessions.party_*_phone_enc` | Lookups go via salted SHA-256 hashes. |
| Numbers never logged in plaintext | `CLAUDE.md` § Code Style (hard rule) | |
| Consent prompt can't be skipped when recording | `createSession()` rejects `recordingEnabled` + `consentPrompt: NONE` | NDPR requirement; enforced server-side. |
| HMAC-signed CPaaS webhooks | `cpaasSignatureValid()` in `src/api/routes/webhooks.ts` | Mandatory outside sandbox. Was unenforced until `a5881bb`. |
| iOS / Android / Flutter SDKs | `relavoi-{ios,android,flutter}-sdk` | Exist and build. Deliberately no maturity claim — the July audit found API contract drift. |
| API shape in the code sample | Live `POST /v1/auth/token` + `POST /v1/sessions` | Key prefixes `rk_live_` / `rs_`, JWT bearer, JSON body, camelCase response. |
| Two-party sessions | `direction_mode` ∈ BIDIRECTIONAL / A_TO_B_ONLY / B_TO_A_ONLY | Strictly two parties. No multi-party chain exists. |

## Claims removed from the template

| Removed | Why |
|---|---|
| "Live across Lagos, Abuja & Port Harcourt" | One region (`lagos`), one DID in the pool. |
| Chowdeck / Kwik / Sendbox / mDoc / Jiji logo wall | Real companies, no relationship with any of them. "Chowdeck" appears only as a dev-seed fixture name. Naming them implies customers we don't have. |
| "412ms median call setup" | Fabricated. No such measurement exists. |
| "99.98% API uptime, trailing 30 days" | Fabricated. No uptime record; 99.9% is a target. |
| "3,200+ proxy numbers across 6 regions" | Pool holds **1** number in **1** region. |
| "4 carriers: MTN, Airtel, Glo, 9mobile" | Those are the networks end users happen to be on. Relavoi holds no carrier relationships — numbers come via Africa's Talking. |
| "Sub-500ms routing" as achieved fact | It's a target. Reworded and labelled. |
| Logistics "multi-party masked chain" | Data model is two-party only. |
| Marketplace `ttl 72h` | Exceeds the 120-min default; would need an explicit override. Shown as 24h. |
| "Sandbox numbers included on every account" | No self-service accounts exist. |
| "Go live once your pool is provisioned — usually the same week" | `POST /numbers/provision` is a `501` stub; provisioning is manual. |
| "NCC licensed" (footer) | **Relavoi is not NCC licensed.** Africa's Talking holds the NCC approvals. Corrected to "Numbers via NCC-licensed carriers". |
| "NDPR compliant" (footer) | Self-assessed, no audit. Softened to "NDPR-aligned". |
| Live DID in the hero diagram | The pool's one real number is not published. Diagram numbers are illustrative and labelled as such. |

## Open items

- **`CICANDA Ltd / Kalubridge Ltd`** in the footer is carried over unverified —
  confirm the registered entity before this goes public.
- The stat band is honest but soft. Once real telemetry exists (`/metrics`
  already exports routing histograms), replace targets with measurements and
  move those rows into the table above.
