# Claim provenance

Every factual assertion on the marketing site, and where it comes from. Update
this file in the same commit as any copy change. Anything that can't be sourced
here doesn't ship.

Verified against the live platform and the backend source on 2026-09-28, and again on
2026-11-01 for the pricing, SMS, recording, push and SDK claims, and again on
2026-11-06 for every security and privacy claim on the site and in the docs
security guide.

## Claims that ship

| Claim | Source | Notes |
|---|---|---|
| Nigerian market, Lagos number pool | `proxy_numbers` region `lagos`; `GET /v1/admin/fleet` | Single region. Multi-country is a Phase 4 item. Do not imply it. `GET /v1/numbers/pool` no longer evidences this: since the number quota work it reports a workspace's own holding, not the pool's regions. |
| Private beta | No self-service onboarding; tenant provisioning is manual | Phase 3 item. |
| Calls run over PSTN, reach any handset | `CLAUDE.md` § Network Resilience; `<Dial>` via the carrier gateway | Genuinely differentiating: feature phones work. |
| `<500ms` call-routing budget, p99 | `CLAUDE.md` § Performance Targets | **Target, not a measurement.** Page labels it as such. |
| 15 min default grace period | `SESSION_DEFAULT_GRACE_PERIOD_MINUTES`, `tenants.default_grace_period` | Per-tenant override live since `a5aab54`. |
| 120 min default session cap | `SESSION_DEFAULT_MAX_DURATION_MINUTES`, `tenants.default_session_ttl_min` | Verified in live session responses. |
| AES-256-GCM at rest, per-tenant keys | `src/utils/crypto.ts:13` (`ALGO = 'aes-256-gcm'`); `src/utils/keyring.ts:170` derives per tenant, PBKDF2-SHA256 100k | True as written. The site says "per-tenant keys" and stops there; the derivation is not published. |
| The API never returns a number anyone could dial, only the last four digits | `src/api/routes/sessions.ts:138-139` -> `maskedFromLast4` in `src/utils/redact.ts:66`, which renders `+234******5678` from `sessions.party_a_last4` (migration 012) | **Corrected 2026-11-06.** The site and `about.html` both said numbers are "never returned by the API, not even to you". Four digits are returned, by design, so a seller can tell one session from another. The claim now states the guarantee that is actually true. |
| Matching a caller to a session never needs the number | `hashPhoneBlind`, `src/utils/crypto.ts:182`: HMAC-SHA256 keyed by `PHONE_HASH_SECRET`, a secret only the platform holds | **Corrected 2026-11-06.** `about.html` said "lookups run on salted hashes". That described the tenant-id-keyed columns dropped on 2 November 2026, and a tenant id is not a salt because it is not secret. `hashPhone` has no caller in `src`. |
| A number is decrypted only when the number itself is needed | Call sites: `services/call-router.ts:358` (dialling), `services/sms-router.ts:146`, `services/session-manager.ts:828-833` (target swap, comparing against both parties), plus `services/reencrypt.ts` and `scripts/verify-restore.ts` as operator actions | The docs security guide first claimed "exactly two moments". Target swap and key rotation are a third and fourth, so the guide now names them. Nothing decrypts to search, report, bill or display. |
| No phone number is written to a log in plaintext | `src/utils/logger.ts` redact paths, plus a `req` serializer that drops every query string and masks the carrier callback path | True, and enforced by a field-name list rather than proved: a new field carrying a number has to be added to it. The docs say so. |
| Numbers never logged in plaintext | `CLAUDE.md` § Code Style (hard rule) | |
| Consent prompt can't be skipped when recording | `createSession()` rejects `recordingEnabled` + `consentPrompt: NONE` | NDPR requirement; enforced server-side. |
| Webhooks Relavoi sends you are HMAC-signed | `src/services/tenant-webhook-delivery.ts` | Unchanged. **Do not claim carrier webhooks are HMAC-signed**; a signature path exists but whether the provider signs voice callbacks is unconfirmed. How callbacks *into* Relavoi are authenticated is no longer described on any public surface: see the removals table. |
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

## Example numbers

**One convention, everywhere a number appears as an example.** Recorded here
because the alternative is each page inventing its own, which is how
`+234 201 342 0117` came to sit on five pages one digit-group away from our
real DID.

| Role | E.164 | Local |
|---|---|---|
| Party A: agent, courier, driver, app user | `+2349000000001` | `09000000001` |
| Party B: customer, rider, buyer, patient | `+2349000000002` | `09000000002` |
| The proxy number Relavoi allocates | `+2349000000100` | |
| A tenant's own support line | `+2349000000200` | |

In **prose and diagrams**, a party is shown masked instead, which is how the
platform itself renders one: `+234 803 ••• 4421`. Only the proxy is ever shown
in full, because the proxy is the number the reader is meant to understand as
dialable.

