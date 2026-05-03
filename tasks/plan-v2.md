---
type: plan
status: draft
owner: @Sterdb
project: voc-synthesizer
spec: ../SPEC.md
created: 2026-05-02
purpose: Domain model pivot — B2B health benefits → patient/physician/social media
---

# VoC Synthesizer v2 — Domain Model Update Plan

## Context

The VoC Synthesizer was built for a B2B health benefits navigation company (Medefy-like: employers, brokers, care guides). The actual user collects signal from TikTok, Instagram, patient advocacy blogs, patient calls, physician calls, and sales calls. This is a different domain model — the voices are patients, physicians, and caregivers in the wild, not employer-mediated members.

This plan implements 8 updates identified in the product review.

## Dependency Graph

```
T1 Domain config (CLAUDE.md + SPEC.md + input template + theme template)
 ├── T2 Transcript cleaner — add social/blog modes
 ├── T3 Bias auditor — add 3 new checks + update reference
 ├── T4 Severity scorer — social reach heuristic + corroboration boost
 ├── T5 Digest — signal quality indicator
 ├── T6 Example inputs — regenerate 25 files
 │    └── T7 Example outputs — registry, themes, digest, audit
 └── T8 Agents README + validation
```

**Critical path:** T1 → T6 → T7
**Parallel lanes after T1:** T2, T3, T4, T5, T6 (all independent)
**Final gate:** T8 (depends on T2-T7)

---

## Checkpoints

| After | Gate | Criteria |
|-------|------|----------|
| T1 | **Config Review** | New channels, personas, schema fields are internally consistent. Channel tiers defined. Attribution levels documented. |
| T6 | **Input Distribution Review** | 25 inputs match target distribution. Bias seeds present (viral TikTok, platform skew, dominant blogger). |
| T7 | **Example Output Review** | Registry, themes, digest, and audit reflect new domain model. Signal quality indicators appear in digest. New bias checks fire correctly. |
| T8 | **Final Validation** | All files reference correct channel/persona values. No orphaned B2B references. README accurate. |

---

## Tasks

### T1: Update domain config across all governance files

**Files:**
- `/Users/Sterdb/voc-synthesizer/CLAUDE.md` — domain config section
- `/Users/Sterdb/samd-os/SPEC.md` — Sections 4.1, 5
- `/Users/Sterdb/voc-synthesizer/inputs/_INPUT_TEMPLATE.md`
- `/Users/Sterdb/voc-synthesizer/themes/_THEME_TEMPLATE.md` (if affected)

**Changes:**

