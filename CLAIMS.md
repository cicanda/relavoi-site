# Claim provenance

Every factual assertion on the marketing site, and where it comes from. Update
this file in the same commit as any copy change. Anything that can't be sourced
here doesn't ship.

Verified against the live platform and the backend source on 2026-09-28.

## Claims that ship

| Claim | Source | Notes |
|---|---|---|
| Nigerian market, Lagos number pool | `proxy_numbers` region `lagos`; `GET /v1/numbers/pool` | Single region. Multi-country is a Phase 4 item. Do not imply it. |
| Private beta | No self-service onboarding; tenant provisioning is manual | Phase 3 item. |
| Calls run over PSTN, reach any handset | `CLAUDE.md` § Network Resilience; `<Dial>` via the carrier gateway | Genuinely differentiating: feature phones work. |
| `<500ms` call-routing budget, p99 | `CLAUDE.md` § Performance Targets | **Target, not a measurement.** Page labels it as such. |
| 15 min default grace period | `SESSION_DEFAULT_GRACE_PERIOD_MINUTES`, `tenants.default_grace_period` | Per-tenant override live since `a5aab54`. |
| 120 min default session cap | `SESSION_DEFAULT_MAX_DURATION_MINUTES`, `tenants.default_session_ttl_min` | Verified in live session responses. |
| AES-256-GCM at rest, per-tenant keys | `src/utils/crypto.ts`; `sessions.party_*_phone_enc` | Lookups go via salted SHA-256 hashes. |
| Numbers never logged in plaintext | `CLAUDE.md` § Code Style (hard rule) | |
| Consent prompt can't be skipped when recording | `createSession()` rejects `recordingEnabled` + `consentPrompt: NONE` | NDPR requirement; enforced server-side. |
| HMAC-signed CPaaS webhooks | `cpaasSignatureValid()` in `src/api/routes/webhooks.ts` | Mandatory outside sandbox. Was unenforced until `a5881bb`. |
| iOS / Android / Flutter SDKs | `relavoi-{ios,android,flutter}-sdk` | Exist and build. Deliberately no maturity claim: the July audit found API contract drift. |
| API shape in the code sample | Live `POST /v1/auth/token` + `POST /v1/sessions` | Key prefixes `rk_live_` / `rs_`, JWT bearer, JSON body, camelCase response. |
| Two-party sessions | `direction_mode` ∈ BIDIRECTIONAL / A_TO_B_ONLY / B_TO_A_ONLY | Strictly two parties. No multi-party chain exists. |
| Outbound webhook contract | `src/services/tenant-webhook-delivery.ts` | `X-Relavoi-Signature: sha256=<hmac of timestamp.body>`, dedupe header `X-Relavoi-Delivery`, body `{event,timestamp,data}`. Retries with exponential backoff, logs each attempt. |
| Event names | `CLAUDE.md` § Event Bus; `src/workers/event-consumers.ts` | `session.created/expired`, `call.incoming/answered/ended/failed`, `sms.sent`. |
| Recording gated on consent | `response-builder.ts` emits `record="true"` only after the consent action | Recordings live at the provider; encrypted storage is a roadmap item. |
| Metered pricing, 3 tiers, NGN | `src/seeds/pricing-seed.ts` | STARTER / GROWTH / ENTERPRISE, five metrics each. **Needs commercial sign-off. See Open items.** |
| Inbound SMS not billed | `sms_received` unit price `0` on every tier | |
| Docs deep links | Every URL probed against the live site, 200 only | `/guides` and `/api-reference` have no index page, so don't link them. |
| iOS / Android / Flutter SDK identifiers | `Package.swift` (`RelavoiSDK`), `build.gradle.kts` (`com.relavoi.sdk`), `relavoi-flutter-sdk` | No version numbers published, since they'd go stale. |

## Claims removed from the template