Why `0900`: NCC's mobile number allocation table assigns every mobile code in
use to a named operator, and the groups it recognises are `070x`, `080x`,
`081x`, `090x` and `091x`. `0900` is the one code in that table held by no
operator; it is reserved for vanity number services, so it is not an
assignable mobile range and cannot be somebody's handset. The all-zero
subscriber block is not issued as a line either. It still satisfies the
platform's own validation (a national significant number of ten digits
starting 7, 8 or 9, `countries.mobile_pattern`), so a developer who copies a
sample gets a request the API accepts rather than a `422` on their first try.

Two rules follow.

**No realistic-looking full Nigerian number ships anywhere.** Not on the site,
not in the docs, not in an SDK README or sample app, not as a form
placeholder, not in the published OpenAPI spec. A number in a real operator's
range is somebody's line.

**Our own DID is not an example.** `+2342017001428` is the production pool. It
had reached the public API reference (`api-reference/target-swap.md`), the
published OpenAPI spec, an admin console placeholder and a Flutter test
fixture. Use the convention above instead.

## The share card

`og-card.png` at the site root, 1200x630, 83 KB. Every page points at the same
one.

Built from the brand archive rather than improvised: Ink `#0E1B2C` ground,
Pulse Teal `#2CC5AE` on the accented words (the guidelines reserve Relay Teal
for text on white and Pulse Teal for dark grounds), Proxy Amber `#F5A524` on a
single dot beside the number, which is the one use the guidelines allow it.
Sora 600 for the headline, IBM Plex Mono for the number. The lockup is
`relavoi_logo_2.svg`, the reversed one made for dark grounds.

The number on the card is `+234 900 000 0100`, the proxy from the example
convention above, for the same reason every other published number is.

Regenerate it from `brand/og-card.html`: serve the folder and screenshot at
1200x630. It is kept in the repository so the card can be changed without
anyone having to reconstruct the recipe, and it is in a subfolder because the
copy guards glob `*.html` at the root and would otherwise treat it as a page.

Each page carries its own `og:title` (its `h1`) and its own `og:description`
(its existing meta description, which is already checked against this file, so
a social preview cannot drift from the page it previews). `twitter:card` is
`summary_large_image`.

One card serves all six pages. A per-page card would be better and is not
built; if the homepage headline changes, this card has to change with it.

## Example companies

Same problem, same answer. A real company used as a fixture implies a customer
we do not have, which is why the logo wall came down.

| Role | Use |
|---|---|
| The example tenant | `Example Logistics` |
| Its app bundle id | `com.example.rider` |
| The verification banner string | a role, not a brand: "Your rider is calling" |

`example.com` and the `com.example` reverse-DNS namespace are reserved for
documentation by RFC 2606 and RFC 6761, so the bundle id cannot collide with a
real app the way `com.chowdeck.rider` did.

No claim about a named company's product ships, ours or anyone else's. Not
"Bolt and Uber connect riders and drivers using raw MSISDNs", not "unlike
Burner and Hushed", not a carrier or CPaaS vendor name. We say what we do.

Not covered by this pass: the backend dev-seed and test fixtures still name a
real company. They are not published copy. `docs/backlog.md` in
relavoi-backend carries it.