1. **Replace personas** (covers review item #3):
   ```yaml
   personas:
     - patient          # Primary voice — person with the health condition
     - caregiver        # Family member / advocate speaking on behalf of patient
     - physician        # Provider perspective on patient experience, treatment friction
     - advocate         # Patient advocacy blogger, community leader, influencer
     - sales-prospect   # Prospect in sales pipeline
   ```

2. **Replace channels with tiered model** (covers review item #1):
   ```yaml
   channel-tiers:
     structured:          # Full attribution, rich context, low volume
       - patient-call     # 1:1 patient call transcripts
       - physician-call   # Provider perspective calls
       - sales-call       # Sales/demo call notes
     semi-structured:     # Some attribution, moderate context
       - nps              # NPS survey verbatim responses
       - ticket           # Support ticket descriptions
       - interview        # Discovery or usability interview transcripts
     unstructured:        # Public, anonymous, high volume, weak attribution
       - tiktok           # Short-form video comments, public
       - instagram        # Captions + comments, public
       - patient-advocacy-blog  # Long-form, curated, partially pre-synthesized
   ```

3. **Update input schema** (covers review item #2):
   - Make `client` OPTIONAL (was required)
   - Add `source-url` (optional) — for social/blog posts
   - Add `attribution-level` (optional): `identified | semi-anonymous | anonymous`
   - Add engagement fields (optional): `engagement-views`, `engagement-comments`, `engagement-shares`
   - Add `source-post-id` (optional) — for tracking which social post generated comments

4. **Update `segment_distribution` schema** in registry:
   - Add `by_source_post` to track which social posts/threads generated mentions
   - Add `by_channel_tier` summary (structured/semi-structured/unstructured counts)

5. **Update required fields table:**
   - `input` type: required = type, channel, persona, date (client removed from required)
   - Add new optional fields to documentation

**Acceptance Criteria:**
- [ ] CLAUDE.md domain config uses new personas and tiered channels
- [ ] SPEC.md Section 4.1 input schema shows client as optional
- [ ] SPEC.md Section 5 domain config matches CLAUDE.md
- [ ] Input template has all new optional fields with comments
- [ ] `channel-tiers` concept is documented in both CLAUDE.md and SPEC.md
- [ ] No references to old personas (member, care-guide, hr-admin, broker, employer) remain
- [ ] No references to old channels (call-notes, chat, partner-feedback, qbr) remain

**Verify:** `grep -r "care-guide\|hr-admin\|broker\|employer\|partner-feedback\|qbr" /Users/Sterdb/voc-synthesizer/` returns no hits outside examples/.

> **CHECKPOINT: Config Review**

---

### T2: Update transcript cleaner — add social/blog modes

**File:** `/Users/Sterdb/voc-synthesizer/.claude/skills/transcript-cleaner/SKILL.md`

**Changes:**

1. **Add mode selection** at the top of processing:
   - `clean transcript` / `clean call notes` → existing dialogue mode (updated personas)
   - `clean social post` / `clean tiktok` / `clean instagram` → new social mode
   - `clean blog post` / `clean advocacy blog` → new blog mode

2. **Social post cleaner mode:**
   - Single-speaker (no dialogue labeling needed)
   - Strip platform formatting (@mentions, hashtags preserved, URLs cleaned)
   - Redact handles to `[HANDLE]` (semi-PII)
   - Extract text from video caption format
   - Generate frontmatter with `attribution-level: semi-anonymous`
   - Auto-set channel based on trigger (tiktok/instagram)
   - Add `source-url` and `source-post-id` if provided
   - Add engagement fields if available (views, comments, shares)

3. **Blog post cleaner mode:**
   - Preserve long-form structure
   - Detect and extract individual patient stories as sub-inputs
   - One blog post with 5 patient stories → 5 separate input files + 1 parent blog file
   - Parent file: `patient-advocacy-blog-{date}-001.md`
   - Sub-inputs: `patient-advocacy-blog-{date}-001a.md`, `001b.md`, etc.
   - Generate frontmatter with `attribution-level: semi-anonymous` for blog, `anonymous` for extracted patient stories
   - Set persona to `advocate` for the blog author, `patient` for extracted stories

4. **Update speaker labels** to use new personas:
   - `[PATIENT]`, `[CAREGIVER]`, `[PHYSICIAN]`, `[ADVOCATE]`, etc.

5. **Update PII table:**
   - Add: social media handles → `[HANDLE]`
   - Keep existing patterns (names, SSN, DOB, etc.)

**Acceptance Criteria:**
- [ ] Three distinct modes documented: dialogue, social, blog
- [ ] Social mode handles TikTok/Instagram formatting
- [ ] Blog mode extracts sub-inputs with correct naming convention
- [ ] Redaction table includes handles
- [ ] Speaker labels use new persona names
- [ ] No references to old personas in inference rules
- [ ] Triggers section includes new mode triggers

**Verify:** Review each mode's processing steps end-to-end. Confirm output examples use new frontmatter schema.

---

### T3: Update bias auditor — add 3 new checks

**Files:**
- `/Users/Sterdb/voc-synthesizer/.claude/skills/agents/bias-auditor/SKILL.md`
- `/Users/Sterdb/voc-synthesizer/.claude/skills/agents/bias-auditor/references/response-bias.md`

**Changes to SKILL.md:**

1. **Replace Check 1 (Client Concentration) with Source Concentration:**
   - Since `client` is now optional, concentration checks shift to: are you over-indexed on one platform? One subreddit? One advocacy blog?
   - New threshold: >50% of a theme's mentions from one source (client, platform, or individual blog)
   - Finding format: `[SOURCE CONCENTRATION] X% of THM-nnn mentions from [source].`

2. **Add Check 6: Platform Demographic Bias** (new):
   - Flag when a theme's evidence is >70% from unstructured channels
   - Each platform has a demographic skew: TikTok (18-34), Instagram (female 25-44), advocacy blogs (health-literate, chronic conditions)
   - Finding format: `[PLATFORM BIAS] X% of THM-nnn evidence from unstructured channels. Demographic skew: [description].`
   - Risk: Theme may over-represent the demographics that use that platform
   - Recommendation: "Cross-validate with structured channels (patient calls, physician calls) before roadmap commitment."

3. **Add Check 7: Engagement / Viral Amplification Bias** (new):
   - Flag when a theme's social media mentions cluster around high-engagement content
   - If engagement-views or engagement-shares on source posts are >10x the platform median, flag
   - Finding format: `[VIRAL AMPLIFICATION] THM-nnn has [N] mentions, [M] trace to responses on [1-2] viral posts.`
   - Risk: Volume reflects one viral moment, not broad patient experience
   - Recommendation: "Discount social volume. Verify with structured channels."

4. **Add Check 8: Single-Source Amplification** (new):
   - Flag when >50% of a theme's social media mentions trace to comments/responses on a single post, video, or thread
   - Uses `source-post-id` from input frontmatter to identify clustering
   - Finding format: `[SINGLE-SOURCE AMPLIFICATION] X% of THM-nnn social mentions trace to [1] post/thread.`
   - Risk: The theme reflects one person's story amplified by engagement, not independent patient experiences
   - Recommendation: "Treat the source post as 1 data point regardless of comment volume. Require independent mentions from other posts/sources."

5. **Update Audit Scope section:**
   - Per-theme checks now include: source concentration, recency, sample size, platform bias, viral amplification, single-source amplification
   - Overall checks: channel skew (updated for channel tiers), persona imbalance (updated for new personas)

6. **Update personas referenced** throughout to new set.

**Changes to response-bias.md:**

1. Add new section: **Social Media-Specific Biases**
   - Platform selection bias (each platform's demographic filter)
   - Engagement amplification (viral content inflates volume)
   - Coordinated signal / astroturfing
   - Advocate amplification (one blogger's synthesis ≠ independent data points)

2. Add threshold rationale for new checks:
   - 70% unstructured (platform bias) — why this threshold
   - 50% single-source (amplification) — why this threshold
   - 10x median engagement (viral) — why this threshold

3. Add mitigation strategies for new bias types.

4. Update existing sections to remove B2B-specific examples and add patient/social media examples.

**Acceptance Criteria:**
- [ ] 8 total bias checks documented (5 original + 3 new)
- [ ] Source concentration replaces client concentration where client is absent
- [ ] Platform bias check documented with demographic skew descriptions
- [ ] Viral amplification check uses engagement fields
- [ ] Single-source amplification uses source-post-id
- [ ] Reference doc has social media bias section
- [ ] New thresholds have rationale
- [ ] All persona/channel references updated

**Verify:** Walk through each check mentally against the planned example data bias seeds.

---

### T4: Update severity scorer — social reach heuristic + corroboration

**Files:**
- `/Users/Sterdb/voc-synthesizer/.claude/skills/agents/severity-scorer/SKILL.md`
- `/Users/Sterdb/voc-synthesizer/.claude/skills/agents/severity-scorer/references/rice-scoring.md`

**Changes to SKILL.md:**

1. **Update Reach estimation** — add channel-tier-aware heuristics:
   - **Structured channels** (patient-call, physician-call, sales-call): Current approach works — estimate affected population from known context. Silent majority multiplier applies.
   - **Unstructured channels** (tiktok, instagram, patient-advocacy-blog): Use engagement metrics as proxy. If `engagement-views` available, scale. If not, use platform-average estimates. Do NOT use comment count as reach — one viral post with 200 comments is 1 signal, not 200.
   - **Cross-validate:** A theme appearing in BOTH structured AND unstructured channels gets a corroboration boost to confidence (+10%).

2. **Add Confidence adjustment for new bias types:**
   - Platform demographic bias: -10%
   - Viral amplification: -15%
   - Single-source amplification: -20%

3. **Add Corroboration Boost:**
   - Theme appears in 2+ channel tiers: +10% confidence
   - Theme appears in all 3 channel tiers: +15% confidence
   - Cap: confidence cannot exceed 95%

4. **Update personas and channels** throughout to new set.

**Changes to rice-scoring.md:**

1. Add section: **Reach Estimation for Social/Unstructured Channels**
   - Why comment count ≠ reach
   - Engagement metrics as proxy (views, shares)
   - Platform-specific reach estimation heuristics
   - The advocate amplification problem: one blog post referencing 50 patient stories is different from 50 patient comments

2. Add section: **Cross-Channel Corroboration**
   - Why corroboration matters (same signal from independent sources = higher confidence)
   - How the boost works
   - Worked example with mixed structured/unstructured evidence

3. Update worked example to use new domain (patient/physician instead of member/care-guide).

4. Update confidence adjustment table with new bias types.

**Acceptance Criteria:**
- [ ] Reach estimation has explicit guidance for each channel tier
- [ ] Comment count ≠ reach is explicitly stated
- [ ] Corroboration boost documented with thresholds
- [ ] New confidence adjustments added to table
- [ ] Reference doc has social reach section
- [ ] Worked example uses new personas/channels
- [ ] All old persona/channel references removed

**Verify:** Check that confidence adjustments (old + new) can't drive confidence below 20% floor in a realistic scenario.

---

### T5: Update digest — add signal quality indicator

**File:** `/Users/Sterdb/voc-synthesizer/.claude/skills/voc-weekly-digest/SKILL.md`

**Changes:**

1. **Add signal quality indicator per theme** in the full treatment section:
   ```markdown
   **Signal quality:** Strong | Moderate | Weak
   - Structured evidence: [N] patient calls, [N] physician calls (assessment)
   - Unstructured evidence: [N] TikTok comments on [N] posts, [N] Instagram (assessment)
   ```

2. **Signal quality rules:**
   - **Strong:** ≥50% of mentions from structured channels, OR mentions from 2+ channel tiers with no single-source amplification flags
   - **Moderate:** 25-50% from structured channels, OR mentions from 2+ channel tiers but with amplification flag
   - **Weak:** <25% from structured channels, OR single-source amplification flag active

3. **Update Step 4 (Render Each Theme):**
   - Add signal quality between trend line and bias flag
   - Show structured vs. unstructured evidence breakdown

4. **Update channel breakdown in header:**
   - Group by channel tier: `[N] structured ([N] patient calls, [N] physician calls), [N] unstructured ([N] TikTok, [N] Instagram)`

5. **Update Input Gap Analysis:**
   - Check against new channel list
   - Flag missing channel tiers (e.g., "No structured channel inputs this period — all evidence is unstructured")

6. **Update all persona/channel references** to new model.

**Acceptance Criteria:**
- [ ] Signal quality indicator documented with Strong/Moderate/Weak definitions
- [ ] Rules for each quality level are explicit and testable
- [ ] Full treatment section includes signal quality
- [ ] Header breakdown shows channel tier grouping
- [ ] Gap analysis references new channels and tiers
- [ ] No old persona/channel references remain

**Verify:** Walk through digest format mentally against planned example data.

---

### T6: Regenerate 25 example inputs

**Directory:** `/Users/Sterdb/voc-synthesizer/examples/inputs/`

**Action:** Delete all 25 existing files. Create 25 new files matching the new domain model.

**Target distribution:**

| Channel | Count | Files |
|---------|-------|-------|
| tiktok | 5 | Short comments about patient experiences |
| instagram | 4 | Caption + comment posts |
| patient-advocacy-blog | 3 | Long-form blog excerpts (1 with multiple patient stories) |
| patient-call | 6 | 1:1 call transcripts |
| physician-call | 3 | Provider perspective notes |
| sales-call | 2 | Sales pipeline calls |
| nps | 1 | Survey verbatim |
| ticket | 1 | Support ticket |
| **Total** | **25** | |

**Persona distribution:**

| Persona | Count |
|---------|-------|
| patient | 14 |
| caregiver | 3 |
| physician | 3 |
| advocate | 3 |
| sales-prospect | 2 |

**Date distribution:**
- W14 (Mar 30–Apr 5): 4 inputs
- W15 (Apr 7–12): 5 inputs
- W16 (Apr 14–19): 6 inputs
- W17 (Apr 21–26): 10 inputs

**Intentional bias seeds:**

1. **Viral TikTok amplification:** One TikTok video about medication side effects generates 5 comment-inputs. All 5 share `source-post-id: "tiktok-viral-001"`. The video has engagement-views: 850000, engagement-shares: 12000. This should trigger single-source amplification and viral amplification checks.

2. **Platform skew:** 60% unstructured (12 social/blog), 24% structured (6 patient-call + 3 physician-call = 9... wait, let me recount).

   Actually: tiktok(5) + instagram(4) + blog(3) = 12 unstructured, patient-call(6) + physician-call(3) + sales-call(2) = 11 structured, nps(1) + ticket(1) = 2 semi-structured. That's 48% unstructured — enough to test but not trigger the 70% threshold.

   Adjust: For the platform bias seed, make sure one specific THEME is >70% unstructured. E.g., THM-003 "medication side effect anxiety" has 8 mentions, 6 from TikTok/Instagram.

3. **Dominant advocate blogger:** One advocacy blogger ("CaregiverVoices" blog) is the source for 3 inputs that share the same `source-url` domain. Two of the three contribute to the same theme, creating source concentration.

4. **Balanced control theme:** "Appointment scheduling friction" — mentioned across patient calls, physician calls, Instagram, with multiple sources. No bias flags.

**Design intent — target themes:**
1. **THM-001: "Medication side effect anxiety"** — 8 mentions, 6 from TikTok/Instagram (platform bias seed), 5 from one viral TikTok (amplification seed)
2. **THM-002: "Appointment scheduling friction"** — 7 mentions, balanced across tiers (control)
3. **THM-003: "Insurance pre-authorization delays"** — 5 mentions, physician-heavy
4. **THM-004: "Caregiver burnout / support gap"** — 4 mentions, concentrated in advocacy blogs (source concentration seed)
5. **THM-005: "Telehealth quality concerns"** — 4 mentions, all W17 (recency bias seed)
6. **THM-006: "Cost transparency before treatment"** — 3 mentions, emerging signal
7. **THM-007: "Medication refill confusion"** — 3 mentions, emerging signal

**Acceptance Criteria:**
- [ ] 25 files in examples/inputs/ with valid frontmatter per new schema
- [ ] Distribution matches targets (±1)
- [ ] Bias seeds are verifiable via frontmatter grep
- [ ] Social media inputs have attribution-level, source-url, engagement fields
- [ ] Blog inputs have attribution-level and source-url
- [ ] Structured channel inputs have attribution-level: identified
- [ ] No real PHI/PII
- [ ] File names follow convention: `{channel}-{date}-{nnn}.md`
- [ ] Content is realistic patient/physician/advocate voice (not B2B/employer)

**Verify:** Count by channel, persona, week. Verify source-post-id clustering for viral TikTok. Confirm advocate blog source-url concentration.

> **CHECKPOINT: Input Distribution Review**

---

### T7: Regenerate example outputs

**Files:**
- `/Users/Sterdb/voc-synthesizer/examples/themes/_registry.yaml`
- `/Users/Sterdb/voc-synthesizer/examples/themes/THM-001.md` through `THM-007.md`
- `/Users/Sterdb/voc-synthesizer/examples/digests/digest-2026-W18.md`
- `/Users/Sterdb/voc-synthesizer/examples/audits/bias-audit-2026-W18.md`

**Action:** Delete all existing example outputs. Regenerate from the new example inputs, reflecting the updated agents.

**Registry requirements:**
- 7 themes with correct IDs, counts, distributions
- `segment_distribution` includes `by_source_post` for social-sourced themes
- `by_channel_tier` summary present

**Theme doc requirements:**
- All 7 themes with Summary, Evidence, Kano, RICE, Bias Flags, Related sections
- Signal quality data present (structured vs. unstructured breakdown)
- Quotes from new input files

**Digest requirements:**
- Signal quality indicator for each top theme
- Header shows channel tier grouping
- Bias audit summary includes new check types
- Gap analysis references new channel model

**Audit requirements:**
- Fires: single-source amplification (THM-001), platform bias (THM-001), source concentration (THM-004), recency (THM-005)
- Clean: THM-002 (balanced signal)
- Sample composition uses new dimensions

**Acceptance Criteria:**
- [ ] Registry has 7 themes with valid schema including new fields
- [ ] Theme docs reference correct input files
- [ ] Digest includes signal quality indicators
- [ ] Audit fires expected bias checks on seeded themes
- [ ] THM-002 appears in "What Looks Sound"
- [ ] All references use new personas/channels
- [ ] RICE scores calculate correctly per formula

> **CHECKPOINT: Example Output Review**

---

### T8: Update Agents README + final validation

**Files:**
- `/Users/Sterdb/voc-synthesizer/.claude/skills/agents/README.md`
- `/Users/Sterdb/samd-os/SPEC.md` (update Sections 4.4, 7 for new checks/format)

**Changes:**

1. Update agent table — version bump to 2.0.0 for all agents
2. Update artifact routing table — add new input types (tiktok, instagram, blog)
3. Update output format summary — mention signal quality, new bias checks
4. Update orchestration notes if needed

**Final validation sweep:**
- [ ] `grep -r "member\|care-guide\|hr-admin\|broker\|employer\b" /Users/Sterdb/voc-synthesizer/` — no hits outside this plan doc
- [ ] `grep -r "call-notes\|chat\b\|partner-feedback\|qbr\b" /Users/Sterdb/voc-synthesizer/` — no hits outside this plan doc
- [ ] All 8 SKILL.md/reference files reference correct personas/channels
- [ ] SPEC.md validation checklists updated for new bias checks
- [ ] Example outputs are internally consistent (registry counts match theme docs)

> **CHECKPOINT: Final Validation**

---

## Summary

| Task | Phase | Depends On | Size | Review Item(s) |
|------|-------|-----------|------|----------------|
| T1: Domain config | Foundation | — | Medium | #1, #2, #3 |
| T2: Transcript cleaner | Skills | T1 | Medium | #6 |
| T3: Bias auditor | Agents | T1 | Large | #4 |
| T4: Severity scorer | Agents | T1 | Medium | #5 |
| T5: Digest | Skills | T1 | Small | #7 |
| T6: Example inputs | Data | T1 | Large | #8 |
| T7: Example outputs | Data | T6 | Large | #8 |
| T8: README + validation | Polish | T2-T7 | Small | All |

**Parallel lanes after T1:**
- Lane A: T2 (transcript cleaner)
- Lane B: T3 (bias auditor)
- Lane C: T4 (severity scorer)
- Lane D: T5 (digest)
- Lane E: T6 → T7 (example data → example outputs)
- Join: T8 (after all lanes complete)