| Removed | Why |
|---|---|
| "Live across Lagos, Abuja & Port Harcourt" | One region (`lagos`), one DID in the pool. |
| Chowdeck / Kwik / Sendbox / mDoc / Jiji logo wall | Real companies, no relationship with any of them. "Chowdeck" appears only as a dev-seed fixture name. Naming them implies customers we don't have. |
| "412ms median call setup" | Fabricated. No such measurement exists. |
| "99.98% API uptime, trailing 30 days" | Fabricated. No uptime record; 99.9% is a target. |
| "3,200+ proxy numbers across 6 regions" | Pool holds **1** number in **1** region. |
| "4 carriers: MTN, Airtel, Glo, 9mobile" | Those are the networks end users happen to be on. Relavoi holds no direct carrier relationships. Numbers come via the CPaaS provider. |
| "Sub-500ms routing" as achieved fact | It's a target. Reworded and labelled. |
| Logistics "multi-party masked chain" | Data model is two-party only. |
| Marketplace `ttl 72h` | Exceeds the 120-min default; would need an explicit override. Shown as 24h. |
| "Sandbox numbers included on every account" | No self-service accounts exist. |
| "Go live once your pool is provisioned, usually the same week" | `POST /numbers/provision` is a `501` stub; provisioning is manual. |
| "NCC licensed" (footer) | **Relavoi is not NCC licensed.** The CPaaS provider holds the NCC approvals. Corrected to "Numbers via NCC-licensed carriers". |
| "NDPR compliant" (footer) | Self-assessed, no audit. Softened to "NDPR-aligned". |
| Live DID in the hero diagram | The pool's one real number is not published. Diagram numbers are illustrative and labelled as such. |
| "region LOS-01 · carrier MTN · 38ms" | Region label is `lagos`, the provider is the CPaaS gateway (not a carrier), and the 38ms was invented. |
| "Automatic failover to secondary CPaaS providers" | The circuit breaker is real, but **no Twilio numbers exist in any pool** and `TWILIO_ACCOUNT_SID` is empty. Nothing to fail over to. Reworded as health monitoring + roadmap. |
| Node.js and Python SDKs | Neither exists. Only iOS, Android and Flutter. |
| SDK version `2.4.1` | Invented. No published release carries that version. |
| "Offline queue" as an SDK feature | `OfflineQueue` is orphaned: referenced nowhere in the iOS SDK outside its own file, and absent from Flutter. |
| Stripe-style `X-Relavoi-Signature: t=…,v1=…` | Real header is `sha256=<hex>`. Body was `{id,type,session_id,data}`; real is `{event,timestamp,data}`. "Dedupe on event_id" → `X-Relavoi-Delivery`. |
| Six broken docs deep links | `/getting-started`, `/api-reference`, `/guides`, `/sdks/{ios,android}` all 404 on the deployed docs build. Replaced with probed 200 URLs. |
| Pricing: ₦80k/₦240k/₦480k monthly, a "Scale" tier, 10/50/250 numbers, "Lagos + Abuja", "All Nigerian regions", 99.99% SLA | Wholly fabricated. There is no flat monthly fee; billing is metered. There are three tiers, not four. Included numbers are 2/10/50. One region. The uptime target is 99.9%, and no SLA is contracted. |
| "Sandbox keys include two test proxy numbers" / "sandbox keys within one business day" | No self-service signup exists; provisioning is manual. |
| "Integration help for existing customers" | There are no customers yet. |
| Team grid with "Founder name" × 4 | Placeholder people. Removed rather than invented, and replaced with an honest Live / In progress / Roadmap section. |
| Phone `+234 800 000 0000` | Placeholder number. Removed; office hours kept. |
| Contact form's fake success message | It rendered "we'll be in touch" while sending nothing anywhere. Now composes a real `mailto:` with the field values. |
| "millions of couriers" | Unverifiable hyperbole. |
| "We're hiring engineers and telecom specialists" | Unverifiable. Reworded to pilot partners. |

## Open items

- **Pricing needs commercial sign-off.** The naira rates on `products.html` come
  from `pricing-seed.ts`, which is the only machine-readable source of truth,
  but it's a *seed file*, and it may hold development placeholders rather than
  agreed commercial rates. Published prices are a commitment. Confirm before
  this page is public.
- **`relavoi.com` has no DNS record.** Only `api.relavoi.com` and
  `docs.relavoi.com` resolve. `sales@relavoi.com` and `support@relavoi.com` on
  the contact page will bounce until MX records exist, and the site itself has
  nowhere to be hosted at the apex domain yet.
- **The contact form has no backend.** It composes a `mailto:` as an honest
  fallback. Wire it to a form endpoint (or the tenant API) before launch; the
  mailto loses anyone without a configured mail client.
- **`CICANDA Ltd`** in the footer and on `about.html` links to the parent site
  at cicanda.com (verified reachable). Confirm the registered entity name reads
  exactly as Companies Registry has it before this goes public.
- **Team section was removed**, not replaced. Supply names, roles and photos if
  you want it back.
- The stat band is honest but soft. Once real telemetry exists (`/metrics`
  already exports routing histograms), replace targets with measurements and
  move those rows into the table above.
