# Speaker Notes — Nudge Engage v2 Quarterly Review

*Full sentences, written to be said out loud. Pairs with `docs/presentation.md`.*

---

### Slide 1 — The Problem

Our 30-day retention has dropped from 44% to 37% over the last two quarters, and that's the number driving everything in this deck. What's important is where that drop is actually happening: day-one activation hasn't moved at all, it's stayed at 90 to 97 percent in every single cohort, so people are still signing up and connecting their accounts just fine. The entire decline is concentrated in the first week after that — people get the initial spending breakdown, find it genuinely useful, and then the app goes quiet and gives them no reason to come back. Before you move on, I want you to take away one thing: this isn't an acquisition problem, it's a first-week relevance problem, and that's what shaped everything we did this quarter.

### Slide 2 — Why Now

This quarter we didn't just theorize about the drop, we went and diagnosed it properly — user interviews, an NPS analysis, a competitive scan, and then we checked all of it against real retention data rather than trusting anecdote. Two things came out of that which changed our thinking. First, users are telling us, independently, in interviews and in NPS comments, that they want to be told what to do, not just shown more information — that's a specific, actionable gap, not a vague complaint. Second, when we looked at YNAB, Cleo, and Monarch, none of them actually solve that combination of being low-effort and still telling you what to do next, so this isn't a solved problem we're just copying, it's real white space. I also want to be upfront that we found a second problem in the process — retention from day seven to day thirty is flat and untouched by anything we've built so far — and I'm naming that now rather than letting it surface later.

### Slide 3 — The Proposal

What we've built is a personalized weekly summary: one insight about your spending that you probably didn't already know, one specific nudge tied to that insight, and your savings goal progress, all in the app, using only data we already have. It's currently sitting in QA. I want to be just as clear about what this is not, because scope creep is the fastest way to lose trust in a result like this. It's not an AI-ranked system in this version, it's deliberately simple, rules-based logic. It doesn't take actions on the user's behalf yet, a nudge is a suggestion, not an automatic change. And critically, it does not fix the day seven to thirty problem I just mentioned — I don't want anyone walking away from this deck thinking one feature solved the whole retention story.

### Slide 4 — Evidence

We didn't just ship this and hope — we tested it with a prototype against someone matching our actual at-risk user, and we ran a real controlled experiment. The quotes on this slide aren't cherry-picked for color, they're the same language showing up independently across interviews and NPS: people are explicitly asking to be told what to do, not just shown a dashboard. On the data side, the headline result is that day-seven retention nearly doubled, from 46 to 76 percent, and that result is statistically significant. I do want to flag, because I'd rather you hear it from me than find it later, that the day-thirty number — 22 to 36 percent — is directionally exciting but not yet statistically significant at this sample size, which is exactly why the next slide is about running a bigger test before we celebrate that number.

### Slide 5 — The Plan

Here's what happens next and on what timeline. The feature stays live for our existing pilot users starting now, so nobody loses the improvement we've already seen. Over the next roughly seven weeks, we're running a properly powered test — about twelve hundred users per arm — specifically designed to tell us, with real statistical confidence, whether that day-thirty effect is real. That fits comfortably inside our eight-week window, so there's no timeline pressure to cut it short. I want to be honest about the risks here too: the day-thirty effect might not hold up at full power, and that's the whole point of testing it properly instead of assuming; engineering has flagged a data backfill that's needed for the ranking logic and we don't have an estimate yet, which could push things; and we need to watch notification opt-outs closely, since we already know from user feedback that irrelevant nudges make people turn notifications off entirely.

### Slide 6 — The Ask

So here's specifically what I need from you today. First, approval to run the seven-week powered test rather than jumping straight to a full-scale rollout — the day-seven result earns that next step, but the day-thirty number doesn't yet earn a full commitment. Second, sign-off to keep the feature running for our current pilot users while that test is in flight, so we don't lose ground we've already gained. And third, I want your explicit agreement that day-seven-to-thirty durability is a separate problem that will need its own initiative later — I don't want this to quietly become "the thing that was supposed to fix retention" when it was only ever designed to fix the first week of it.
