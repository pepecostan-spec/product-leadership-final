# PM Tour: maybe-finance/maybe

**Repo**: [github.com/maybe-finance/maybe](https://github.com/maybe-finance/maybe)
**Note**: This repo is archived/no longer actively maintained (final release v0.6.0) but the codebase is fully functional and self-hostable under AGPLv3. Reviewed by cloning locally and reading the code directly, not just browsing GitHub.

**Stack at a glance**: Ruby on Rails + PostgreSQL, Hotwire (Turbo + Stimulus, not a JS SPA framework), ViewComponents for UI, Tailwind CSS, Sidekiq for background jobs, Plaid for bank sync.

---

## 1. What this product does, in one sentence
Maybe is an open-source personal finance app that lets a household ("family") connect and manually track all their accounts — checking, credit cards, investments, crypto, property, vehicles, loans — to see net worth, budget by category, and get AI-assisted insight, either self-hosted or Maybe-managed.

## 2. How the codebase is organized

| Folder | What it does |
|---|---|
| `app/models/` | Where the actual business logic lives. This team follows a "fat model, skinny controller" convention deliberately — see finding below. |
| `app/controllers/` | Thin request handlers that delegate to models; ~40 resource controllers, one per major feature area (accounts, budgets, rules, imports, etc.) |
| `app/jobs/` | Sidekiq background jobs — account syncing, CSV import processing, AI chat response generation, scheduled cleanup |
| `app/components/` | ViewComponents — reusable UI building blocks, split into `DS/` (raw design-system primitives) and `UI/` (composed components) |
| `app/views/` | ERB templates, one folder per resource, mirroring the controllers |
| `app/javascript/` | Stimulus controllers for interactivity — intentionally minimal JS; native HTML (`<dialog>`, `<details>`) is preferred over JS components |
| `app/services/` | Nearly empty (2 files) — **this is a deliberate choice**, not an oversight. The team pushes business logic into models instead of a services layer. |
| `app/channels/` | ActionCable (websockets) — used for streaming AI chat responses live |
| `app/mailers/` | Transactional email |
| `app/data_migrations/` | One-off data backfill scripts, kept separate from schema migrations |
| `db/` | `schema.rb` (59 tables) + migrations + seed data |
| `config/routes.rb` | ~66 top-level resources — a genuinely broad feature surface for a personal finance app |
| `docs/` | Only 2 files (hosting + API docs) — this is for self-hosters/integrators, not a PM-facing product doc folder |
| `test/` | Minitest + fixtures only — the team explicitly avoids RSpec and FactoryBot (stated in their own contributor guide) |

## 3. The 3 most important files to know

1. **`app/models/account.rb`** — The central entity. Every account type (checking, credit card, investment, crypto, property, vehicle, loan) is a subtype of `Account` via Rails' `delegated_type` mechanism. Reading this file is reading how the product defines "everywhere money or debt can live."
2. **`app/models/entry.rb`** — The universal ledger line. Every transaction, balance snapshot ("valuation"), and investment trade is wrapped in an `Entry` using the same polymorphic pattern as `Account`. This is *why* the product can show one unified activity timeline across totally different account types instead of building a separate feed per account type.
3. **`app/models/family.rb`** — The tenant boundary. Accounts, budgets, rules, and entries all belong to a `Family`, not a `User`. This one modeling decision is why multi-user households, shared budgets, and invitations exist as first-class features rather than a "sharing" feature bolted on later.

**Bonus, not code**: the repo's own root `CLAUDE.md` is a genuinely good PM-level architecture briefing written by the team itself — it explains their conventions and reasoning better than inferring from code alone, and is worth reading directly if you want more depth than this summary.

## 4. Key data models and what they tell you about product decisions

- **`Account` + accountable subtypes** (Depository, CreditCard, Investment, Crypto, Property, Vehicle, Loan, OtherAsset, OtherLiability) → **Decision**: this is a net-worth product (assets minus liabilities), not just a spending tracker. Investments, property, and vehicles are first-class, not an afterthought — meaningfully broader scope than Nudge's current surface.
- **`Entry` + entryable subtypes** (Transaction, Valuation, Trade) → **Decision**: a single "thing happened on this date" abstraction unifies wildly different data (a coffee purchase, a manual balance correction, a stock trade) so the rest of the app doesn't need type-specific logic for basic operations like sorting a timeline or recalculating balance history.
- **`Family` as owner of everything, not `User`** → **Decision**: built for households from day one, not a single-user app with sharing added later.
- **`Rule`** (conditions + actions applied to transactions) → **Decision**: user-authorable automation (auto-categorize, auto-tag) is a core trust feature — users can see and control the "if this, then that" logic rather than trusting an opaque AI classifier alone.
- **`Budget` + `BudgetCategory`** → **Decision**: budgeting is category-based and month-scoped, closer to Monarch's model than YNAB's zero-based envelope approach.
- **`PlaidItem`/`PlaidAccount` alongside `Import`** → **Decision**: two parallel ingestion paths — real-time bank sync AND manual CSV import — coexist deliberately, likely because a privacy-conscious/self-hosting audience won't always want to link bank credentials via Plaid.
- **`Chat` / `Assistant` / `Message` / `ToolCall`** → **Decision**: an AI chat assistant that can call tools against the user's real financial data is treated as a core feature, not a bolt-on — Maybe's answer to "how do I get insight," in the same spirit as Monarch's AI Assistant.
- **`Sync`** (a tracked, stateful process, not fire-and-forget) → **Decision**: data freshness and reliability are treated as first-class product concerns — sensible for a finance app where stale data erodes trust fast.

## 5. What you'd need to understand to write a good ticket for a notification ranking feature

**Important finding**: this codebase has no notification or push infrastructure at all. The only thing called "notification" (`app/controllers/concerns/notifiable.rb`) renders transient in-app flash/toast messages (alerts, CTAs) via Turbo Streams — it's UI feedback for the current request, not a push system, not a ranked feed, and there's no notification-history table or per-user notification-preference model anywhere in the schema. A notification ranking feature here would be **greenfield, not an extension** — there's nothing existing to inherit or reuse for the ranking/delivery mechanism itself. That changes what the ticket needs to cover:

- **Candidate signal sources** — since there's no existing "notification event" concept, the ticket needs to enumerate what could trigger a notification by looking at what already changes in the data: new `Entry` creation (a transaction posted), `Sync` completion, a `Budget` category crossing its `available_to_spend` threshold, a `Rule` match, or a balance change. These are the raw signals a ranking model would prioritize among.
- **Who gets notified** — data is owned by `Family`, but notifications are presumably per-`User`. That mapping isn't modeled anywhere yet (e.g., does every family member get notified about every account, or just whoever connected it?) — the ticket needs to explicitly define this, it won't fall out of the existing schema.
- **Timing/trigger point** — since signals like new transactions arrive via the `Sync` lifecycle (`sync.rb`, `SyncJob`), understanding when a sync is considered "complete" matters for deciding when a notification-ranking pass would even run.
- **A reusable mental model, if not reusable code** — the `Rule` engine's condition/action pattern (already built for transactions) is the closest existing analog to "if X happens, do Y" logic, even though it currently mutates data (categorize, tag) rather than notifying. Worth referencing in the ticket as prior art for how this team structures conditional logic, even if the notification system itself is net-new.
- **What's entirely unspecified today**: importance/ranking criteria, delivery channel (push vs. in-app vs. email), frequency capping, and user notification preferences. None of this exists in the current schema — the ticket needs to specify all of it from scratch rather than assuming there's a default to extend.
- **Existing infra to build on**: Sidekiq background jobs already follow a "react to a model change" pattern (e.g., `AutoCategorizeJob`, `AutoDetectMerchantsJob` fire off transaction creation) — a notification-ranking job would plausibly follow the same shape, which is useful context for scoping engineering effort in the ticket.
