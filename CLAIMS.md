# Claim provenance

Every factual assertion on the marketing site, and where it comes from. Update
this file in the same commit as any copy change. Anything that can't be sourced
here doesn't ship.

Verified against the live platform and the backend source on 2026-09-28, and again on
2026-11-01 for the pricing, SMS, recording, push and SDK claims.

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
| Carrier callbacks authenticated by a secret callback address | `authorizeCallback()` in `src/api/routes/webhooks.ts`; `CPAAS_CALLBACK_TOKEN`, `CPAAS_CALLBACK_ENFORCE=true` | The gateway posts to a path carrying a secret token, compared in constant time. A signature path exists but whether the provider signs voice callbacks is unconfirmed, so **do not claim carrier webhooks are HMAC-signed**. Only the webhooks Relavoi sends to businesses are signed. |
| iOS / Android / Flutter SDKs | `relavoi-{ios,android,flutter}-sdk` | Exist and build. Deliberately no maturity claim: the July audit found API contract drift. |
| API shape in the code sample | Live `POST /v1/auth/token` + `POST /v1/sessions` | Key prefixes `rk_live_` / `rs_`, JWT bearer, JSON body, camelCase response. |
| Two-party sessions | `direction_mode` ∈ BIDIRECTIONAL / A_TO_B_ONLY / B_TO_A_ONLY | Strictly two parties. No multi-party chain exists. |
| Outbound webhook contract | `src/services/tenant-webhook-delivery.ts` | `X-Relavoi-Signature: sha256=<hmac of timestamp.body>`, dedupe header `X-Relavoi-Delivery`, body `{event,timestamp,data}`. Retries with exponential backoff, logs each attempt. |
| Event names | `CLAUDE.md` § Event Bus; `src/workers/event-consumers.ts` | `session.created/expired`, `call.incoming/answered/ended/failed`, `sms.sent`. |
| Recording gated on consent | `response-builder.ts` emits `record="true"` only after the consent action | Recordings live at the provider; encrypted storage is a roadmap item. |
| Monthly plans, NGN, included minutes plus overage | `plans` table, live database, read 2026-11-01 | STARTER 50,000 / 1,500 / 35.00; GROWTH 250,000 / 8,000 / 32.00; SCALE 1,000,000 / 35,000 / 30.00; ENTERPRISE 27.00 overage, shown as "talk to us". Concurrency figures are `max_concurrent_sessions`. Published static; see CLAUDE.md. |
| Prepaid wallet, per started minute, answered only | `src/services/billing/`, `wallet_ledger`; `GET /v1/billing/wallet` | Verified live on 2026-11-01: the endpoint returns the STARTER plan block with NGN 50,000.00 and NGN 35.00. |
| Nigerian mobile numbers only | `countries` holds one enabled row, NG, `mobile_pattern ^[789][0-9]{9}$`; session parties normalise with `allow: 'mobile'`; `assertSameCountry` refuses cross-border | The API's own refusal says "Relavoi currently connects Nigerian mobile numbers only." A landline is accepted only as a tenant's REDIRECT_SUPPORT target, never as a party. |
| Session length configurable up to 24 hours | `maxDurationMinutes` is `.max(1440)` in `POST /sessions`; default 120 from `SESSION_DEFAULT_MAX_DURATION_MINUTES` | Grace period has the same 1440 ceiling. |
| Webhook replay window of five minutes | `docs/guides/webhook-integration.md`: reject `|now - timestamp| > 300` | Advice to the receiver, not something we enforce. We sign `X-Relavoi-Timestamp` so they can. |
| iOS Live Activities | `relavoi-ios-sdk` v0.2.0, `Sources/RelavoiSDK/LiveActivity/`, `public final class LiveActivityManager` | Public and in the released tag, and in the SDK README. Not reachable from the `Relavoi` facade, and the host app must ship a Widget Extension and set `NSSupportsLiveActivities`, which the page now says. |
| In-call verification | `CallVerificationManager` wired into the public facade in all three SDKs (`Relavoi.swift:66`, `Relavoi.kt:141`, `relavoi.dart:23`) | The one SDK feature that is wired, released and the same on every platform. |
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
| "NDPR-aligned" (footer) | Removed entirely on 2026-10-30. Even softened, it is a compliance claim we cannot back: the privacy policy is unpublished, the retention jobs are unbuilt and there is no NDPC registration. "Numbers via NCC-licensed carriers" stays, because the carrier gateway really does hold the approvals. |
| "Built for NDPR" (`index.html` card heading) | Removed on 2026-10-30. A compliance claim we cannot back, for the same reasons the footer claim went. Now "Privacy built in", and the body keeps only what is true today: AES-256-GCM at rest under per-tenant keys, and no plaintext numbers in logs. |
| "a consent prompt the platform refuses to let you skip when recording is on" (`index.html` card body) | True of the code, but recording is not a live feature, so as written it advertised something nobody can switch on. Now states that recording is coming soon and will only run after a consent message the caller hears first. |
| "Recording gated behind an enforced NDPR consent prompt" (`products.html`) | Same reason. Recording is not live, and the sentence led with a regulation rather than with the mechanism. Now "Call recording (coming soon): only after a consent message the caller hears first." |
| "NDPR" in the `about.html` meta description and story copy | Naming the regulation in a list of things we were "built for" reads as a compliance claim. Replaced with "Nigeria's data protection law", which describes what the design accounts for without asserting a status. The meta description was re-cut to 139 characters so it does not truncate in search results. |
| "Nigerian compliance" (`about.html` values card) | Asserts a state rather than a feature, and is the weakest of the six claims found in the 2026-10-30 scan. Replaced with "private by design". |
| Privacy / Terms / NDPR DPA footer links | They pointed at `contact.html`. A link labelled "Privacy" that opens a contact page is worse than no link. The Legal column is gone; the security guide moved to Developers. |
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
| SMS masking, everywhere it appeared | Removed on 2026-11-01. `sms_records` holds zero rows, nothing has ever sent one, and the only SMS code path is a lazily constructed SDK client that no live traffic reaches. The products section, the "every tier includes SMS" line, the three SMS pricing rows, the `sms.sent` webhook event and the SMS entry in the REST API card are all gone. It is named once, on the roadmap list. |
| Call recording, everywhere it appeared | Removed on 2026-11-01. `RECORDING_AVAILABLE = false` in `src/services/features.ts`, and the gate exists because the API would otherwise have accepted `recordingEnabled`. "Coming soon" labels on the voice feature list, the privacy card and the telemedicine card are gone, as is "recording consent" from the Developers concepts card. Named once, on the roadmap list. |
| Branded push alerts | Removed on 2026-11-01. The SDKs register device tokens and expose a hook; the host app renders the notification. More to the point the platform cannot send one: no `FIREBASE_*` value is set on the box and `device_tokens` holds zero rows. Removed from the products SDK list, the how-it-works step 04 and the Developers SDK blurb. Named once, on the roadmap list. |
| Post-call rating and issue-report components | Removed on 2026-11-01. They do not exist in any of the three SDKs: no file, class or symbol matching post-call, rating or issue anywhere under `Sources/`, `src/main/` or `lib/`. Not on the roadmap list either, because nobody has asked for it. |
| Prometheus metrics endpoint | Removed from customer-facing copy on 2026-11-01. `/metrics` is real but guarded by `METRICS_TOKEN` through the public proxy and answers 404 without it, so it is an operator surface, not a tenant one. |
| "Priced in naira. Billed by usage." / "No platform fee" | Removed on 2026-11-01. Both describe the metered seed pricing that the `plans` table replaced. There is a monthly fee, and it is the larger half of the bill. |
| "See every call. Store no numbers." | Reworded to "Never see a number" on 2026-11-01. We do store numbers, as AES-256-GCM ciphertext; what we never do is show them to anybody, including the tenant. The old line claimed the stronger thing and the weaker thing was the true one. |
| "headquartered in Lagos" (`about.html`) | Removed on 2026-11-01. The footer carries the registered address, which is in Abuja, with an RC number behind it. Two different head offices on one site is a question for Kay, not something to resolve by picking one. |
| "Nigerian carriers" (`about.html` values card) | Reworded to "Nigerian networks" on 2026-11-01, for the same reason the "4 carriers" logo claim went: we hold no carrier relationships. |
| "millions of couriers" | Unverifiable hyperbole. |
| "We're hiring engineers and telecom specialists" | Unverifiable. Reworded to pilot partners. |