Not covered by this pass: the SDK unit-test fixtures in all three repositories
still use numbers in real operator ranges. They are not published copy, and a
phone-normalising test needs inputs in the formats people actually type, so
changing them could weaken the test rather than the exposure. The one
exception was the Flutter session test, which held our real DID, and that is
fixed.

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
| "Connect your users. Never expose their numbers." (`index.html` hero) | Replaced on 2026-11-06 with "Keep every customer on your platform." The old line described the mechanism; the new one names what a platform loses without it, which is the reason anybody buys this. The hero paragraph changed with it. Nothing in the claim set moved: the only factual sentence dropped from the hero is "Nigerian mobile numbers only today", which is still stated on `products.html` and is still the API's own refusal message. The phrase appeared nowhere else, on any surface, in any repository. |
| "headquartered in Lagos" (`about.html`) | Removed on 2026-11-01. The footer carries the registered address, which is in Abuja, with an RC number behind it. Two different head offices on one site is a question for Kay, not something to resolve by picking one. |
| "Nigerian carriers" (`about.html` values card) | Reworded to "Nigerian networks" on 2026-11-01, for the same reason the "4 carriers" logo claim went: we hold no carrier relationships. |
| "millions of couriers" | Unverifiable hyperbole. |
| "We're hiring engineers and telecom specialists" | Unverifiable. Reworded to pilot partners. |
| How carrier callbacks are authenticated (`developers.html`, docs security guide) | Removed on 2026-11-06. The page described the mechanism that protects the path the carrier posts to. A customer never touches that path, so publishing how it is secured is cost without benefit. Both surfaces now say only that securing it is our job and that the signature they verify is on the webhooks we send them. |
| Implementation internals in marketing copy and the security guide | Removed on 2026-11-06. Gone: "atomic Redis allocator", "one Redis Lua script", "a circuit breaker tracks the carrier gateway's error rate and trips on sustained failure", "the routing decision is cached by event ID", the dead-letter queue, "salted hashes", the PBKDF2 recipe and iteration count, the key-derivation diagram, column names, the bcrypt cost factor, the Docker network, and the logger's field list. What each one promised is still on the page: "two calls can never be crossed onto the same number", "duplicate carrier events never create duplicate call legs", "we know within seconds when the provider starts failing". The guarantee is the claim; the machinery is how we keep it, and it can change without the page becoming a lie. |
| Itemised roadmaps (`about.html` "On the roadmap", `products.html` "Not built yet", `how-it-works.html` secondary-provider pools) | Replaced on 2026-11-06 with one line: more is on the way, ask us. A dated list of unbuilt features is a promise with a schedule attached that nobody agreed to, and it goes stale silently. The rule that the site claims only what is live is unchanged; what is live is still listed in full. The docs keep their `## Not built yet` section, because a developer reading the reference needs to know which fields will be refused, and ten pages link to that anchor. |
| "Enterprise starts at ₦27.00 per extra minute" (`products.html`) | Removed on 2026-11-06. Now "Beyond Scale, talk to us." The three published plan figures are unchanged and still match the `plans` table. The Enterprise row in that table still reads ₦27.00; pricing is being revised separately, and an overage rate on the page is a commitment that revision would break. |
| Claims about named companies' products (docs `introduction.md`) | Removed on 2026-11-06. "There is currently no dedicated number-masking provider operating in the Nigerian market, which is why Bolt and Uber connect riders and drivers using raw MSISDNs today" and "Unlike consumer privacy apps (Burner, Hushed)". Four real companies, two of them prospective customers, and a claim about what each does that we have not verified and could not correct if they changed it. Replaced with what Relavoi is for. |
| "Chowdeck" as the example tenant, in eleven places across the docs | Removed on 2026-11-06. A real delivery company, no relationship with them, named as the workspace in the signup, auth and config examples, as `com.chowdeck.rider`, and in two SDK verification banners. The site's logo wall came down for this reason in September and the docs kept doing it. Now `Example Logistics` and `com.example.rider`. |
| "The `routing.latency.ms` metric is surfaced per tenant in Analytics" (docs `guides/call-flow.md`) | Removed on 2026-11-06. **No such metric exists**, and nothing returns routing latency per workspace: `call_routing_duration_seconds` is a Prometheus histogram on `/metrics`, which is operator-only behind `METRICS_TOKEN`. The page told integrators to build an alert on a field they would never receive. It now says so and offers to expose one. |
| The internal latency table and the breaker mechanics (docs `guides/call-flow.md`, `guides/failover.md`) | Removed on 2026-11-06. Gone: the per-stage millisecond budget naming Fastify, `crypto.timingSafeEqual` and the Redis key for each lookup, "the Call Router is explicitly designed to never hit Postgres", the Redis participant in the sequence diagram, the trip thresholds (5 consecutive failures, 10% over 2 minutes, 5 health checks, 95% over 5 minutes) and the breaker state machine. What a developer acts on stays and grew: the three states and what each means for their app, the real `GET /v1/health/cpaas` shape verified against the live endpoint, and four things to do on their side. |
| "A second provider to fail over **to** does not exist yet" (docs `guides/failover.md`) | Removed on 2026-11-06 from that page only. The observable behaviour it explained stays stated plainly: while the provider is degraded, new session creation is **refused**, not rerouted. The unavailability itself is still disclosed once, in `introduction.md` under Not built yet, which is where the docs keep that kind of statement and which ten pages link to. |

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
- **Measured on 2026-11-01, correcting what this file used to say.** The
  entry here claimed `relavoi.com` had no DNS record and that both contact
  addresses would bounce for want of MX records. That was written before the
  domain was set up and was repeated in a report without being re-checked.
  What is actually true: the zone is delegated to Namecheap, carries Google
  Workspace MX, SPF `include:_spf.google.com`, DMARC `p=none` reporting to
  ops@, and `relavoi.com`, `api`, `staging-api`, `app`, `admin` and `docs` all
  resolve and serve valid Let's Encrypt certificates.
- **`sales@relavoi.com` does not exist.** Tested through SES on 2026-11-01 from
  ops@: the message to `sales@` hard-bounced and the address is now on the SES
  account suppression list; the message to `support@` was accepted. The contact
  page lists both and its form composes a `mailto:` to `sales@`, so the form
  currently goes nowhere. Kay is deciding whether to create the mailbox or
  point the page at `support@`. If the mailbox is created, the suppression
  entry has to be cleared first:
  `aws sesv2 delete-suppressed-destination --email-address sales@relavoi.com`.
- **`staging-api.relavoi.com` is an unused alias.** It resolves to the same
  instance as `api.relavoi.com`, holds its own certificate, and nothing outside
  `relavoi-infra` refers to it: no SDK, no console, no doc, no script.
  Recommended for deletion.
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