## Open items

- **Pricing is published as introductory and subject to written confirmation.**
  The rates now come from the `plans` table in the live database rather than
  from a seed file, which is a real source of truth, and Kay approved these
  four plans on 2026-11-01. The page says so in as many words, because a
  published price is a commitment: "Introductory pricing, subject to
  confirmation in writing before you go live."
- **Enterprise has concrete numbers in the table that the site does not
  publish.** The row reads NGN 3,000,000 a month for 105,000 included minutes
  at NGN 27.00 overage. Kay's instruction was to show Enterprise as "talk to
  us, from NGN 27", so the monthly fee and the allowance are deliberately not
  on the page. If that changes, the row is already there.
- **Lagos or Abuja.** `about.html` said "headquartered in Lagos", the footer
  gives a registered address in Abuja with an RC number, and `contact.html`
  still says the office is in Lagos. The claim removed is the vaguest of the
  three; the contact page is left alone because changing an address on a guess
  is worse than an inconsistency Kay can settle in one sentence.
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
- **The products SDK illustration still draws a push notification.** The
  claim is gone from the copy but the phone mock-up beside it shows "Your
  courier is calling". That is Genesis's artwork, so it is listed for them
  rather than edited here.
- The stat band is honest but soft. Once real telemetry exists (`/metrics`
  already exports routing histograms), replace targets with measurements and
  move those rows into the table above.
